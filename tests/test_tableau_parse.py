import unittest

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from  mdx_tableau import tableau

def c(content, format={}):
    return ( format, content )

DEFAULT_FORMAT = {
            'alignment': "=",
            "span": None,
            "heading": False,
            "css_classes": [],
        }
        
class TestTableauParse(unittest.TestCase):

    def assertCell(self, actual, expected):
        ef, ec = expected
        format = DEFAULT_FORMAT | ef
        self.assertEqual(actual.content, ec)
        self.assertEqual(actual.format.alignment, format["alignment"])
        self.assertEqual(actual.format.span, format["span"])
        self.assertEqual(actual.format.heading, format["heading"])
        self.assertEqual(actual.format.css_classes, format["css_classes"])

    def assertResult(self, result, expected):
        self.assertEqual(len(result.rows), len(expected))
        for i, row in enumerate(result.rows):
            self.assertEqual(len(row.cells), len(expected[i]))
            for j, cell in enumerate(row.cells):
                self.assertCell(cell, expected[i][j])

    def test_simple_table(self):
        block = "\n".join([
                    "| a | b |",
                    "| d | e |",
                ])
        result = tableau.to_ast(block)
        self.assertResult(result, [ 
            [ c("a"), c("b") ],
            [ c("d"), c("e") ],
        ])

    def test_table_pads_column_length(self):
        block = "\n".join([
                    "| a | b |",
                    "| d | e | f |",
                    "| g |",
                ])
        result = tableau.to_ast(block)
        self.assertResult(result, [ 
            [ c("a"), c("b"), c("") ],
            [ c("d"), c("e"), c("f") ],
            [ c("g"), c(""), c("") ],
        ])

    def test_table_empty_columns(self):
        block = "\n".join([
                    "| a |   |",
                    "|   | e | f |",
                    "| g |",
                ])
        result = tableau.to_ast(block)
        self.assertResult(result, [ 
            [ c("a"), c(""),  c("")  ],
            [ c(""),  c("e"), c("f") ],
            [ c("g"), c(""),  c("")  ],
        ])

    def test_format_row_included_in_padding(self):
        block = "\n".join([
                    "| a | b |",
                    "|:< |:= |:> |",
                    "| g |",
                ])
        result = tableau.to_ast(block)
        self.assertResult(result, [ 
            [ c("a"), c("b"), c("")  ],
            [ c("g", {"alignment": "<"}), c(""),  c("", {"alignment": ">"})  ],
        ])

    def test_format_row_applies_alignment_to_subsequent_rows(self):
        block = "\n".join([
                    "| a | b |",
                    "|:< |:= |:> |",
                    "| c | e | f | g |",
                    "| h |",
                ])
        result = tableau.to_ast(block)
        self.assertResult(result, [ 
            [ c("a"), c("b"), c(""), c("") ],
            [ c("c", {"alignment": "<"}), c("e"),  c("f", {"alignment": ">"}), c("g")  ],
            [ c("h", { "alignment": "<"}), c(""),c("", {"alignment": ">"}),  c(""), ]
        ])

    def test_column_repeat_format_applies_to_subsequent_columns(self):
        block = "\n".join([
                    "| a |>… b | c | d |",
                    "| h |",
                ])
        result = tableau.to_ast(block)
        right = { "alignment": ">"}
        self.assertResult(result, [ 
            [ c("a"), c("b", right), c("c", right), c("d", right) ],
            [ c("h"), c(""), c(""), c("")    ]
        ])

    def test_column_repeat_can_be_overridden(self):
        block = "\n".join([
                    "| a |>… b | c |< d |",
                    "| h |",
                ])
        result = tableau.to_ast(block)
        right = { "alignment": ">"}
        left  = { "alignment": "<"}
        self.assertResult(result, [ 
            [ c("a"), c("b", right), c("c", right), c("d", left) ],
            [ c("h"), c(""), c(""), c("")    ]
        ])

    def test_legacy_format_row_applies_alignment_to_subsequent_rows(self):
        block = "\n".join([
                    "|:--- |:---: | ---: |",
                    "| c | e | f | g |",
                    "| h |",
                ])
        result = tableau.to_ast(block)
        self.assertResult(result, [ 
            [ c("c", {"alignment": "<"}), c("e"),  c("f", {"alignment": ">"}), c("g")  ],
            [ c("h", { "alignment": "<"}), c(""),c("", {"alignment": ">"}),  c(""), ]
        ])

    def test_legacy_format_makes_preceding_row_a_header(self):
        block = "\n".join([
                    "| a | b |",
                    "|:--- |:---: | ---: |",
                    "| c | e | f | g |",
                    "| h |",
                ])
        result = tableau.to_ast(block)
        self.assertResult(result, [ 
            [ c("a", {"heading": True}), c("b", {"heading": True}), c("", {"heading": True}), c("", {"heading": True}) ],
            [ c("c", {"alignment": "<"}), c("e"),  c("f", {"alignment": ">"}), c("g")  ],
            [ c("h", { "alignment": "<"}), c(""),c("", {"alignment": ">"}),  c(""), ]
        ])

    def test_legacy_format_makes_preceding_rows_a_header(self):
        block = "\n".join([
                    "| a | b |",
                    "| x | y |",
                    "|:--- |:---: |",
                    "| c | e |",
                    "| h |",
                ])
        result = tableau.to_ast(block)
        self.assertResult(result, [ 
            [ c("a", {"heading": True}), c("b", {"heading": True}) ],
            [ c("x", {"heading": True}), c("y", {"heading": True}) ],
            [ c("c", {"alignment": "<"}), c("e") ],
            [ c("h", { "alignment": "<"}), c("") ],
        ])


    def test_header_row(self):
        block = "\n".join([
                    "|# a |# b |",
                    "| d | e |",
                ])
        result = tableau.to_ast(block)
        self.assertResult(result, [ 
            [ c("a", {"heading": True}), c("b", {"heading": True}) ],
            [ c("d"), c("e") ],
        ])

    def test_headers_anywhere(self):
        block = "\n".join([
                    "|# a | b |",
                    "| d |# e |",
                ])
        result = tableau.to_ast(block)
        self.assertResult(result, [ 
            [ c("a", {"heading": True}), c("b") ],
            [ c("d"), c("e", {"heading": True}) ],
        ])


    def test_headers_propagate(self):
        block = "\n".join([
                    "|:# |   |",
                    "| a | b |",
                    "| d | e |",
                ])

        result = tableau.to_ast(block)
        self.assertResult(result, [ 
            [ c("a", {"heading": True}), c("b") ],
            [ c("d", {"heading": True}), c("e") ],
        ])

    def test_single_rowspan(self):
        block = "\n".join([
                    "| a | b |",
                    "|^  | e |",
                ])

        result = tableau.to_ast(block)
        self.assertResult(result, [ 
            [ c("a"), c("b") ],
            [ c("", { "span": "^"}), c("e") ],
        ])

    def test_single_colspan(self):
        block = "\n".join([
                    "| a | b |",
                    "| d |{e |",
                ])

        result = tableau.to_ast(block)
        self.assertResult(result, [ 
            [ c("a"), c("b") ],
            [ c("d"), c("e", { "span": "{"})]
        ])

    def test_class_names_as_formats(self):
        block = "\n".join([
                    "|.c1 a | b |",
                    "| d |.c2.c3> e |",
                ])

        result = tableau.to_ast(block)
        self.assertResult(result, [ 
            [ c("a", { "css_classes": [ "c1" ]}), c("b") ],
            [ c("d"), c("e", { "alignment": ">", "css_classes": [ "c2", "c3" ]})]
        ])

    def test_caption(self):
        block = "\n".join([
                    "|!.c1.c2 My Caption |"
                    "| a | b |",
                    "| d |{e |",
                ])

        result = tableau.to_ast(block)
        self.assertEqual(result.caption, "My Caption")
        self.assertEqual(result.table_classes, [ "tableau-table", "c1", "c2" ])

    def test_no_header_but_format(self):
        block = "\n".join([
            "|:---:|:---:|",
                    "| a | b |",
                    "| d | e |",
                ])
        result = tableau.to_ast(block)
        self.assertResult(result, [ 
            [ c("a"), c("b") ],
            [ c("d"), c("e") ],
        ])

if __name__ == '__main__':
    unittest.main()
