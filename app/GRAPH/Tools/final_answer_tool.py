# from langchain.tools import BaseTool

# #from GRAPH.states import State
# #from langchain.chat_models.base import BaseChatModel


# class FinalAnswerTool(BaseTool):

#     name: str = 'final_answer_tool'
#     description: str = 'Once the problem is solved or failed after many attempts, write a final answer to the user.\nInput: message to the user.'
#     #'this tool can be used to generate a final answer'
#     #' using the sequence of iterations stored in the Scratchpad.\n')
#     #'No input required.')

#     #llm:BaseChatModel


#     def _run(self,final_answer): #state:State
#         return final_answer
#         # scratchpad = '\n\n'.join([s.get_state_scratchpad() for s in state['agent_state']])

#         # prompt_str = (
#         #     "Problem: {problem}\n"
#         #     "Sequence of actions to solve the problem:\n" \
#         #     "{scratchpad}\n" \
#         #     "Based on the problem and the solution give a short final answer with a single line sentence."
#         # ).format(problem=state['user_input'],scratchpad=scratchpad)

#         # return self.llm.invoke(prompt_str).content

