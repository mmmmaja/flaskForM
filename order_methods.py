import datetime

from databases import Pizza, Customer, Deliverer, Order, PizzaIngredient, PizzaOrder, Drink, DrinkOrder, DessertOrder, Dessert
import werkzeug
from base import app, db


def detect_action(_request, ORDER_ID):
    """
    :param _request: POST request from the order page buttons
    :param ORDER_ID: identifier for the current order
    :return: True if all products were picked, and we proceed to order_details page, False otherwise
    """

    for instance in db.session.query(Pizza):
        try:
            if _request.form["pizza_" + str(instance.pizza_id)] == "Add to basket":
                db.session.add(PizzaOrder(pizza_id=instance.pizza_id, order_id=ORDER_ID))
        except werkzeug.exceptions.BadRequestKeyError:
            pass

    for instance in db.session.query(Drink):
        try:
            if _request.form["drink_" + str(instance.drink_id)] == "Add to basket":
                db.session.add(DrinkOrder(drink_id=instance.drink_id, order_id=ORDER_ID))
        except werkzeug.exceptions.BadRequestKeyError:
            pass

    for instance in db.session.query(Dessert):
        try:
            if _request.form["dessert_" + str(instance.dessert_id)] == "Add to basket":
                db.session.add(DessertOrder(dessert_id=instance.dessert_id, order_id=ORDER_ID))
        except werkzeug.exceptions.BadRequestKeyError:
            pass
    db.session.commit()


def find_deliverer(customer_id):
    """
    :param customer_id: ID of the current user
    :return: deliverer that are not busy and that deliver to the addresses with the same postal code as customer's
    """
    customer = db.session.query(Customer).where(Customer.customer_id == customer_id)[0]
    for deliverer in db.session.query(Deliverer).where(Deliverer.postal_code_id == customer.postal_code_id):
        if not deliverer.occupied:
            return deliverer.deliverer_id
    return None


def finalize_order(ORDER_ID):

    pizza_number = len(db.session.query(PizzaOrder).where(PizzaOrder.order_id == ORDER_ID))
    if pizza_number < 1:
        return False

    order = db.session.query(Order).where(Order.order_id == ORDER_ID)[0]
    customer_id = order.customer_id
    customer = db.session.query(Customer).where(Customer.customer_id == customer_id)[0]
    customer.point_number += pizza_number

    order.order_time = datetime.datetime.now()
    return True


def get_order_details(ORDER_ID):
    price, products, valid, discount_available = 0, [[], [], []], False, False

    # collect price and products
    for pizza_order in db.session.query(PizzaOrder).where(PizzaOrder.order_id == ORDER_ID):
        pizza = db.session.query(Pizza).where(Pizza.pizza_id == pizza_order.pizza_id)[0]
        price += pizza.price
        products[0].append(pizza.name)
    for drink_order in db.session.query(DrinkOrder).where(DrinkOrder.order_id == ORDER_ID):
        drink = db.session.query(Drink).where(Drink.drink_id == drink_order.drink_id)[0]
        products[1].append(drink.name)
        price += drink.price
    for dessert_order in db.session.query(DessertOrder).where(DessertOrder.order_id == ORDER_ID):
        dessert = db.session.query(Dessert).where(Dessert.dessert_id == dessert_order.dessert_id)[0]
        products[2].append(dessert.name)
        price += dessert.price
    price = round(price, 2)

    # Check if discount is possible
    order = db.session.query(Order).where(Order.order_id == ORDER_ID)[0]
    customer_id = order.customer_id
    customer = db.session.query(Customer).where(Customer.customer_id == customer_id)[0]
    if customer.point_number > 10 and not customer.discount_used:
        discount_available = True
    valid = len(products[0]) > 0

    return products, price, valid, discount_available
