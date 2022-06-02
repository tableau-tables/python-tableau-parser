
# Tableau: Extended Table Creation

Add features I needed to create tables for my courses, such as:

|!.hlines.vlines.wide How place values work in binary |
|: #<            | >…    |
|#… Bit position | 7     | 6     | 5     | 4     | 3     | 2     | 1     | 0     |
| Bits           | 1     | 0     | 0     | 1     | 0     | 0     | 1     | 1     |
| Place value    | $2^7$ | $2^6$ | $2^5$ | $2^4$ | $2^3$ | $2^2$ | $2^1$ | $2^0$ |
|^               | 128   | 64    | 32    | 16    | 8     | 4     | 2     |     1 |
| Bit x value    | 128   |  0    |  0    | 16    | 0     | 0     | 2     |     1 |

Features include:

* Headerless tables
* Multiline headers
* Multiple separate headers
* Headers in columns
* Row and column span
* Per cell alignment and CSS classes
* Default attributes, both down columns and across rows
* Table-wide classes
* Caption
* Continuation lines
* Compatible (with two exceptions) with standard markdown tables

## Basic Markup

A traditional markdown table might look like:

~~~ md
| Country | Region       | Minimum Nos. | Probably Nos. | Speculative Nos. |
|:--------|:-------------|-------------:|--------------:|-----------------:|
| India   | Northern     |          750 |           875 |            1,000 |
| India   | Northeastern |        7,200 |         9,250 |           11,300 |
| Nepal   |              |           41 |            50 |               60 |
~~~

Columns are separated using pipe characters ("|"), and the second line both
separated the headings from the table body and also gives the alignment of each
of the columns.

This table is also a valid tableau table. Formatted, it looks like this:

| Country | Region       | Minimum Nos. | Probably Nos. | Speculative Nos. |
|:--------|:-------------|-------------:|--------------:|-----------------:|
| India   | Northern     |          750 |           875 |            1,000 |
| India   | Northeastern |        7,200 |         9,250 |           11,300 |
| Nepal   |              |           41 |            50 |               60 |

A tableau table is a markdown block where each line starts and ends with
a pipe character. (This is different from conventional markdown tables,
where the opening and closing pipes are sometimes optional.)

## Multiple Header Lines

~~~
| Country | Region       | Minimum  | Probable | Speculative  |
|         |              | Numbers  | Numbers  | Numbers      |
|:--------|:-------------|---------:|---------:|-------------:|
| India   | Northern     |      750 |      875 |        1,000 |
| India   | Northeastern |    7,200 |    9,250 |       11,300 |
| Nepal   |              |       41 |       50 |           60 |
~~~

Every line before the format line is considered a header.

| Country | Region       | Minimum  | Probable | Speculative  |
|         |              | Numbers  | Numbers  | Numbers      |
|:--------|:-------------|---------:|---------:|-------------:|
| India   | Northern     |      750 |      875 |        1,000 |
| India   | Northeastern |    7,200 |    9,250 |       11,300 |
| Nepal   |              |       41 |       50 |           60 |

## No Header Lines

~~~
|:--------|:-------------|---------:|---------:|-------------:|
| India   | Northern     |      750 |      875 |        1,000 |
| India   | Northeastern |    7,200 |    9,250 |       11,300 |
| Nepal   |              |       41 |       50 |           60 |
~~~

|:--------|:-------------|---------:|---------:|-------------:|
| India   | Northern     |      750 |      875 |        1,000 |
| India   | Northeastern |    7,200 |    9,250 |       11,300 |
| Nepal   |              |       41 |       50 |           60 |

## No Format Line

~~~
| India   | Northern     |      750 |      875 |        1,000 |
| India   | Northeastern |    7,200 |    9,250 |       11,300 |
| Nepal   |              |       41 |       50 |           60 |
~~~

| India   | Northern     |      750 |      875 |        1,000 |
| India   | Northeastern |    7,200 |    9,250 |       11,300 |
| Nepal   |              |       41 |       50 |           60 |

## Spanned Header Rows

