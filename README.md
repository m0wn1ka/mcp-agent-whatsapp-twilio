# mcpServer-ReAct agent-whatsapp
## tech used
- reAct  agent which would call tools
- mcp server and tools, agent will use these tools whenever necessary
- tool to send whatsapp msg using twilio
- flask server which would work as webhook 
## usecase
- say we want to fill our place when talking  to other persons 
- so we use this agent
- when ever we receive a msg, the agent will reply using the pre saved context
## how it works
- flask endpoint /webhook will listen for incoming requests
- i ran the flask server and using ngrok i got a publicly accessible url
- i gave this url in twilio whatsapp callback
- so when a msg reaches the my twilio number, this callback is invoked
- my callback in my system will call the agent 
- the agent uses the available tools and uses the given context
- using a mcp tool user will be given reply
## useful commands
- ngrok http http://localhost:8000
