from flask import Flask, request, jsonify
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from TwilioToRadha import send_whatsapp_message
from mcp.server.fastmcp import FastMCP
import logging 
log = logging.getLogger('werkzeug')
log.setLevel(logging.CRITICAL)  
logging.getLogger("twilio").setLevel(logging.CRITICAL)
load_dotenv()
app = Flask(__name__)
mcp = FastMCP("Whatsapp-Agent")
@mcp.tool()
def send_whatsapp_message_tool(
    body: str = "Hello from Twilio!",
):
    """Send a WhatsApp message via Twilio"""
    # print(" send_whatsapp_message_tool called with:", body)
    send_whatsapp_message(body)
    return {"status": "sent", "body": body}
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)
agent = create_react_agent(
    llm,
    tools=[send_whatsapp_message_tool]
)
persona_prompt = (
    "You are Radha Mounika chatting with a friend on WhatsApp. "
    "Always reply casually in first person, as if you are Radha. "
    "Here is info about you: "
    "I am working as an SDE at Lloyds, studied B.Tech at IIIT Nuzvid, "
    "did NCC from 4A Battalion Kakinada, have projects in ML and web dev, "
    "I love to travel, explore new places, learn new tech, "
    "solve problems, help others, and I’m a quick learner and team player. "
    "Keep replies short and natural (like WhatsApp style). "
    "If someone asks something not in the info, just say "
    "'I don’t want to share it'."
)
@app.route("/webhook", methods=["POST"])
def webhook():
    """Handle incoming WhatsApp webhook from Twilio"""
    try:
        form_data = request.form.to_dict()
        # print("Received form data:", form_data)
        body = form_data.get("Body")
        if not body:
            return "No body in message", 200
        print(" User:", body)
        response = agent.invoke({
            "messages": [
                ("system", persona_prompt),
                ("user", body)
            ]
        })
        final_reply = response["messages"][-1].content
        print(" Radha:", final_reply)
        send_whatsapp_message(final_reply)
        return "Webhook processed!", 200
    except Exception as e:
        print(" Error:", e)
        return "Error processing webhook", 500
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002, debug=False)
