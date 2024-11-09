import json

PRODUCT_CATALOG = {
    "laptop_pro": {
        "id": "LP001",
        "name": "Laptop Pro X1",
        "description": "Powerful laptop with 16GB RAM and 1TB SSD",
        "price": 1299.99,
        "stock": 10
    },
    "smartphone_plus": {
        "id": "SP002",
        "name": "Smartphone Plus 12",
        "description": "Smartphone with 6GB RAM and 128GB storage",
        "price": 799.99,
        "stock": 15
    },
    "wireless_earbuds": {
        "id": "WE003",
        "name": "AudioBuds Pro",
        "description": "Wireless earbuds with noise-cancelling technology",
        "price": 149.99,
        "stock": 20
    },
    "smart_watch": {
        "id": "SW004",
        "name": "SmartWatch Elite",
        "description": "Smartwatch with heart rate monitoring and GPS",
        "price": 299.99,
        "stock": 8
    },
    "tablet_lite": {
        "id": "TL005",
        "name": "Tablet Lite 10",
        "description": "Lightweight tablet with 8GB RAM and 256GB storage",
        "price": 399.99,
        "stock": 12
    }
}

def get_product_info(product_name):
    """
    Retrieve detailed information about a specific product.

    Parameters:
    product_name (str): The exact name of the product to search for.

    Returns:
    str: A JSON string containing the product details if found, otherwise "NOT FOUND".
    """
    # Normalize the product name to match the keys in the product catalog
    product_name = product_name.lower().replace(" ", "_")
    # Retrieve the product information from the catalog
    product = PRODUCT_CATALOG.get(product_name)
    print("Product: ", product, "And type: ", type(product))
    if product:
        # Return the product details as a JSON string
        return json.dumps(product)
    # Return "Not found" if the product does not exist in the catalog
    return "Not found"

def check_stock(product_name):

    product_name = product_name.lower().replace(" ", "_")
    product = PRODUCT_CATALOG.get(product_name)
    
    if product:
        response = f"stock_quantity: {product['stock']}"
        return response
    return "Not found"

def available_tools():
    tools=[
        {
            "type": "function",
            "function": {
                "name": "get_product_info",
                "description": "Get detailed information about a product",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_name": {
                            "type": "string",
                            "description": "The exact name of the product to search for"
                        }
                    },
                    "required": ["product_name"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "check_stock",
                "description": "Check the stock quantity of a product",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_name": {
                            "type": "string",
                            "description": "The exact name of the product to search for"
                        }
                    },
                    "required": ["product_name"]
                }
            }
        }
    ]

    return tools