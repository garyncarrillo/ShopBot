import json
from fastapi import HTTPException

class ProductCatalogService:
    def __init__(self, catalog_path="product_catalog.json"):
        # Initialize the product catalog service with a path to the catalog file
        self.catalog_path = catalog_path
        self.products = self.load_catalog()

    def load_catalog(self):
        # Load the product catalog from a JSON file
        try:
            with open(self.catalog_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            # Raise an HTTPException if the catalog file is not found
            raise HTTPException(status_code=404, detail="Product catalog file not found.")
        except json.JSONDecodeError:
            # Raise an HTTPException if there is an error decoding the JSON file
            raise HTTPException(status_code=500, detail="Error decoding product catalog file.")

    def get_product_info(self, product_names):
        # If product_names is a single name, convert it to a list
        if isinstance(product_names, str):
            product_names = [product_names]

        products_info = []
        for product_name in product_names:
            # Search for product information by name
            product_info = next((product for product in self.products if product["product_name"] == product_name), None)
            if product_info:
                products_info.append(product_info)
            else:
                # Return a response if the product is not found in stock
                return {"ai_response":f"Product {product_name} not found in stock."}
        
        return products_info

    def check_stock(self, product_names):
        # If product_names is a single name, convert it to a list
        if isinstance(product_names, str):
            product_names = [product_names]

        stock_status = {}
        for product_name in product_names:
            # Search for product information and check stock availability
            product_info = next((product for product in self.products if product["product_name"] == product_name), None)
            if product_info:
                stock_status[product_name] = product_info["stock_availability"] > 0
            else:
                # Return a response if the product is not found in stock
                return {"ai_response":f"Product {product_name} not found in stock."}
        
        return stock_status

