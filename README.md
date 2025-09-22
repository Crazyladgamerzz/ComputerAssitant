<h1>User Computer Assistant Project</h1>

This project is a python desktop console application using <b>langchain and langgraph</b> to build an agentic system that execute actions in the user computer.

The graph starts with a <b>security layer</b> that will immediatly end if the user input may damage his system or illegal requests.

After, the graph starts the <b>agent loop</b> that uses tool calls capable of execute terminal commands and python code in the user computer (a human confirmation before executing is optionaly added for security). It also has a tool that the agent can make questions or instructions for user preferneces if needed.

If the iteration gets too long the graph can fall into the <b>summarizer node</b> to simplify older tool calls historic by reducing tokens count.