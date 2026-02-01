from fastapi import FastAPI, Depends
import database_models
from models import Product
from database import session, engine
from sqlalchemy.orm import Session


app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)


@app.get("/")

def greet():
    return "Hello, World!"

products = [
    Product(id=1,name="Laptop", price=999.99, description="A high-performance laptop", quantity=10),
    Product(id=2,name="Smartphone", price=499.99, description="A latest model smartphone", quantity=25),
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()

    for product in products:
        db.add(database_models.Product(**product.model_dump()))

    db.commit()

init_db()

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products

@app.get("/products/{product_id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if product:
        return product
    return {"error": "Product not found"}

@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product
    return product

@app.put("/products")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if not db_product:
        return {"error": "Product not found"}
    for key, value in product.model_dump().items():
        setattr(db_product, key, value)
    db.commit()
    return db_product
        


@app.delete("/products")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if not db_product:
        return {"error": "Product not found"}
    db.delete(db_product)
    db.commit()
    return "product deleted successfully"
        