~~~
| Country | Region       | Minimum  | Probable | Speculative  |
|^        |^             | Numbers  | Numbers  | Numbers      |
|:--------|:-------------|---------:|---------:|-------------:|
| India   | Northern     |      750 |      875 |        1,000 |
| India   | Northeastern |    7,200 |    9,250 |       11,300 |
| Nepal   |              |       41 |       50 |           60 |
~~~



| Country | Region       | Minimum  | Probable | Speculative  |
|^        |^             | Numbers  | Numbers  | Numbers      |
|:--------|:-------------|---------:|---------:|-------------:|
| India   | Northern     |      750 |      875 |        1,000 |
| India   | Northeastern |    7,200 |    9,250 |       11,300 |
| Nepal   |              |       41 |       50 |           60 |

## Tableau Format Specifications

In the preceding table, the two cells at the start of the second row are
merged with the cells above. This is done using the up-arrow format
specification.

Every cell in a tableau table can have one or more format
specifications. They must immediately follow the cell's opening pipe,
with no intervening spaces.

The valid format specifications are:

|!.striped |
|:  |< |
| `^` | Merge this cell with the one above it. Multiple cells in a column may be merged |
| `{` | Merge this cell with the one to its left. Multiple cells in a row may be merged |
| `<` | Left align this cell |
| `=` | Center this cell |
| `>` | Right align this cell |
| `#` | Make this cell a header (use `<th>`) |
| `.class` | Apply the CSS class to this cell |

The two span specifications (`^` and `{`) must appear alone (as the cell
formatting is taken from the cell above or to the left). Otherwise, a
format specification can contain an optional alignment specifier, an
optional heading specifier, and zero or more class specifiers. These
three types of specifier can appear in any order: 

``` markdown
|<#.warn.big Note |.info> Meaning |
```

The first cell is a left-aligned heading cell with the CSS classes `warn` and `big`, while
the second is a right-aligned cell with the class `info`.

## Propagating Formats Along a Row

Any format specification can be followed by an ellipsis (either three
periods `...` or a Unicode ellipsis, `…`). This format will then be
propagated as a default to subsequent cells in the same row. 

For example, a tableau header row can be created using:

~~~ markdown
|# Country |# Region       |# Minimum Nos. |# Probably Nos. |# Speculative Nos. |
| ...      |
~~~

|# Country |# Region       |# Minimum Nos. |# Probably Nos. |# Speculative Nos. |
| ...      |

You can also use the heading specifier on just the first column, and use
an ellipsis to propagate it.

~~~ markdown
|#… Country |Region       |Minimum Nos. |Probably Nos. |Speculative Nos. |
| ...      |
~~~

|#… Country |Region       |Minimum Nos. |Probably Nos. |Speculative Nos. |
| ...      |

The propagated format is just a default: it can be overridden in any
subsequent cell.

~~~ markdown
|#...>... Animal 1 | Animal 1 | Animal 1 | Animal 1 | Animal 1 |
|>... ant | bee |<cat | dog | elk |
~~~

|!.vlines |
|#...>... Animal 1 | Animal 1 | Animal 1 | Animal 1 | Animal 1 |
|>... ant | bee |<cat | dog | elk |

You can even override it in the cell that initially propagates it:

~~~ markdown
|#...>... Animal 1 | Animal 1 | Animal 1 | Animal 1 | Animal 1 |
|>...< ant | bee |<cat | dog | elk |
~~~

|!.vlines |
|#...>... Animal 1 | Animal 1 | Animal 1 | Animal 1 | Animal 1 |
|>...< ant | bee |<cat | dog | elk |

## Propagating Formats Down a Column

Any tableau row that starts `|:` is a format row. We've already seen
a version of this:

~~~ md
| Country | Region       | Minimum Nos. | Probably Nos. | Speculative Nos. |
|:--------|:-------------|-------------:|--------------:|-----------------:|
| India   | Northern     |          750 |           875 |            1,000 |
| India   | Northeastern |        7,200 |         9,250 |           11,300 |
| Nepal   |              |           41 |            50 |               60 |
~~~

