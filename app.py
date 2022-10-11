import datetime
import werkzeug
from flask import request, render_template, redirect, url_for
from base import app, db
from databases import all_ingredients, Order, get_customer_ID, all_products
from order_methods import detect_action, cancel_order, find_deliverer, finalize_order

ORDER_ID = None


def convert_time(time):
    hour = str(time.time().hour)
    if len(hour) == 1:
        hour = "0" + hour
    minute = str(time.time().minute)
    if len(minute) == 1:
        minute = "0" + minute
    return hour + ":" + minute


@app.route('/order_details', methods=("GET", "POST"))
def order_details():
    _order = db.session.query(Order).where(Order.order_id == ORDER_ID)[0]
    _order.order_details()
    if request.method == 'POST':
        try:
            if request.form["discount"] == "Use discount code":
                _order.use_discount_code()
        except werkzeug.exceptions.BadRequestKeyError:
            pass

    return render_template(
        "order_details.html",
        products=_order.products,
        price=_order.price,
        valid=_order.valid,
        discount=_order.discount_available
    )


@app.route('/check_out', methods=("GET", "POST"))
def check_out():
    order_time, error = finalize_order(ORDER_ID), False
    if request.method == 'POST':
        try:
            if request.form["cancel"] == "Cancel Order":
                # check if it's still possible to cancel the order
                if cancel_order(ORDER_ID):
                    return redirect(url_for('login'))
                else:
                    # Time has passed, unable to cancel order
                    error = True
        except werkzeug.exceptions.BadRequestKeyError:
            pass
    return render_template(
        'check_out.html',
        time=convert_time(order_time + datetime.timedelta(seconds=60*40)),
        error=error
    )


@app.route('/order', methods=("GET", "POST"))
def order():
    if request.method == 'POST':
        detect_action(request, ORDER_ID)
    return render_template(
        'order.html',
        products=all_products,
        ingredients=all_ingredients,
        ranges=[len(all_products[0]), len(all_products[1]), len(all_products[2])]
    )


@app.route('/', methods=("GET", "POST"))
def login():
    global ORDER_ID

    if request.method == "POST":

        # Find if customer with given login is in the database
        customer_id = get_customer_ID(request.form["username"], request.form["password"])
        if customer_id is None:
            # No customer found
            return redirect(url_for('login'))
        else:
            # Create new order for current customer
            deliverer_id = find_deliverer(customer_id)
            current_order = Order(customer_id=customer_id, deliverer_id=deliverer_id)
            db.session.add(current_order)
            db.session.commit()
            ORDER_ID = current_order.order_id
            return redirect(url_for('order'))
    else:
        return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)



