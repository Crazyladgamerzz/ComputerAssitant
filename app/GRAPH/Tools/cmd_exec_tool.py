from langchain.tools import BaseTool
import os
import subprocess

class CMDExecTool(BaseTool):
    name: str = 'cmd_exec_tool'
    description: str = ('Execute a terminal command and return the output.\n' \
    'cd commands must be executed individually, like: cd path\n'
    'Args:\n'
    'command: prompt command to be executed, make sure to include only the command with correct syntax.')
    request_confirmation: bool = True

    def _run(self, command:str):
        cmd_split = command.split()
        b_change_dir = False
        if cmd_split[0].lower() == 'cd' and len(cmd_split) == 2:
            command = command + " && cd"
            b_change_dir = True

        if self.request_confirmation and input(f'Execute command: {command}? (y/n)') != 'y':
            return input('Cancel message: ')
        
        prompt_result = subprocess.run(command, shell=True, capture_output=True,encoding='utf-8',errors='ignore')
        output = prompt_result.stdout.strip() if prompt_result.returncode == 0 else prompt_result.stderr.strip()

        if b_change_dir and prompt_result.returncode == 0:
            try:
                os.chdir(output)
            except Exception as e:
                output = 'error: ' + str(e)
        
        if len(output) > 0 and prompt_result.returncode != 0:
            output = f'Error: {output}'
        elif len(output) == 0:
            output = 'success' if prompt_result.returncode == 0 else 'error'

        return output

