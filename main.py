from fastapi import FastAPI
from models import Product

app = FastAPI()

@app.get("/")

def greet():
    return "Hello, World!"

products = [
    Product(id=1,name="Laptop", price=999.99, description="A high-performance laptop", quantity=10),
    Product(id=2,name="Smartphone", price=499.99, description="A latest model smartphone", quantity=25),
]

@app.get("/products")
def get_products():
    return products

@app.get("/products/{product_id}")
def get_product_by_id(id: int):
    for product in products:
        if product.id == id:
            return product
    return {"error": "Product not found"}

@app.post("/products")
def add_product(product: Product):
    products.append(product)
    return product

@app.put("/products")
def update_product(id: int, product: Product):
    for i in range(len(products)): 
        if products[i].id == id:
            products[i] = product
            return "product updated successfully"
        
    return {"error": "Product not found"}


@app.delete("/products")
def delete_product(id: int):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return "product deleted successfully"
    return {"error": "Product not found"}