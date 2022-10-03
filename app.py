import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'hazelnoot2022'
app.config['MYSQL_DB'] = 'flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Ingredient(db.Model):
    ingredient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    vegetarian = db.Column(db.Boolean, nullable=False)
    price = db.Column(db.Float, nullable=False)


class Pizza(db.Model):
    pizza_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float)
    vegetarian = db.Column(db.Boolean)


class Drink(db.Model):
    drink_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)


class Dessert(db.Model):
    dessert_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)


class PostalCode(db.Model):
    postal_code_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), nullable=False)


class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(100), nullable=False)
    postal_code_id = db.Column(db.Integer, db.ForeignKey('postal_code.postal_code_id'), nullable=False)

    point_number = db.Column(db.Integer)
    used_discount = db.Column(db.Boolean)


class Deliverer(db.Model):
    deliverer_id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(100), nullable=False)
    postal_code_id = db.Column(db.Integer, db.ForeignKey('postal_code.postal_code_id'), nullable=False)
    occupied = db.Column(db.Boolean)


class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    deliverer_id = db.Column(db.Integer, db.ForeignKey('deliverer.deliverer_id'), nullable=False)


class PizzaIngredient(db.Model):
    pizza_ingredient_id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.pizza_id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.ingredient_id'), nullable=False)


class CustomerOrder(db.Model):
    customer_order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), nullable=False)


class PizzaOrder(db.Model):
    pizza_order_id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.pizza_id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), nullable=False)


class DrinkOrder(db.Model):
    drink_order_id = db.Column(db.Integer, primary_key=True)
    drink_id = db.Column(db.Integer, db.ForeignKey('drink.drink_id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), nullable=False)


class DessertOrder(db.Model):
    dessert_order_id = db.Column(db.Integer, primary_key=True)
    dessert_id = db.Column(db.Integer, db.ForeignKey('dessert.dessert_id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), nullable=False)


db.drop_all()
db.create_all()

mozzarella = Ingredient(name="mozzarella", price=1.2, vegetarian=True)
db.session.add(mozzarella)
db.session.commit()


def create_pizza(ingredients, name):
    pizza = Pizza(name=name)
    db.session.add(pizza)
    db.session.commit()

    vegetarian = True
    price = 0

    for ingredient in ingredients:
        db.session.add(PizzaIngredient(pizza_id=pizza.pizza_id, ingredient_id=ingredient.ingredient_id))
        price += ingredient.price
        if not ingredient.vegetarian:
            vegetarian = False
    pizza.price = price * 1.09 * 1.4
    pizza.vegetarian = vegetarian
    db.session.commit()


create_pizza([mozzarella], "margherita")


@app.route('/')
def index():
    ingredients = Ingredient.query.all()
    return render_template('index.html', students=ingredients)


@app.route('/pizza')
def pizza_page():
    pizzas = Pizza.query.all()
    return render_template('pizza_page.html', pizzas=pizzas)


@app.route('/customer', methods=("GET", "POST"))
def customer_page():
    return render_template('customer.html')


if __name__ == '__main__':
    app.run(debug=True)


def get_ingredients(pizza_id):
    ingredient_array = []
    for instance in db.session.query(PizzaIngredient).where(
            PizzaIngredient.pizza_id == pizza_id
    ):
        ingredients = db.session.query(Ingredient).where(
            instance.ingredient_id == Ingredient.ingredient_id
        )
        for ingredient in ingredients:
            ingredient_array.append(ingredient)
    return ingredient_array
