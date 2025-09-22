
from GRAPH.llms import LLMs
from GRAPH.states import State,SecuritySchema
from GRAPH.Nodes.utils import get_sys_info,debug_node,get_scratchpad_len
from GRAPH.Tools.main_tools import MainTools
import GRAPH.config as config
from typing import Literal
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage,ToolMessage
#import json

class Nodes:
    def __init__(self,llms:LLMs,main_tools:MainTools,max_iterations:int=-1):
        self.llms = llms
        self.main_tools = main_tools
        self.max_iterations = max_iterations
    
    def security_node(self,state:State):
        if config.SKIP_SECURITY:
            return {'input_security_status':SecuritySchema(security_violation='no',cause=None)}

        prompt_str = (
            'You are a input security checker for a task computer assistant.\n'
            'The system is designed to execute tasks in the user computer, '
            'so it\'s fine if the user asks to perform safe tasks on his computer.\n'
            'Your task is to answer only yes or no. '
            'You should answer yes when the input may be dangerous for the user system. '
            'If it is safe answer no.\n'
    
            'User input:\n'
            '{user_input}'
        ).format(user_input=state['user_input'])

        response = self.llms.llm_security.invoke(prompt_str)
        debug_node('security_node',input_=prompt_str,output=response)
        return {'input_security_status':response,'final_answer': '' if response.security_violation == 'no' else response.cause }
    
    def security_condition(self,state:State) -> Literal['continue','stop']:
        if 'input_security_status' not in state: return 'stop'
        return 'continue' if state['input_security_status'].security_violation == 'no' else 'stop'
    
    def agent_node(self,state:State):
        system_message = (
            'You are an agent that solves user computer problems\n'
            f'{get_sys_info()}\n\n'
            'You must work in a loop where every iteration you will receive the output of the previous iteration.\n'
            'You should use this iterations history to pick your next action\n'
            'You can pick multiple tools if their results are independent from each other.\n'
            'If the tool call return an error, try to solve it using available tools or using alternative methods.\n' \
            'Once the problem is solved or failed after many attempts do not pick any tool, instead just give a short final answer.\n' \
            'If you don\'t pick any tool the loop execution will end.\n'
           # 'Before providing a final answer you can ask the user for a feedback or if he needs anything else with the ask user tool.'
        )
        messages = [
            SystemMessage(system_message),
            HumanMessage(state['user_input']),
            *state['scratchpad']
        ]
        
        response = self.llms.llm_agent.invoke(messages)
        debug_node(f"agent_node : iteration {state['iteration_count']+1}",input_=messages,output=[response],color='green')
        return {'agent_response':response,'final_answer':response.content,'iteration_count':state['iteration_count']+1}
    

    def execute_action_node(self,state:State):
        agent_response = state['agent_response']
        scratchpad = state['scratchpad'].copy()
        
        for tool_call in agent_response.tool_calls:
            tool_name = tool_call['name']
            tool_args = tool_call['args']
            tool = self.main_tools.tools.get(tool_name,None)
            if tool:
                tool_response = tool.invoke(tool_args)

                ai_msg = AIMessage(content='',tool_calls=[tool_call]) #ai_msg = AIMessage(content=json.dumps(tool_call)) 
                #ai_msg = AIMessage(content=json.dumps(tool_call)) 
                tool_msg = ToolMessage(content=tool_response,tool_call_id=tool_call['id'])
                scratchpad += [ai_msg,tool_msg]

        debug_node(node_name='execute_action_node',output=scratchpad)
        return {'scratchpad':scratchpad}



    def tool_condition(self,state:State) -> Literal['execute_action','__end__']:
        agent_response = state['agent_response']
        next_node = '__end__'

        if len(state['final_answer']) > 0:
            next_node = '__end__'
        elif self.max_iterations > 0 and state['iteration_count'] >= self.max_iterations:
            next_node = '__end__'
        elif hasattr(agent_response,'tool_calls') and len(agent_response.tool_calls) > 0:
            next_node = 'execute_action'
        
        debug_node('tool_condition',output=next_node)
        
        if next_node != '__end__' and config.CONFIRM_EVERY_LOOP and input('Continue iteration? (y/n)').strip() != 'y':
            next_node = '__end__'
        
        return next_node
    
    def summarize_scratchpad_condition(self,state:State) -> Literal['summarize','continue']:
        if config.MAX_SCRATCHPAD_LEN < 0 or len(state['scratchpad']) < 4: 
            return 'continue'

        scratchpad_len = get_scratchpad_len( state['scratchpad'][:-2] )
        next_node = 'continue'

        if scratchpad_len > config.MAX_SCRATCHPAD_LEN:
            next_node = 'summarize'
        
        debug_node('summarize_scratchpad_condition',input_=f'Scratchpad len: {scratchpad_len}',output=next_node)
        return next_node
    
    def summarize_scratchpad_node(self,state:State):
        scratchpad = state['scratchpad'][:-2]
        msgs = [
            SystemMessage((f"You are a tool calls input and output summarizer that extracts only relevant information related to the problem: "
                          f"{state['user_input']}")),
            *scratchpad,
            HumanMessage('Write a short summary.')
        ]
        scratchpad_summary = 'Summary of previous tool calls\n' + self.llms.llm_scratchpad.invoke(msgs).scratchpad

        new_scratchpad = [AIMessage(scratchpad_summary)] + state['scratchpad'][-2:]

        debug_node('summarize_scratchpad_node',input_=msgs,output=new_scratchpad)
        return {'scratchpad':new_scratchpad}


