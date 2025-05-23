from openai import OpenAI
from functions import function_specs, functions_map
from prompts.react_prompt import build_prompt
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_agent(user_goal):
    prompt = build_prompt(user_goal)
    messages = [{"role": "user", "content": prompt}]
    
    while True:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            tools=function_specs,
            tool_choice="auto"
        )
        msg = response.choices[0].message

        if msg.tool_calls:
            tool_call = msg.tool_calls[0]
            fn_name = tool_call.function.name
            args = tool_call.function.arguments
            tool_response = functions_map[fn_name](**eval(args))
            messages.append(msg)
            messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": tool_response})
        else:
            return msg.content
