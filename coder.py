import os
import openai
import re
from chatbot import Chatbot

import sys
from io import StringIO

# Setting up OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")


class Coder(Chatbot):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def save_python_code(self, text, file_name = "code.py"):

        # Use regular expressions to extract the Python code block
        match = re.search(r'```python\n(.+?)\n```', text, re.DOTALL)

        # If a match is found, extract the code block and save it to a file in a subfolder
        if match:
            code_block = match.group(1)
            folder_name = "generated_code"
            os.makedirs(folder_name, exist_ok=True)
            with open(os.path.join(folder_name, file_name), 'w') as f:
                f.write(code_block)
            return "Code saved to file '{}/{}'".format(folder_name, file_name)
        else:
            return "No Python code block found."


    def run_python_file(self, file_path):
        # Save current stdin and stderr
        saved_stdin, saved_stderr = sys.stdin, sys.stderr

        try:
            # Redirect stdin and stderr to StringIO objects
            sys.stdin = StringIO()
            sys.stderr = StringIO()

            # Run the file
            exec(open(file_path).read())

            # Return the inputs and outputs captured by StringIO
            return sys.stdin.getvalue().strip(), sys.stderr.getvalue().strip()

        except Exception as e:
            # Return the error message captured by StringIO
            return None, sys.stderr.getvalue().strip()

        finally:
            # Restore original stdin and stderr
            sys.stdin, sys.stderr = saved_stdin, saved_stderr
    def write_code(self, instructions):
        self.respond(""" 
        Write code according to the following instructions:
        """+instructions)
        return self.save_python_code(self.latest_response)

    def improve_file(self, file_path, instructions):
        with open(file_path, 'r') as file:
            contents = file.read()
        self.respond("""
        Improve the following code:
        """+contents+"""
        According to the following instructions:
        """+instructions)
        return self.save_python_code(self.latest_response, "improved_"+os.path.basename(file_path))


# Initiate the bot
Coder_Bot = Coder(
    model="gpt-3.5-turbo",
    max_tokens=1000,
    temperature=0.8,
    pre_prompt="""
    You are a senior python developer who can write professional code.

    You only reply with code, nothing else, unless explicitly asked for.

    The code MUST be enclosed like this:

    ```python
    <code>
    ```
    """
)

# Run the code
Coder_Bot.write_code("A class of objects called fruits.")
print(Coder_Bot.latest_response)