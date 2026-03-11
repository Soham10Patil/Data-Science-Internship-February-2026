from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel, Field
from typing import Optional


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

feedback = []
orders = []

class CustomerFeedback(BaseModel):
    customer_name: str = Field(..., min_length=2)
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=300)

class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=1, le=50)

class BulkOrder(BaseModel):
    company_name: str = Field(..., min_length=2)
    contact_email: str = Field(..., min_length=5)
    items: list[OrderItem] = Field(..., min_items=1)

class Order(BaseModel):
    customer_name: str = Field(..., min_length=2)
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=1)


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


@app.get("/products/filter")
def filter_products(
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    category: Optional[str] = None
):

    filtered = products

    if min_price is not None:
        filtered = [p for p in filtered if p["price"] >= min_price]

    if max_price is not None:
        filtered = [p for p in filtered if p["price"] <= max_price]

    if category is not None:
        filtered = [p for p in filtered if p["category"].lower() == category.lower()]

    return {
        "filtered_products": filtered,
        "count": len(filtered)
    }

@app.get("/products/{product_id}/price")
def get_product_price(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return {
                "name": product["name"],
                "price": product["price"]
            }
    return {"error": "Product not found"}

@app.post("/feedback")
def submit_feedback(data: CustomerFeedback):
    feedback.append(data)

    return {
        "message": "Feedback submitted successfully",
        "feedback": data,
        "total_feedback": len(feedback)
    }

@app.get("/products/summary")
def product_summary():

    total_products = len(products)

    in_stock_count = len([p for p in products if p["in_stock"]])
    out_of_stock_count = total_products - in_stock_count

    most_expensive_product = max(products, key=lambda x: x["price"])
    cheapest_product = min(products, key=lambda x: x["price"])

    categories = list({p["category"] for p in products})

    return {
        "total_products": total_products,
        "in_stock_count": in_stock_count,
        "out_of_stock_count": out_of_stock_count,
        "most_expensive": {
            "name": most_expensive_product["name"],
            "price": most_expensive_product["price"]
        },
        "cheapest": {
            "name": cheapest_product["name"],
            "price": cheapest_product["price"]
        },
        "categories": categories
    }

@app.post("/orders/bulk")
def place_bulk_order(order: BulkOrder):

    confirmed = []
    failed = []
    grand_total = 0

    for item in order.items:

        product = next((p for p in products if p["id"] == item.product_id), None)

        if not product:
            failed.append({
                "product_id": item.product_id,
                "reason": "Product not found"
            })
            continue

        if not product["in_stock"]:
            failed.append({
                "product_id": item.product_id,
                "reason": f'{product["name"]} is out of stock'
            })
            continue

        subtotal = product["price"] * item.quantity
        grand_total += subtotal

        confirmed.append({
            "product": product["name"],
            "qty": item.quantity,
            "subtotal": subtotal
        })

    return {
        "company": order.company_name,
        "confirmed": confirmed,
        "failed": failed,
        "grand_total": grand_total
    }

@app.post("/orders")
def create_order(order: Order):

    order_id = len(orders) + 1

    new_order = {
        "order_id": order_id,
        "customer_name": order.customer_name,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "status": "pending"
    }

    orders.append(new_order)

    return new_order

@app.get("/orders/{order_id}")
def get_order(order_id: int):

    for order in orders:
        if order["order_id"] == order_id:
            return order

    return {"error": "Order not found"}

@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id: int):

    for order in orders:
        if order["order_id"] == order_id:
            order["status"] = "confirmed"
            return order

    return {"error": "Order not found"}
