import re
import xml.etree.ElementTree as etree
from mdx_tableau.parser import parse_row

################ end of parser #########################################

LINE_CONTINUATION = re.compile(r'\\\n')

def merge_continuation_lines(table):
    return LINE_CONTINUATION.sub("", table)

NEWLINE_PATTERN = re.compile(r'\r?\n')

def split_into_rows(table):
    return NEWLINE_PATTERN.split(table.strip())

########################################################################


ALIGNMENT_CLASS = {
        "<": "a-l",
        "=": "a-c",
        ">": "a-r",
        }

class Format:
    def __init__(self, other=None):
        self.alignment = other.alignment if other else "="
        self.span = other.span if other else None
        self.css_classes = other.css_classes  + [] if other else []
        self.heading = other.heading if other else False
        self.propagate_formats = []

    def merge(self, cell_format):
        new_format = Format(self)
      
        for fmt in cell_format:
            if type(fmt) == tuple:
                (mod, fmt) = fmt
                if mod:
                    if not mod == "repeat":
                        print("Invalid format modifier:" + mod)
                    else:
                        new_format.propagate_formats.append(fmt)

            if fmt in ALIGNMENT_CLASS:
                new_format.alignment = fmt
            elif fmt == "^" or fmt == "{":
                new_format.span = fmt
            elif fmt == "#":
                new_format.heading = True
            elif fmt.startswith("."):
                new_format.css_classes.append(fmt[1:])

        return new_format

    def render_tag(self, row, content, extra_attrs, parser):
        tag = "th" if self.heading else "td"
        attrs = self.format_attrs(extra_attrs)
        cell = etree.SubElement(row, tag, attrs)
        parser.parseChunk(cell, content)
        # if extra_attrs and len(extra_attrs) > 0:
        #     attrs = attrs + " " + extra_attrs


    def format_attrs(self, extra_attrs):
        classes = [ ALIGNMENT_CLASS[self.alignment] ]
        if self.css_classes:
            classes = classes + self.css_classes
        cls = " ".join(classes)
        extra_attrs["class"] = cls
        return extra_attrs

class Cell:
    def __init__(self, raw_cell, base_format, row_format):
        (format, content) = raw_cell
        self.content = "".join(content).strip()
        self.format = base_format.merge(row_format + format)
        self.rowspan_count = 0
        self.colspan_count = 0
        self.hidden = False

    def possible_spans(self):
        result = {}
        if self.rowspan_count > 0:
            result["rowspan"] = str(self.rowspan_count + 1)
        if self.colspan_count > 0:
            result["colspan"] = str(self.colspan_count + 1)
        return result
        
    def content_to_html(self, row, parser):
        if not self.hidden:
            self.format.render_tag(row, self.content, self.possible_spans(), parser)

EMPTY_CELL = ( [], [] )

class Row:
    def __init__(self):
        self.cells = []

    def append(self, cell):
        self.cells.append(cell)

    def cellAt(self, n):
        return self.cells[n]

    def looks_like_header(self):
        return all([ (cell.hidden or cell.format.heading) for cell in self.cells ])

    def to_html(self, parent, parser):
        row = etree.SubElement(parent, "tr")

        for cell in self.cells:
            cell.content_to_html(row, parser)

########################################################################

class Result:
    def __init__(self, row_count, col_count):
        self.default_formats = [ Format() for _ in  range(0, col_count) ]
        self.row_count = row_count
        self.col_count = col_count
        self.rows = []
        self.seen_legacy = False
        self.caption = None
        self.table_classes = [ "tableau-table" ]

    def add_content_row(self, cells):
        row = Row()
        row_format = []

        for col in range(0, self.col_count):
            raw_cell = cells[col] if col < len(cells) else EMPTY_CELL
            cell = Cell(raw_cell, self.default_formats[col], row_format)
            row_format += cell.format.propagate_formats
            row.append(cell)

        self.rows.append(row)

    def add_caption_row(self, row):
        classes, caption = row
        if classes:
            self.table_classes += [ cls[1:] for cls in classes ]
        if caption:
            caption = "".join(caption).strip()
            if len(caption):
                self.caption = caption

    def add_format_row(self, row):
        for col, fmt in enumerate(row):
            self.default_formats[col] = self.default_formats[col].merge(fmt)
        
    def add_legacy_format_row(self, row):
        self.add_format_row(row)
        if not self.seen_legacy:
            self.make_rows_into_heading()
            self.seen_legacy = True

    def make_rows_into_heading(self):
        for row in self.rows:
            for cell in row.cells:
                cell.format.heading = True

    def merge_spans(self):
        self.merge_colspan()
        self.merge_rowspan()

    def merge_colspan(self):
        for row in self.rows:
            count = 0
            for col_idx in range(self.col_count-1, -1, -1):
                cell = row.cellAt(col_idx)
                if cell.format.span == "{":
                    count += 1
                    cell.hidden = True
                else:
                    cell.colspan_count = count
                    count = 0
            if count > 0:
                print("Cannot span horizontally in first column of table")

    def merge_rowspan(self):
        for col_idx in range(self.col_count-1, -1, -1):
            count = 0
            for row_idx in range(self.row_count-1, -1, -1):
                cell = self.rows[row_idx].cellAt(col_idx)
                if cell.format.span == "^":
                    count += 1
                    cell.hidden = True
                else:
                    cell.rowspan_count = count
                    count = 0
            if count > 0:
                print("Cannot span vertically in top row of table")

    def split_out_head(self):
        head = []
        body = []
        possibly_head = True

        for row in self.rows:
            if possibly_head:
                if row.looks_like_header():
                    head.append(row)
                else:
                    possibly_head = False
            if not possibly_head:
                body.append(row)

        return head, body


    def to_html(self, parent, parser):
        head, body = self.split_out_head()

        table = etree.SubElement(parent,
                "table",
                { "class": " ".join(self.table_classes)})

        if self.caption:
            caption = etree.SubElement(table, "caption")
            parser.parseChunk(caption, self.caption)

        if head: 
            thead = etree.SubElement(table, "thead")
            for row in head:
                row.to_html(thead, parser)

        if body: 
            tbody = etree.SubElement(table, "tbody")
            for row in body:
                row.to_html(tbody, parser)


########################################################################

# import pprint
# from tatsu.util import asjson
# from tatsu.model import ModelBuilderSemantics

# tableau_parser = compile(GRAMMAR)

TEST_RE = re.compile(r'^\s*\|[^\n]+\|\s*\n\s*\|[^\n]+\|\s*(\n|$)')

def test(block):
    return TEST_RE.match(block)


def to_ast(table):
    table = merge_continuation_lines(table)
    table = split_into_rows(table)

    ast = []
    for row in table:
        parsed = parse_row(row)
        if parsed:
            ast.append(parsed)
        else:
            return False

    if not ast:
        return False

    row_count = len([ 1 for (kind, _) in ast if kind == "content" ])
    col_count = max([ len(cells) for (_, cells) in ast ])

    result = Result(row_count, col_count)

    for (kind, cells) in ast:
        if kind == "format":
            result.add_format_row(cells)

        elif kind == "legacy_format":
            result.add_legacy_format_row(cells)

        elif kind == "content":
            result.add_content_row(cells)

        elif kind == "caption":
            result.add_caption_row(cells)
        else:
            print("Internal error. Unknown row type", kind)

    result.merge_spans()
    return result

def ast_to_html(result, parent, parser):
    result.to_html(parent, parser)

