import werkzeug
from flask import request, render_template, redirect, url_for
from base import app, db
from databases import Pizza, all_ingredients, Order, get_customer_ID
from order_methods import detect_action
from order_methods import find_deliverer, get_order_details

# TODO
# figure out how to store current user in session -> loginManager(?)
ORDER_ID = None


@app.route('/order', methods=("GET", "POST"))
def order():

    if request.method == 'POST':
        # One of the buttons was clicked
        order_finished = detect_action(request, ORDER_ID)
        if order_finished:
            return redirect(url_for('order_details'))

    return render_template(
        'order.html',
        pizzas=Pizza.query.all(),
        ingredients=all_ingredients,
        pizza_number=len(Pizza.query.all())
    )


@app.route('/order_details', methods=("GET", "POST"))
def order_details():

    if request.method == 'POST':
        # Button was clicked, go back to previous page
        try:
            if request.form["back"] == "Back to order":
                return redirect(url_for('order'))
        except werkzeug.exceptions.BadRequestKeyError:
            pass
    return render_template(
        "order_details.html",
        products=get_order_details(ORDER_ID)[0],
        price=get_order_details(ORDER_ID)[1]
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