The `:---` specifier in the first cell of line two is conventional
markdown for "subsequent cells in this column should be left aligned".

You can specify the sme thing using tableau format specifiers:

~~~ md
|#... Country | Region       | Minimum Nos. | Probably Nos. | Speculative Nos. |
|:<           |<             |>...          |               |                  |
| India       | Northern     |          750 |           875 |            1,000 |
| India       | Northeastern |        7,200 |         9,250 |           11,300 |
| Nepal       |              |           41 |            50 |               60 |
~~~

|#... Country | Region       | Minimum Nos. | Probably Nos. | Speculative Nos. |
|:<           |<             |>...          |               |                  |
| India       | Northern     |          750 |           875 |            1,000 |
| India       | Northeastern |        7,200 |         9,250 |           11,300 |
| Nepal       |              |           41 |            50 |               60 |

By moving the format line above the header, you can align it, too:

~~~ md
|:<           |<             |>...          |               |                  |
|#... Country | Region       | Minimum Nos. | Probably Nos. | Speculative Nos. |
| India       | Northern     |          750 |           875 |            1,000 |
| India       | Northeastern |        7,200 |         9,250 |           11,300 |
| Nepal       |              |           41 |            50 |               60 |
~~~

|:<           |<             |>...          |               |                  |
|#... Country | Region       | Minimum Nos. | Probably Nos. | Speculative Nos. |
| India       | Northern     |          750 |           875 |            1,000 |
| India       | Northeastern |        7,200 |         9,250 |           11,300 |
| Nepal       |              |           41 |            50 |               60 |

Here's another example that makes both the first row and first column
into headers.

~~~ markdown
|: #<            | >     | >     | >     | >     | >     | >     | >     | >     |
|#… Bit position | 7     | 6     | 5     | 4     | 3     | 2     | 1     | 0     |
| Bits           | 1     | 0     | 0     | 1     | 0     | 0     | 1     | 1     |
| Place value    | $2^7$ | $2^6$ | $2^5$ | $2^4$ | $2^3$ | $2^2$ | $2^1$ | $2^0$ |
|^               | 128   | 64    | 32    | 16    | 8     | 4     | 2     |     1 |
| Bit x value    | 128   |  0    |  0    | 16    | 0     | 0     | 2     |     1 |
~~~

|: #<            | >     | >     | >     | >     | >     | >     | >     | >     |
|#… Bit position | 7     | 6     | 5     | 4     | 3     | 2     | 1     | 0     |
| Bits           | 1     | 0     | 0     | 1     | 0     | 0     | 1     | 1     |
| Place value    | $2^7$ | $2^6$ | $2^5$ | $2^4$ | $2^3$ | $2^2$ | $2^1$ | $2^0$ |
|^               | 128   | 64    | 32    | 16    | 8     | 4     | 2     |     1 |
| Bit x value    | 128   |  0    |  0    | 16    | 0     | 0     | 2     |     1 |

## Table Level Formatting

A line starting `|!` can be used to add CSS classes and/or a caption to
the table.

~~~ markdown
|!.hlines.vlines.wide How place values work in binary |
|: #<            | >     | >     | >     | >     | >     | >     | >     | >     |
|#… Bit position | 7     | 6     | 5     | 4     | 3     | 2     | 1     | 0     |
| Bits           | 1     | 0     | 0     | 1     | 0     | 0     | 1     | 1     |
| Place value    | $2^7$ | $2^6$ | $2^5$ | $2^4$ | $2^3$ | $2^2$ | $2^1$ | $2^0$ |
|^               | 128   | 64    | 32    | 16    | 8     | 4     | 2     |     1 |
| Bit x value    | 128   |  0    |  0    | 16    | 0     | 0     | 2     |     1 |
~~~

The three classes add horizontal and vertical lines to the table and
force it to be a full column wide. Any text after the format becomes the 
table caption.


