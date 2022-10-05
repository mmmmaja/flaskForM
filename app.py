import werkzeug
from flask import request, render_template, redirect, url_for
from base import app, db
from databases import Pizza, all_ingredients, Order, get_customer_ID, all_products
from order_methods import detect_action
from order_methods import find_deliverer, get_order_details

# TODO
# figure out how to store current user in session -> loginManager(?)
ORDER_ID = None


@app.route('/order_details', methods=("GET", "POST"))
def order_details():

    return render_template(
        "order_details.html",
        products=get_order_details(ORDER_ID)[0],
        price=get_order_details(ORDER_ID)[1],
        valid=get_order_details(ORDER_ID)[2],
        discount=get_order_details(ORDER_ID)[3]
    )


@app.route('/finalize', methods=("GET", "POST"))
def finalize():
    name1 = request.form.get('discount')
    print(name1)
    value = request.form.getlist('discount')
    print(value)
    return render_template("finalize_order.html")


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
        name1 = request.form.get('discount')
        print(name1)
        value = request.form.getlist('discount')
        print(value)
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

