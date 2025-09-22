
#from GRAPH.states import State
import os
import locale
import platform
from GRAPH import config
from typing import Literal
import json
import tiktoken

def get_sys_info():
    sys_info = (
        "###Basic user computer system information:\n"
        f"Username: {os.getlogin()}\n"
        f"Language: {locale.getlocale()[0]} (you may receive some outputs in this language but always answer in english)\n"
        f"Operational system: {platform.system()} {platform.architecture()[0]}\n"
        f"Terminal: {os.getenv('COMSPEC') if os.name == 'nt' else os.getenv('SHELL')}\n"
        f"You are in the directory: {os.getcwd()} (you can change it with cd commands)"
        ).replace('\\','\\\\')
    return sys_info

def get_scratchpad_len(scratchpad):
    encoding = tiktoken.encoding_for_model('gpt-4o')
    total_len=0
    for msg in scratchpad:
        total_len += len(encoding.encode(msg.content) )#len(msg.content)
        if hasattr(msg,'tool_calls'):
            total_len += len( encoding.encode(json.dumps(msg.tool_calls[0])) )
    return total_len

def debug_node(node_name,input_=None,output=None,color:Literal['red','green','blue','default'] = 'blue'):
    if config.DEBUG_GRAPH:
        color_ = {'red':'\033[31m','green':'\033[32m','blue':'\033[36m','default':''}[color]
        print(f'\033[1m{color_}========================= START {node_name} =========================\033[0m\033[0m')
        print_messages(input_,'INPUT')
        print_messages(output,'OUTPUT')       
        print()

def print_messages(msgs,label):
    if msgs:
        print()
        print(f'\033[1m\033[34m--- <{label}> ---\033[0m\033[0m')
        if isinstance(msgs,list):
            for msg in msgs: msg.pretty_print()
        else:
            print(str(msgs))

