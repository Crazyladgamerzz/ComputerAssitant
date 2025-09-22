
from langchain.tools import BaseTool


class AskUserTool(BaseTool):
    name: str = 'ask_user_tool'
    description: str = ('Ask the user a question.\n'
    #'Usefull to ask relevant information that the user may not included in the input, like file, folder names and other preferences.\n'
    #'Avoid asking the user if you can do it by yourself.\n'
    'Args:\n'
    'question: question to be displayed to the user.')

    def _run(self, question):
        return input(question)
        #return f"Question: {question}\nAnswer: {answer}"