|!.hlines.vlines.wide How place values work in binary |
|: #<            | >     | >     | >     | >     | >     | >     | >     | >     |
|#… Bit position | 7     | 6     | 5     | 4     | 3     | 2     | 1     | 0     |
| Bits           | 1     | 0     | 0     | 1     | 0     | 0     | 1     | 1     |
| Place value    | $2^7$ | $2^6$ | $2^5$ | $2^4$ | $2^3$ | $2^2$ | $2^1$ | $2^0$ |
|^               | 128   | 64    | 32    | 16    | 8     | 4     | 2     |     1 |
| Bit x value    | 128   |  0    |  0    | 16    | 0     | 0     | 2     |     1 |

Another example of table-level classes is the list of [format
specifications](#tableau-format-specifications), which uses the CSS `stripe` class to
get alternating row backgrounds.


### Nutrition Facts

One more example, showing a mockup of a nutrition facts panel. We use
a CSS style to make the first and last columns bold (starting at the
"Calories 200" line). 

We use three more styles to draw light, medium, or
bold lines under rows, and colspans both to indent subcategories and to
control where lines are drawn. i

Finally we use a table formatting line (the last line in the table) to
both set a caption and to give the table a CSS class. We use that class
both to draw a box around the table and to namespace our other styles.

Here's the table markup:

~~~ markdown
|:< |< |> |
|.ulb…  Serving Size 1/2 cup (about 82g)<br/>Servings Per Container 8 |{ |{ |
|.ull… Amount Per Serving |{ |{ |
|:.bold  | |.bold|
|.ulm… Calories 200 |{ | Calories from Fat 130 |
|.ull… | | % Daily Value |
| Total Fat  |{                   | 22% |
|  |.ull… Saturated Fat 9g   | 22% |
|.ull…  | Trans Fat 0g       |  0% |
|.ull… Cholesterol 55mg  |{  | 18% |
|.ull… Sodium 40mg |{        |  2% |
| Total Carbohydrate 17g |{       |  6% |
|  |.ull… Dietary Fiber 1g   |  4% |
|.ull…  | Sugars 14g         |  0% |
|.ulm… Protein 3g |{ |
|!.nutrition (from \
   [examples of data tables](https://wpdatatables.com/examples-of-data-tables/)) |
~~~

The CSS styles are included inline in the Markdown:

~~~ css
<style>
table.nutrition {
  border: solid 6px #666;
}
table.nutrition .bold {
    font-weight: bold;
}

table.nutrition .ull {
    border-bottom: 1px solid #222;
}

table.nutrition .ulm {
    border-bottom: 2px solid #333;
}

table.nutrition .ulb {
    border-bottom: 8px solid #666;
}
</style>
~~~

And the result is:


|:< |< |> |
|.ulb…  Serving Size 1/2 cup (about 82g)<br/>Servings Per Container 8 |{ |{ |
|.ull… Amount Per Serving |{ |{ |
|:.bold  | |.bold|
|.ulm… Calories 200 |{ | Calories from Fat 130 |
|.ull… | | % Daily Value |
| Total Fat  |{                   | 22% |
|  |.ull… Saturated Fat 9g   | 22% |
|.ull…  | Trans Fat 0g       |  0% |
|.ull… Cholesterol 55mg  |{  | 18% |
|.ull… Sodium 40mg |{        |  2% |
| Total Carbohydrate 17g |{       |  6% |
|  |.ull… Dietary Fiber 1g   |  4% |
|.ull…  | Sugars 14g         |  0% |
|.ulm… Protein 3g |{ |
|!.nutrition (from \
   [examples of data tables](https://wpdatatables.com/examples-of-data-tables/)) |

<style>
table.nutrition {
  border: solid 6px #666;
}
table.nutrition .bold {
    font-weight: bold;
}

table.nutrition .ull {
    border-bottom: 1px solid #222;
}

table.nutrition .ulm {
    border-bottom: 2px solid #333;
}

table.nutrition .ulb {
    border-bottom: 8px solid #666;
}
</style>


## Formatting and CSS

Unlike most markdown table formatters, tableau uses CSS classes and not
inline markup to format tables. The stylesheet I used to format this
document can be found in [docs/assets/css/tableau]() (and a version
using Postcss' preset-env can be found in the project's `css` directory.)
