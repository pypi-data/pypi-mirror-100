import os
import io

# Parses the lines present in input content whereever a variable or variable expression is present


def _variable_parser(text):
    '''
    Description:
    This function parses the given text with variables and returns the variables and strings in comma separated format to put them directly to a print statement

    Parameters:
    text (string) : This string is supposed to have plain text with variables or variable expressions

    Returns: The plain text and variables / variable expressions are returned as a comma separated string which can be directly put into a print statement

    Example:

            $ _variable_parser("Hello {{ world }}")
            "Hello",world
    '''
    left_marker = "{{"
    right_marker = "}}"
    quotes = '"'
    output = []

    while len(text) != 0:
        if left_marker in text:
            text = text.split(left_marker, 1)
            if text[0] != "":
                output.append(quotes+(text[0].strip())+quotes)
            text = text[1].strip().split(right_marker, 1)
            output.append(text[0].strip())
            if text[1] != "":
                text = text[1]
        else:
            if text[-1] != "":
                output.append(quotes+text+quotes)
            break

    return(",".join(output))


# Checks for {{ , }} , {% , %}, if and for blocks' syntaxes and returns "good" if everything works and returns error messages if otherwise
def _syntax_check(text):
    left_marker = "{{"
    right_marker = "}}"
    left_if_marker = "{%"
    right_if_marker = "%}"
    if_block = "{% if"
    for_block = "{% for"
    end_if_block = "endif"
    end_for_block = "endfor"
    if not text.count(if_block) == text.count(end_if_block) and text.count((for_block)) == text.count((end_for_block)):
        return "SyntaxError: please check 'if' or 'for' blocks"
    for every_line in text.split("\n"):
        if not every_line.count(left_marker) == every_line.count(right_marker):
            return "SyntaxError: please check '{{' and '}}'"
        if not every_line.count(left_if_marker) == every_line.count(right_if_marker):
            return "SyntaxError: please check '{%' and '%}'"
    return "good"

# Builds the python code for the input supplied with variables and saves it in the 'output_string'


def _code_builder(input_content, variables):
    '''
    Description:
    This function builds executable python code with appropriate indentation so that the code can be run as such to render the user's input text.
    It processes plain lines, lines with if,else,elif,for blocks and lines with variables and variable expressions

    Parameters:
    input_content (string) : This is the user input, which is assumed to have multiple lines
    variables (dictionary) : This contains the list of variables and their values as key-value pairs

    Returns: Executable python code as a string

    Example:
            $sample_input = "
             This is where it all starts!!!
             Hello {{ text }} This is a wonderful day. My name is {{ name }}.
             "
            $sample_variables = {
                "text" : "World !"
                "name" : "Python"
                }
            $_code_builder(sample_input, sample_variables)
            text = "World !"
            name = "Python"
            print("Hello",text,"This is a wonderful day. My name is",name)
    '''

    variable_marker = "{{"
    left_marker = "{%"
    right_marker = "%}"
    end_if_block = "endif"
    end_for_block = "endfor"
    line_break = "\n"
    output_string = "def mould_function(f):"+line_break
    indent = 4
    space = " "
    quotes = "'''"
    assignment_sign = " = "
    scoping_colon = ": "
    print_block_start = "print("
    print_block_end = ", file=f)"

    for key, value in variables.items():
        # with open(output_file, "a") as f:
        if type(value) != str:
            output_string = output_string + \
                (indent*space) + key + \
                assignment_sign + str(value) + line_break
        else:
            output_string = output_string + \
                (indent*space)+key+assignment_sign + \
                quotes+str(value)+quotes+line_break

    for every_line in input_content.split(line_break):
        line = every_line.strip()

        # Checks for if,else,elif and for blocks and adds the relevant python code block to the output code

        if line.startswith(left_marker) and line.endswith(right_marker) and not end_if_block in line.split() and not end_for_block in line.split():
            line_split = line.split()
            if line_split[1] in ["else", "elif"]:
                indent -= 4
                output_string = output_string + \
                    (indent*space) + \
                    space.join(line_split[1:-1])+scoping_colon+line_break
                indent += 4
            elif line_split[1] in ["if", "for"]:
                output_string = output_string + \
                    (indent*space) + \
                    space.join(line_split[1:-1])+scoping_colon+line_break
                indent += 4

        # Checks for endif block to close the indentation generated for if block previously in the output code

        elif line.startswith(left_marker) and line.endswith(right_marker) and (end_if_block in line.split() or end_for_block in line.split()):
            indent -= 4

        # Adds the variable declaration statements and variable expression statements in output python code

        elif variable_marker in line and left_marker not in line:
            output_string = output_string + \
                (indent*space)+print_block_start + \
                _variable_parser(line)+print_block_end+line_break

        # Checks for plain lines to be printed as such and add them to the output code

        elif variable_marker not in line and left_marker not in line:
            output_string = output_string + \
                (indent*space)+print_block_start + quotes + \
                line+quotes+print_block_end+line_break
    return output_string


# Wrapper function that calls the code builder with input content and input variables

def it(input_template_content, input_variables):
    '''
    Description:
    This function gets the user input and renders the templated output with values applied for the variables, conditionals and loops processed

    Parameters:
    input_template_content (string or file) : This is the user input, which can be a string or a file.
    input_variables (dictionary) : This is the collection of variables and their values as a dictionary

    Returns:
    output_text (string) : Returns the rendered file as a string

    Usage Example:
                $ sample_input = "
                This is where it all starts!!!
                Hello {{ text }} This is a wonderful day. My name is {{ name }}.
                {% if a < b %}
                'b' is bigger
                The value of b is {{ b }}
                {% else %}
                'a' is bigger
                The value of a is {{ a }}
                {% endif %}
                "
                $ sample_variables = {
                "text" : "World !"
                "name" : "Python"
                "a" : 50
                "b" : 100
                }
                $ mould.it(sample_input,sample_variables)
                This is where it all starts!!!
                Hello World ! This is a wonderful day. My name is Python
                'b' is bigger
                The value of b is 100

    '''
    try:
        input_content = ""
        # Checks whether the input_variables is a dictionary and if it is otherwise, returns to user with the same message
        if type(input_variables) != dict:
            return "Error: input_variables should be of type 'dictionary'"

        if os.path.isfile(input_template_content) and len(open(input_template_content).read().strip()) != 0:
            input_content = open(input_template_content).read()
        elif len(input_template_content.strip()) != 0:
            input_content = input_template_content
        else:
            return "Error: 'input_template_content' cannot be empty"

        syntax_check_result = _syntax_check(input_content)

        if syntax_check_result != "good":
            return syntax_check_result

        built_code = _code_builder(input_content, input_variables)
        # Running the generated code 'built-code' in a separate environment and returs the output back to user
        try:
            f = io.StringIO()
            env = {}
            exec(built_code, env)
            built_code_output = env['mould_function']
            built_code_output(f)
            return f.getvalue().strip()
        except NameError:
            return "NameError : Not all variables used, are present in 'input_variables' dictionary"
        except SyntaxError as e:
            return "SyntaxError: variables (or) 'if' (or) 'for' is not correctly syntaxed"
        except TypeError:
            return "TypeError: Please check whether the variables used in 'for' are of the allowed datatypes"
    except:
        return "An error occurred. Please try again"
