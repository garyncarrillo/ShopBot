from fastapi import HTTPException
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import time

from .services.product_catalog_service import ProductCatalogService

# Load environment variables from .env file
load_dotenv()


class GptLlm():
    def __init__(self):
        # Initialize the class and retrieve the OpenAI API key from environment variables
        self.open_ai_key = os.getenv('OPENAI_API_KEY')


    def get_tools(self):
        # Definition of available functions (tools) as function objects
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_product_info",
                    "description": "Get product details for a product",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "product_name": {
                                "type": "string",
                                "description": "The name or part of the name of the product."
                            }
                        },
                        "required": ["product_name"],
                        "additionalProperties": False,
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "check_stock",
                    "description": "Get product stock availability for a product",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "stock_availability": {
                                "type": "string",
                                "description": "The stock availability of the product."
                            }
                        },
                        "required": ["product_name"],
                        "additionalProperties": False,
                    }
                }
            }
        ]

    def get_open_ai__assistant_response(
            self,
            query,
            product_name,
    ):
        try:
            # Initialize the OpenAI client
            client = OpenAI(api_key=self.open_ai_key)

            # Call to the get_tools method to retrieve the list of tools
            tools = self.get_tools()
            
            # create Assistants
            assistant = client.beta.assistants.create(
                name="E-commerce Platform Assistant",
                instructions="""AI assistant for an e-commerce platform that provides users with seamless,intuitive access to product details, availability, and purchasing support, ensuring high engagement and personalized recommendations.
                Use the supplied tools to assist the user
                Get the delivery date for a customer's query.
                """,
                model="gpt-4o",
                tools= tools,
            )

            # Create a thread
            thread = client.beta.threads.create()

            # Add the message to the thread
            message = client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=f"{query}",
            )
            
            # Get assistant to respond to the user
            run = client.beta.threads.runs.create_and_poll(
                thread_id=thread.id,
                assistant_id=assistant.id,
            )
            print(run)
            print('*'*40)

            # Initialize lists to store call IDs and function names for each product
            tool_outputs = []
            function_name = []
            call_id = []

            if product_name:
                # Accede al Tool Call ID
                for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                    # Append each call ID and function name to their respective lists
                    call_id.append(tool_call.id)
                    function_name.append(tool_call.function.name)
                
                # Print the lists of call IDs and function names for verification
                print("Call IDs:", call_id)
                print("Function Names:", function_name)
                
            # know when the Assistant has completed processing
            def wait_on_run(run, thread):
                while run.status == "queued" or run.status == "in_progress":
                    run = client.beta.threads.runs.retrieve(
                        thread_id=thread.id,
                        run_id=run.id,
                    )
                    time.sleep(0.5)
                return run
            
            run = wait_on_run(run, thread)

            # List the Messages in the Thread
            messages = client.beta.threads.messages.list(thread_id=thread.id)

            # Instance of ProductCatalogService
            product_service = ProductCatalogService()

            # Check if there are multiple tool calls for different products
            if product_name:
                # Iterate over each `call_id` and `function_name`
                for call_id, function_name in zip(call_id, function_name):
                    # If the tool is get_product_info
                    if function_name == 'get_product_info':
                        # Retrieve product details
                        product_details = product_service.get_product_info(product_name)
                        description = product_details[0].get("description")
                        price = product_details[0].get("price")
                        stock_availability = product_details[0].get("stock_availability")
                        # Create a dictionary with product details
                        product_info = {
                            "description": description,
                            "price": price,
                            "stock_availability": stock_availability
                        }
                        # Convert the dictionary into a JSON string
                        product_info_str = json.dumps(product_info)

                        tool_outputs.append({
                            "tool_call_id": call_id,
                            "output": product_info_str # Assign the output of the function
                        })
                    
                    # If the tool is check_stock
                    elif function_name == 'check_stock':
                        # Check the product stock
                        stock_status = product_service.check_stock(product_name)
                        # Verify if stock_status is a dictionary
                        if isinstance(stock_status, dict):
                            # Convert the dictionary directly to a JSON string
                            stock_status_str = json.dumps(stock_status)
                        else:
                            # If it's not a dictionary, simply convert it to a JSON string
                            stock_status_str = json.dumps({product_name: stock_status})

                        tool_outputs.append({
                            "tool_call_id": call_id,
                            "output": stock_status_str  # Assign the output of the function
                        })
                        
            # Submit all tool outputs at once after collecting them in a list
            if tool_outputs:
                try:
                    run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                        thread_id=thread.id,
                        run_id=run.id,
                        tool_outputs=tool_outputs
                    )
                    print("Tool outputs submitted successfully.")
                except Exception as e:
                    print("Failed to submit tool outputs:", e)
            else:
                print("No tool outputs to submit.")
            
            # know when the Assistant has completed processing
            def wait_on_run(run, thread):
                while run.status == "queued" or run.status == "in_progress":
                    run = client.beta.threads.runs.retrieve(
                        thread_id=thread.id,
                        run_id=run.id,
                    )
                    time.sleep(0.5)
                return run
            
            run = wait_on_run(run, thread)
            # List the Messages in the Thread
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            
            return messages.data[0].content[0].text.value
        except Exception as e:
            raise HTTPException(
                status_code=422,
                detail=f"GptLmm method: generate_open_ai_assistant_response {str(e)}",
            )
        
    def get_open_ai_response(
            self,
            query,
            prompt,
        ):
        try:
            # Initialize the OpenAI client with the provided API key
            client = OpenAI(api_key=self.open_ai_key)
            # Prepare the messages for the chat, including the system and user roles
            messages = [
                {
                    "role": "system",
                    "content": "You are AI assistant for an e-commerce platform that provides users support",
                },
                {
                    "role": "user",
                    "content": f"{prompt}:{query}",
                },
            ]

            # Execute the chat completion request with the specified model
            response = client.chat.completions.create(
                model="gpt-4o",  # The model to be used for generating the response
                messages=messages,  # The messages passed to the chat for context
            )
            # Return the content of the first choice in the response
            return response.choices[0].message.content

        except Exception as e:
            # Raise an HTTP exception with a detailed error message in case of failure
            raise HTTPException(
                status_code=422,
                detail=f"GptLmm method: generate_open_ai_response {str(e)}",
            )