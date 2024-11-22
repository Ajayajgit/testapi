from fastapi import FastAPI, HTTPException
import random
from typing import List, Dict
import logging

app = FastAPI()

# Set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock data for the pizza menu
mock_menu = [
    {"id": 1, "name": "Margherita", "size": "Medium", "price": 8.99, "toppings": ["tomato sauce", "mozzarella", "basil"]},
    {"id": 2, "name": "Pepperoni", "size": "Medium", "price": 9.99, "toppings": ["tomato sauce", "mozzarella", "pepperoni"]},
    {"id": 3, "name": "Vegetarian", "size": "Medium", "price": 10.99, "toppings": ["tomato sauce", "mozzarella", "bell peppers", "onions", "mushrooms"]},
    {"id": 4, "name": "Hawaiian", "size": "Medium", "price": 11.99, "toppings": ["tomato sauce", "mozzarella", "ham", "pineapple"]},
    {"id": 5, "name": "BBQ Chicken", "size": "Medium", "price": 12.99, "toppings": ["BBQ sauce", "mozzarella", "grilled chicken", "red onions"]},
    {"id": 6, "name": "Cheese", "size": "Medium", "price": 9.99, "toppings": ["tomato sauce", "mozzarella"]},
    {"id": 7, "name": "Mushroom", "size": "Medium", "price": 10.99, "toppings": ["tomato sauce", "mozzarella", "mushrooms"]},
    {"id": 8, "name": "Spinach and Feta", "size": "Medium", "price": 11.99, "toppings": ["tomato sauce", "mozzarella", "spinach", "feta cheese"]},
    {"id": 9, "name": "Meat Lover's", "size": "Medium", "price": 12.99, "toppings": ["tomato sauce", "mozzarella", "pepperoni", "sausage", "ham", "bacon"]},
    {"id": 10, "name": "Buffalo Chicken", "size": "Medium", "price": 13.99, "toppings": ["Buffalo sauce", "mozzarella", "grilled chicken", "red onions", "blue cheese"]},
]

menu_by_id = {pizza["id"]: pizza for pizza in mock_menu}  # Improving the data
menu_by_name = {pizza["name"].lower(): pizza for pizza in mock_menu}

@app.get("/menu")
async def fetch_menu(name: str):
    logger.info(f"getting pizza with the give name: {name}")
    
    pizza = menu_by_name.get(name.lower())
    if pizza:
        logger.info(f"got the pizza: {pizza['name']}")
        return pizza
    logger.error(f"Pizza '{name}' not found.")
    raise HTTPException(status_code=404, detail=f"Pizza '{name}' not found.")


@app.post("/order")
async def place_order(order: List[Dict[str, int]]):
    logger.info("order received: %s", order)
    
    if not order:
        logger.warning("empty order received.")
        raise HTTPException(status_code=400, detail="Order is not given by the user.")
    
    total_price = 0# initilize price to the value 0
    for item in order:
        pizza_id = item.get("id")
        quantity = item.get("quantity")

        if not pizza_id or not quantity:
            logger.warning(f"Invalid order item: {item}")
            raise HTTPException(status_code=400, detail="Each order should include 'id' and 'quantity'.")

        pizza = menu_by_id.get(pizza_id)#getting the pizza with the id
        if not pizza:
            logger.error(f"Pizza's ID {pizza_id} not found.")
            raise HTTPException(status_code=404, detail=f"Pizza with ID {pizza_id} not found.")
        
        logger.info(f"adding {quantity} x {pizza['name']} to the order.")
        total_price += pizza["price"] * quantity

    order_id = random.randint(11, 50)# this will give random ids for the order
    logger.info(f"order placed successfully with order ID: {order_id}, total price: {total_price}")

    return {"order_id": order_id, "price": round(total_price, 2)}
