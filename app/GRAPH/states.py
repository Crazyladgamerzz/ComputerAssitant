
from pydantic import BaseModel,Field
from typing import Literal,Optional,TypedDict
from langchain_core.messages import AIMessage,BaseMessage

class SecuritySchema(BaseModel):
    security_violation:Literal['yes','no'] = Field(description='Answer only yes or no if the security has been violated')
    cause:Optional[str] = Field(default=None,description='Short single line answer explaining why the security failed')

class RewrittenScratchpadSchema(BaseModel):
    scratchpad:str = Field(description='Rewritten tool calls history only with relevant information for the user problem')



class State(TypedDict):
    user_input:str
    input_security_status:SecuritySchema
    agent_response: AIMessage
    iteration_count: int
    scratchpad:list[BaseMessage]
    final_answer:str

    @staticmethod
    def get_initial_state(user_input):
        return State({'user_input':user_input,
                      'agent_response':None,
                      'iteration_count':0,
                      'final_answer':'',
                      'scratchpad':[]})
