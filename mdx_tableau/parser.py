from strscan import StringScanner

EXPECTED_ROWS = """
A table should contain two or more rows, each starting
and ending with a pipe character ("|").
""".strip()

def parse_fail(msg):
    print(msg)
    return False

def unknown_table_row(row):
    return parse_fail("Can't decipher table row:" + row)

def parse_row(row):
    row = StringScanner(row.strip())

    result = ( legacy_format_row(row) 
            or new_format_row(row) 
            or table_title_row(row)
            or content_row(row)
            or unknown_table_row(row.peek(100)))

    if not result:
        return parse_fail(EXPECTED_ROWS)

    return result

def legacy_format_row(row):
    fmt = row.scan(r'\s*\|\s*(:?---+:?\s*\|\s*)+$')
    if not fmt:
        return False
    formats = fmt.split("|")
    formats.pop(0)
    formats.pop()

    formats = [ map_legacy(f.strip()) for f in formats]
    return ( "legacy_format", formats )

def map_legacy(fmt):
    sc = fmt.startswith(":")
    ec = fmt.endswith(":")
   
    if sc and ec:
        return ["="]
    elif sc:
        return ["<"]
    elif ec:
        return [">"]
    else:
        return [ "=" ]

def new_format_row(row):
    if not row.check(r'\s*\|:'):
        return False

    formats = []

    while True:
        if row.scan(r'\s*\|\s*$'):
            break
        if not row.scan(r'\s*\|:?\s*'):
            return False
        mods = maybe_modifiers(row)
        formats.append(mods)

    return ( "format", formats )

def table_title_row(row):
    if not row.scan(r'\s*\|!'):
        return False
    classes = modifiers(row, class_modifier)
    caption = cell_content(row)
    return ( "caption", ( classes, caption )) 

def content_row(row):
    result = []
    a_cell = cell(row)
    while a_cell:
        result.append(a_cell)
        a_cell = cell(row)

    if not result:
        return False

    return  ( "content", result )

def cell(row):
    if not row.scan(r'\s*\|'):
        return False
    modifiers = maybe_modifiers(row)
    row.skip(r'\s*')
    content = cell_content(row)
    if not content:
        return False

    return ( modifiers, content )

def cell_content(row):
    result = []
    fragment = cell_fragment(row)
    while fragment:
        result.append(fragment)
        fragment = cell_fragment(row)

    # empty cell?
    if not result and row.check(r'\|'):
        result = [ "" ]

    return result 

def cell_fragment(row):
    return (row.scan(r'[^`$|\\]+') or  # regular characters
            row.scan(r'`[^`]+`')   or  # inline code
            row.scan(r'\$[^$]+\$') or  # inline math
            row.scan(r'\\\|'))           # escaped pipe

def maybe_modifiers(row):
    span = span_modifier(row)
    if span:
        return [ span ]
    else:
        return other_modifiers(row)


def span_modifier(row):
    return row.scan(r'[{^]')

def modifiers(row, kind):
    result = []
    mod = kind(row)
    while mod:
        if row.scan(r'(\.\.\.)|…'):
            mod = ("repeat", mod)

        result.append(mod)
        mod = kind(row)
    return result

def other_modifiers(row):
    return modifiers(row, other_modifier)

def other_modifier(row):
    return alignment_modifier(row) or class_modifier(row) or heading_modifier(row)

def alignment_modifier(row):
    return row.scan(r'[<=>]')

def class_modifier(row):
    return row.scan(r'\.(?!\d)[-\w]+')


def heading_modifier(row):
    return row.scan('#')


