<h1>User Computer Assistant Project</h1>

Python desktop console application using <b>langchain and langgraph</b> to build an agentic system that execute actions in the user computer.

The graph package developed can be found at  [app/GRAPH](https://github.com/c-azb/ComputerAssitant/tree/main/app/GRAPH). It starts with a <b>security node</b> that will immediately end if the user input solution may damage his system or illegal requests.

After, the graph starts the <b>agent loop</b> that uses tool calls capable of execute terminal commands and python code in the user computer (a human confirmation before executing is optionaly added for security). It also has a tool that the agent can make questions or instructions for user preferences if needed.

If the iteration gets too long the graph can fall into the <b>summarizer node</b> to simplify older tool calls history by reducing tokens count.