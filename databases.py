from base import db


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
    username = db.Column(db.String(100), unique = True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
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


def create_pizza(name, ingredient_list):
    pizza = Pizza(name=name)
    db.session.add(pizza)
    db.session.commit()

    vegetarian = True
    price = 0

    for i in ingredient_list:
        db.session.add(PizzaIngredient(pizza_id=pizza.pizza_id, ingredient_id=ingredient.ingredient_id))
        price += i.price
        if not i.vegetarian:
            vegetarian = False
    pizza.price = price * 1.09 * 1.4
    pizza.vegetarian = vegetarian
    db.session.commit()


mozzarella = Ingredient(name="mozzarella", price=1.2, vegetarian=True)
basil = Ingredient(name="basil", price=1.2, vegetarian=True)
olives = Ingredient(name="olives", price=1.8, vegetarian=True)
mushrooms = Ingredient(name="mushrooms", price=1.2, vegetarian=True)
salami = Ingredient(name="salami", price=2.1, vegetarian=False)
chicken = Ingredient(name="chicken", price=2.3, vegetarian=False)
pepperoni = Ingredient(name="pepperoni", price=2.3, vegetarian=False)
tomato_sauce = Ingredient(name="tomato_sauce", price=0.7, vegetarian=True)
onions = Ingredient(name="onions", price=0.9, vegetarian=True)
spinach = Ingredient(name="spinach", price=0.9, vegetarian=True)
feta = Ingredient(name="feta", price=0.9, vegetarian=True)

ingredients = [
    mozzarella, basil, olives, mushrooms, salami, chicken, pepperoni, tomato_sauce, onions,
    spinach, feta
]

drinks = [
    Drink(name="water", price=2.3),
    Drink(name="white wine", price=5.2),
    Drink(name="red wine", price=6.0),
    Drink(name="orange juice", price=3.5),
    Drink(name="lemonade", price=4.5)
]

desserts = [
    Dessert(name="tiramisu", price=6.6),
    Dessert(name="ice cream", price=4.8),
    Dessert(name="apple pie", price=5.2),
    Dessert(name="waffles", price=5.7),
]

postal_codes = [
    PostalCode(code="123"),
    PostalCode(code="456"),
    PostalCode(code="789"),
    PostalCode(code="098"),
    PostalCode(code="654"),
]

for ingredient in ingredients:
    db.session.add(ingredient)
for drink in drinks:
    db.session.add(drink)
for dessert in desserts:
    db.session.add(dessert)
for postal_code in postal_codes:
    db.session.add(postal_code)

db.session.commit()

pizzas = [
    create_pizza("margherita", [mozzarella, basil, tomato_sauce]),
    create_pizza("greek", [mozzarella, tomato_sauce, olives, spinach, onions, feta]),
    create_pizza("chicken", [mozzarella, tomato_sauce, chicken]),
    create_pizza("onion", [mozzarella, tomato_sauce, onions]),
    create_pizza("mushroom", [mozzarella, tomato_sauce, mushrooms]),
    create_pizza("meat-lovers", [mozzarella, tomato_sauce, chicken, salami, pepperoni]),
    create_pizza("pepperoni", [mozzarella, tomato_sauce, pepperoni]),
    create_pizza("health-nut", [mozzarella, tomato_sauce, basil, olives, mushrooms, onions, spinach]),
    create_pizza("founder's favorite", [mozzarella, tomato_sauce, mushrooms, chicken, basil]),
    create_pizza("diavolo", [mozzarella, tomato_sauce, basil, pepperoni, onions, olives])
]

