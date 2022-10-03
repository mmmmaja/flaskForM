import base
import databases
from base import app, db
from databases import Ingredient, PizzaIngredient, Pizza, Customer
import os
from datetime import timedelta

from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


@app.route('/')
def index():
    ingredients = Ingredient.query.all()
    return render_template('index.html', students=ingredients)


@app.route('/pizza')
def pizza_page():
    pizzas = Pizza.query.all()
    print(len(pizzas))
    return render_template('pizza_page.html', pizzas=pizzas)


@app.route('/customer', methods=("GET", "POST"))
def customer_page():
    return render_template('customer.html')


@app.route('/login', methods=("GET", "POST"))
def login():

    if request.method == "POST":
        db.session.permanent = True
        customer = get_customer(request.form["username"], request.form["password"])

        if customer is None:
            # Failed to log in
            return render_template("login.html")
        else:
            # Logged in, proceed to order page
            pass
    else:
        # Already logged in
        pass

    return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)


def get_customer(username, password):
    for instance in db.session.query(Customer).where(
            Customer.username == username
    ):
        if instance.password == password:
            return instance
    return None
