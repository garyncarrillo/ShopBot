class CustomPromptService:

    def __init__(self) -> None:
        pass
    
    
    def generate_product_name_prompt(self, query):
        generated_prompt = f"""
        You are an expert e-commerce assistant.
        Based only on the provided query, identify and return **only** the full product names from the following list.
        Ignore any additional information or context.

        Query: {query}

        List of products:
        [
            EcoFriendly Water Bottle,
            Organic Cotton T-Shirt,
            Yoga Mat,
            Stainless Steel Travel Mug,
            Bamboo Cutting Board Set,
            Ceramic Plant Pot,
            Stainless Steel Cookware Set,
            Portable Hammock
        ]

        Task: Extract product names from the query, including partial names, nicknames, abbreviations, or misspellings.
        If no matching product is found, return only the name mentioned in the query as a list.
        If no product name is in the query, return None

        Response format: ["product_one_name", "product_two_name", ..., "product_x_name"]
        """.strip()

        return generated_prompt