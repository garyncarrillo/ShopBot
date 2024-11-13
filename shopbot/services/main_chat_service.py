from ..gpt_llm import GptLlm
import json

from .custom_prompts_service import CustomPromptService

class MainChatService:
    # Constructor method: Initializes the instance
    def __init__(self):
        pass
        
        
    def handlle_user_query(
            self,
            query,
        ):
        # Add prompt to get the product name from the query
        product_name_prompt = CustomPromptService().generate_product_name_prompt(query)
        # Get the product name from the query
        product_name = GptLlm().get_open_ai_response(
            query=None, prompt=product_name_prompt
        )
        # Process query with product name
        if product_name != 'None':
            # Product name list
            product_list = json.loads(product_name)
            print(product_list)
            # Retrieve a response from the Open AI Assistant based on the user's query and a list of product names.
            chat_llm_response = GptLlm().get_open_ai__assistant_response(
                query=query, product_name=product_list
            )
        else:
            # Process query without product name
            chat_llm_response = GptLlm().get_open_ai__assistant_response(
                query=query, product_name=None
            )
        return {"assistant_response": chat_llm_response}