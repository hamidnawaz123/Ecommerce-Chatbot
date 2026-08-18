import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///ecommerce.db")

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50))
    color = Column(String(30))
    price = Column(Float)
    stock = Column(Integer)
    description = Column(Text)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(String(20), primary_key=True)
    customer_email = Column(String(100))
    status = Column(String(50))
    tracking_number = Column(String(50))

def init_db():
    print("Creating tables...")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()

    # Dummy Products
    products = [
        Product(name="Nike Pegasus", category="running shoes", color="black", price=90.0, stock=15, description="Comfortable black running shoes."),
        Product(name="Adidas Cloud", category="running shoes", color="black", price=85.0, stock=22, description="Lightweight black running shoes."),
        Product(name="Puma Runner", category="running shoes", color="white", price=75.0, stock=10, description="White running shoes for everyday use."),
        Product(name="Levis 501", category="jeans", color="blue", price=60.0, stock=50, description="Classic blue denim jeans."),
        Product(name="Gucci T-Shirt", category="shirt", color="white", price=250.0, stock=5, description="Premium white cotton t-shirt.")
    ]
    
    # Dummy Orders
    orders = [
        Order(id="ORD-123", customer_email="test@example.com", status="Shipped", tracking_number="TRK987654321"),
        Order(id="ORD-456", customer_email="hello@example.com", status="Processing", tracking_number=""),
        Order(id="ORD-789", customer_email="user@test.com", status="Delivered", tracking_number="TRK123456789")
    ]
    
    session.add_all(products)
    session.add_all(orders)
    session.commit()
    print("Database populated successfully.")
    session.close()

if __name__ == "__main__":
    init_db()
