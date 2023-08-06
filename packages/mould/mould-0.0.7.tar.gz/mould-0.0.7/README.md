# <i><b>mould</i></b> - A minimalistic templating engine for Python

This Python library helps to render HTML pages and plain text with variable substitutions, if conditions and for loops.


## Templating syntax :

## To delcare variables enclose the variable name with '{{ ' and ' }}'

    Hello {{ text }} -- 'text' is the variable here

You can use the same syntax to write variable expressions.

    This is line number {{ n+10 }}


## <b>if</b> conditional
<br>
Use '{% ' and ' %}' to enclose the lines where an if block starts and use the same with 'endif' keyword for closing the if blocks

    
    {% if 5 < 6  %}
    Hello world!
    {% endif %}
    
Variables can also be used to write if conditions. Inside the conditional statement, the variables can be written as such. The enclosing syntax mentioned above is not required.

    {% if x > y %}
    Hello Python!
    {% endif %}
    
<b>if</b> block supports 'else' and 'elif' as well.

    {% if x > y %}
    Hello X!
    {% elif z > x %}
    Hello Z!
    {% else %}
    Hello ABC!
    {% endif %}

## <b>for</b> loop

Use '{% ' and ' %}' to enclose the lines where a 'for' block starts and use the same with 'endfor' keyword for closing the 'for' blocks
    
    {% for n in numbers %}
    This is line {{ n }} printed using for loop
    {% endfor %}

In the above code, 'n' and 'numbers' are variables where 'n' is the looping variable and 'numbers' is the list on whose items, the loop is run.

<b>for</b> supports looping over lists, strings and dictionaries

# How to install:

You can get this from <i>PyPI</i>  using pip

    pip install mould

Alternatively, you can get it from <i>git</i> also using pip.

    pip install https://github.com/ramk95/mould-it/archive/refs/heads/master.zip

# How to use:
Import the library to your python program
    
    import mould

Call the mould.it() function with your input file / input text along with a dictionary of variables that you have used in your text / input file

    mould.it(input_text, variables_dictionary)

This will return the rendered output. You can either print it direclty or save it.

    print(mould.it(input_text, variables_dictionary))
or

    rendered_data = mould.it(input_text, variables_dictionary)

# Dependencies:

<i>mould</i> uses python standard libraries <b>io</b> and <b>os</b>. No other dependent packages are required.

# Example:

        import mould

        input = "Hello {{ var }}"
        variables = {"var" : "world !"}

        print(mould.it(input,variables))



        Output:
        Hello world !