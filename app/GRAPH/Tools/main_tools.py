
from GRAPH.Tools.ask_user_tool import AskUserTool
from GRAPH.Tools.cmd_exec_tool import CMDExecTool
from GRAPH.Tools.run_python_code_tool import RunPythonCodeTool
#from GRAPH.Tools.final_answer_tool import FinalAnswerTool

class MainTools:
    def __init__(self,human_validation=True):
        self.init_tools(human_validation)

    def init_tools(self,human_validation):
        ask_user_tool = AskUserTool()
        cmd_exec_tool = CMDExecTool(request_confirmation=human_validation)
        run_python_code_tool = RunPythonCodeTool(request_confirmation=human_validation)
        #final_answer_tool = FinalAnswerTool()

        tools = [cmd_exec_tool,ask_user_tool,run_python_code_tool]#final_answer_tool
        self.tools = { tool.name:tool for tool in tools }
        