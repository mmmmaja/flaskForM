import datetime
from databases import Pizza, Customer, Deliverer, Order, PizzaOrder, Drink, DrinkOrder, DessertOrder, Dessert
import werkzeug
from base import db


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
    order = db.session.query(Order).where(Order.order_id == ORDER_ID)[0]
    if order.order_time is None:
        customer_id = order.customer_id
        customer = db.session.query(Customer).where(Customer.customer_id == customer_id)[0]
        for _ in db.session.query(PizzaOrder).where(PizzaOrder.order_id == ORDER_ID):
            customer.point_number += 1

        order.order_time = datetime.datetime.now()
        deliverer = db.session.query(Deliverer).where(Deliverer.deliverer_id == order.order_id)[0]
        deliverer.occupy()
        db.session.commit()

    return order.order_time


def cancel_order(ORDER_ID):
    order = db.session.query(Order).where(Order.order_id == ORDER_ID)[0]
    time_elapsed = (datetime.datetime.now() - order.order_time).total_seconds() / 60
    if time_elapsed > 5:
        return False
    db.session.delete(order)
    db.session.commit()
    return True
