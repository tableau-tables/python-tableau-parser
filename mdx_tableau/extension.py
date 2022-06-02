from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor
from . import tableau

class TableauBlockProcessor(BlockProcessor):

    def test(self, _, block):
        return tableau.test(block)

    def run(self, parent, blocks):
        ast = tableau.to_ast(blocks[0])
        if ast:
            blocks.pop(0)
            tableau.ast_to_html(ast, parent, self.parser)
            return True
        else:
            return False

class TableauExtension(Extension):
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(TableauBlockProcessor(md.parser), 'tableau', 175)

def makeExtension(*args, **kwargs):
    return TableauExtension(*args, **kwargs)
