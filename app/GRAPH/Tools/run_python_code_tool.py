
from langchain.tools import BaseTool

class RunPythonCodeTool(BaseTool):
    name: str = 'run_python_code_tool'
    description: str = ('Execute python code.\n'
    'Usefull to execute actions in the user computer, get relevant information, manage files, etc.\n'
    'The code will be executed using the python command exec(), make sure to use to correct format for it.\n'
    "If any information should be seen in the output, the value should be stored in a global variable called 'return_value'\n"
    #"Also avoid using ; for formatting, instead use \\t and \\n\n"
    "Here is a simple format example using return_value:\n"
    "def sum(x,y):\n"
    "\treturn x+y\n"
    "return_value=sum(3,5)\n"
    'Args:\n'
    'python_code: python code string, make sure to include only the code with the correct syntax.\n'
    )
    request_confirmation: bool = True

    def _run(self,python_code:str):
        if self.request_confirmation and input('Run code (y/n):\n\n'+python_code) != 'y':
            return input('Cancel message: ')
        
        sandbox = {'__buildins__':__builtins__}
        try:
            exec(python_code,sandbox)
            return str( sandbox.get('return_value','success') )
        except Exception as e:
            return 'Error: '+ str(e)