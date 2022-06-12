# Extended Table Syntax for Markdown

[Tableau Tables](https://tableau-tables.github.io) gives you way more control 
over the tables you create in Markdown documents. `tableau-marked` is the version of Tableau 
for the Python Markdown processor.

#### Headers

* Headerless tables
* Multiline headers
* Multiple separate headers
* Headers in columns and rows
* Captions

#### Layout

* Layout uses CSS styles and not inline attributes (making it easier to
  change the style of a whole document)
* Per cell alignment and CSS classes
* Default attributes, both down columns and across rows
* Table-wide classes
* Row and column span
* Continuation lines

Here are [some samples](https://tableau-tables.github.io/samples/).

## Installation


1. Install the extension:

    ~~~ console
    $ pip install git+https://github.com/tableau-tables/python-tableau-parser
    ~~~

    (once things have settled it'll be moved to PyPl.)

2. Add it to your list of Markdown extensions

   ~~~ python
   markdown.markdown(your_documenti, extensions=[..., 'python-tableau-parser', ...])
   ~~~

   If you're using mkdocs, simply add it to the list of extensions in `mkdocs.yml`:

   ~~~ yaml
   markdown_extensions:
      - def_list
      - python-tableau-parser
      - pymdownx.superfences
      :       :
  ~~~

## Writing Tables Using Tableau Tables

Pop on over to the [documentation site](https://tableau-tables.github.io).
