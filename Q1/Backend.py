# PoC: Scalable Fashion Data Aggregation Service
# Tech Stack: Python, FastAPI, SQLAlchemy, SQLite (PostgreSQL-ready), Threading

import threading
import requests
import logging
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi.middleware.cors import CORSMiddleware

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')


# FastAPI app initialization
app = FastAPI()

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # You can list multiple origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Allow methods as required
    allow_headers=["*"],  # Allow all headers
)

# --- Database Setup ---
Base = declarative_base()
engine = create_engine("sqlite:///fashion_items.db")  # Switch to PostgreSQL in production
Session = sessionmaker(bind=engine)

class FashionItem(Base):
    __tablename__ = "fashion_items"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    brand = Column(String)
    category = Column(String)
    extra_data = Column(JSON)  # Renamed from 'metadata' to avoid conflict

Base.metadata.create_all(engine)

# --- API Fetch Functions ---
def fetch_dummy_fashion_api():
    try:
        # Sample mock data simulating fashion API response
        response = {
            "items": [
                {"name": "Floral Summer Dress", "brand": "Zara", "category": "Dresses", "details": {"price": 49.99}},
                {"name": "Denim Jacket", "brand": "Levi's", "category": "Outerwear", "details": {"price": 89.99}},
            ]
        }
        return [{
            "name": item.get("name"),
            "brand": item.get("brand"),
            "category": item.get("category"),
            "extra_data": item
        } for item in response["items"]]
    except Exception as e:
        logging.error(f"Error fetching dummy fashion data: {e}")
        return []

def fetch_mock_fashion_api():
    try:
        # Another simulated response for demo purposes
        response = {
            "data": [
                {"name": "Classic White Shirt", "brand": "H&M", "category": "Tops", "details": {"price": 29.99}},
                {"name": "Running Sneakers", "brand": "Nike", "category": "Footwear", "details": {"price": 119.99}},
            ]
        }
        return [{
            "name": item.get("name"),
            "brand": item.get("brand"),
            "category": item.get("category"),
            "extra_data": item
        } for item in response["data"]]
    except Exception as e:
        logging.error(f"Error fetching mock fashion data: {e}")
        return []

# --- Storage Function ---
def store_fashion_items(data):
    session = Session()
    try:
        for item in data:
            session.add(FashionItem(**item))
        session.commit()
        logging.info(f"Stored {len(data)} fashion items.")
    except Exception as e:
        logging.error(f"Error storing fashion data: {e}")
        session.rollback()
    finally:
        session.close()

# --- Parallel Ingestion ---
def run_parallel_ingestion():
    threads = [
        threading.Thread(target=lambda: store_fashion_items(fetch_dummy_fashion_api())),
        threading.Thread(target=lambda: store_fashion_items(fetch_mock_fashion_api())),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

# --- RESTful API Endpoint ---
@app.get("/fashion-items")
def get_fashion_items():
    session = Session()
    items = session.query(FashionItem).all()
    session.close()
    return [
        {
            "id": item.id,
            "name": item.name,
            "brand": item.brand,
            "category": item.category
        } for item in items
    ]

# Trigger data ingestion at startup (for PoC purpose)
if __name__ == "__main__":
    run_parallel_ingestion()
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
