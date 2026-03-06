from fastapi import FastAPI

app = FastAPI()

products = [
    {"id": 1, "name": "Smartphone", "price": 25000, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "mouse", "price": 2000, "category": "Electronics", "in_stock": True},
    {"id": 3, "name": "Coffee Mug", "price": 300, "category": "Kitchen", "in_stock": True},
    {"id": 4, "name": "Notebook", "price": 100, "category": "Stationery", "in_stock": True},

    # 1.Add 3 More Products
    {"id": 5, "name": "Laptop Stand", "price": 1500, "category": "Accessories", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 4500, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 2200, "category": "Electronics", "in_stock": True}
]

@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }

# 2.Add a Category Filter Endpoint
@app.get("/products/category/{category_name}")
def get_products_by_category(category_name: str):
    
    filtered_products = [
        product for product in products 
        if product["category"].lower() == category_name.lower()
    ]

    if not filtered_products:
        return {"error": "No products found in this category"}

    return {
        "category": category_name,
        "products": filtered_products
    }

# 3.Show Only In-Stock Products
@app.get("/products/instock")
def get_instock_products():

    instock_products = [
        product for product in products
        if product["in_stock"] == True
    ]

    return {
        "in_stock_products": instock_products,
        "count": len(instock_products)
    }

# 4.Build a Store Info Endpoint
@app.get("/store/summary")
def store_summary():

    total_products = len(products)

    in_stock_count = len([p for p in products if p["in_stock"]])

    out_of_stock_count = total_products - in_stock_count

    categories = list(set([p["category"] for p in products]))

    return {
        "store_name": "My E-commerce Store",
        "total_products": total_products,
        "in_stock": in_stock_count,
        "out_of_stock": out_of_stock_count,
        "categories": categories
    }

# 5.Search Products by Name
@app.get("/products/search/{keyword}")
def search_products(keyword: str):

    matched_products = [
        product for product in products
        if keyword.lower() in product["name"].lower()
    ]

    if not matched_products:
        return {"message": "No products matched your search"}

    return {
        "matched_products": matched_products,
        "count": len(matched_products)
    }

# Cheapest & Most Expensive Product
@app.get("/products/deals")
def get_product_deals():

    best_deal = min(products, key=lambda x: x["price"])

    premium_pick = max(products, key=lambda x: x["price"])

    return {
        "best_deal": best_deal,
        "premium_pick": premium_pick
    }
