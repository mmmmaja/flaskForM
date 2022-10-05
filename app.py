from flask import request, render_template, redirect, url_for
from base import app, db
from databases import Pizza, Customer, get_ingredients, SessionOrder
import databases

pizzas = Pizza.query.all()
ingredients = []
for pizza in pizzas:
    ingredients.append(get_ingredients(pizza.pizza_id))


def get_customer(username, password):
    for instance in db.session.query(Customer).where(
            Customer.username == username
    ):
        if instance.password == password:
            return instance
    return None


@app.route('/order', methods=("GET", "POST"))
def order():
    if request.method == 'POST':
        # print(databases.ORDER)
        # databases.ORDER.detect_order_action(request)
        pass

    return render_template('order.html', pizzas=pizzas, ingredients=ingredients, pizza_number=len(pizzas))


@app.route('/new_customer', methods=['GET', 'POST'])
def new_customer():
    return render_template('new_customer.html')


@app.route('/', methods=("GET", "POST"))
def login():
    if request.method == "POST":

        db.session.permanent = True
        customer = get_customer(request.form["username"], request.form["password"])

        if customer is None:
            # Failed to log in

            # FIXME Just temporal things to work with order!
            temp = Customer(username="e", password="", phone_number="", postal_code_id=1)
            db.session.add(temp)
            db.session.commit()
            # databases.ORDER = SessionOrder(temp.customer_id)
            # print("created session order")
            return redirect(url_for('order'))
        else:
            # Logged in, proceed to order page
            pass
    else:
        # Already logged in
        pass

    return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)
