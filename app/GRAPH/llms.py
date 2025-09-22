
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
import os

from GRAPH.states import RewrittenScratchpadSchema,SecuritySchema
from GRAPH.Tools.main_tools import MainTools
from enum import Enum
from GRAPH.config import OLLAMA_URL

from typing import Literal
class CustomChatGroq(ChatGroq):
    reasoning_effort:Literal['none', 'default','low','medium','high']

class LLMSource(Enum):
    OLLAMA=0
    GROQ=1

class LLMModel:
    class Defaults(Enum):
        LLAMA3b=('llama3.2:3b',LLMSource.OLLAMA)
        LLAMA8b=('llama3.1:8b',LLMSource.OLLAMA)
        QWEN8b=('qwen3:8b',LLMSource.OLLAMA)

        LLAMA70b = ('llama-3.3-70b-versatile',LLMSource.GROQ)
        QWEN32b = ('qwen/qwen3-32b',LLMSource.GROQ)
        GPT_OSS20b = ('openai/gpt-oss-20b',LLMSource.GROQ)
        GPT_OSS120b = ('openai/gpt-oss-120b',LLMSource.GROQ)
    
    @staticmethod
    def default(default:Defaults,reasoning:Literal['none', 'default','low','medium','high']='none',temperature=0.7):
        return LLMModel(default.value[0],default.value[1],reasoning=reasoning,temperature=temperature)
    
    def __init__(self,model_name:str,model_source:LLMSource,reasoning:Literal['none', 'default','low','medium','high'] = 'none',temperature:float = 0.7):
        self.model_name = model_name
        self.model_source = model_source
        self.reasoning = reasoning
        self.temperature = temperature

class LLMModels:
    def __init__(self,agent_llm_model:LLMModel,scratchpad_llm_model:LLMModel = None,security_llm_model:LLMModel = None):
        self.agent_llm_model = agent_llm_model
        self.scratchpad_llm_model = scratchpad_llm_model
        self.security_llm_model = security_llm_model

class LLMs:
    def __init__(self,llm_models:LLMModels,main_tools:MainTools):
        self.setup_llms(llm_models,main_tools)

    def setup_llms(self,llm_models:LLMModels,main_tools:MainTools):
        agent_llm = self.get_llm(llm_models.agent_llm_model)
        scratchpad_llm = self.get_llm(llm_models.scratchpad_llm_model) if llm_models.scratchpad_llm_model is not None else agent_llm
        security_llm = self.get_llm(llm_models.security_llm_model) if llm_models.security_llm_model is not None else agent_llm

        self.llm_agent = agent_llm.bind_tools( list(main_tools.tools.values()) )
        self.llm_scratchpad = scratchpad_llm.with_structured_output(RewrittenScratchpadSchema)
        self.llm_security = security_llm.with_structured_output(SecuritySchema)
    
    def get_llm(self,llm_model:LLMModel):
        if llm_model.model_source == LLMSource.GROQ and 'GROQ_API_KEY' in os.environ:
            return CustomChatGroq(model=llm_model.model_name,
                            temperature=llm_model.temperature,
                            reasoning_effort= llm_model.reasoning,
                            reasoning_format= 'parsed')
        elif llm_model.model_source == LLMSource.OLLAMA:
            return ChatOllama(base_url=OLLAMA_URL,
                              model=llm_model.model_name,
                              temperature=llm_model.temperature,
                              reasoning=llm_model.reasoning != 'none')
        
        raise ValueError('Unsuported llm model, suported models source are GROQ and OLLAMA.\nFor GROQ make sure the api key is set.')

    
