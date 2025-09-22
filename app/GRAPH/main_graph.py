
from GRAPH.llms import LLMs,LLMModels
from GRAPH.Tools.main_tools import MainTools
from GRAPH.states import State
from GRAPH.Nodes.nodes import Nodes

from langgraph.graph import StateGraph,START,END

class MainGraph:
    def __init__(self,llm_models:LLMModels,human_validation,max_iterations):
        self.create_graph(llm_models,human_validation,max_iterations)

    def create_graph(self,llm_models,human_validation,max_iterations):
        main_tools = MainTools(human_validation=human_validation)
        llms = LLMs(llm_models=llm_models,main_tools=main_tools)
        nodes = Nodes(llms=llms,main_tools=main_tools,max_iterations=max_iterations)

        graph = StateGraph(State)

        graph.add_node('security_node',nodes.security_node)
        graph.add_node('agent_node',nodes.agent_node)
        graph.add_node('execute_action_node',nodes.execute_action_node)
        graph.add_node('summarize_scratchpad_node',nodes.summarize_scratchpad_node)

        graph.add_edge(START,'security_node')

        graph.add_conditional_edges('security_node',
                                    nodes.security_condition,
                                    {
                                        'continue':'agent_node',
                                        'stop':END
                                    })

        graph.add_conditional_edges('agent_node',
                                    nodes.tool_condition,
                                    {
                                        'execute_action':'execute_action_node',
                                        '__end__':END,
                                    })
        graph.add_conditional_edges('execute_action_node',
                                    nodes.summarize_scratchpad_condition,
                                    {
                                        'summarize':'summarize_scratchpad_node',
                                        'continue':'agent_node',
                                    })
        graph.add_edge('summarize_scratchpad_node','agent_node')

        self.graph = graph.compile()
    
    def invoke(self,user_input):
        initial_state = State.get_initial_state(user_input=user_input)
        return self.graph.invoke(initial_state)
    

