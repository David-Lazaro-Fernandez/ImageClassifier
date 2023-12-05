from openai import OpenAI
import json
from tools import get_user_bills, get_all_bills
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY", None)
client = OpenAI()

# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API

def read_json():
    with open('instructions.json') as json_file:
        data = json.load(json_file)
        return data
json_data = read_json()

def run_conversation():
    # Step 1: send the conversation and available functions to the model
    messages = [{"role": "user", "content": "Hola, por favor descarga las facturas recibidas de este mes de todos los usuarios"}]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=json_data,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    # Step 2: check if the model wanted to call a function
    if tool_calls:
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_user_bills": get_user_bills,
            "get_all_bills": get_all_bills,
        }  # only one function in this example, but you can have multiple
        messages.append(response_message)  # extend conversation with assistant's reply
        # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                type_of_bill=function_args.get("type_of_bill"),
                user=function_args.get("user"),
            )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
        )  # get a new response from the model where it can see the function response
        return second_response
print(run_conversation())
print(run_conversation().choices[0].message.content)