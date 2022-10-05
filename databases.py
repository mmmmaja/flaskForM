import time

from base import db
import werkzeug



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
        db.session.add(PizzaIngredient(pizza_id=pizza.pizza_id, ingredient_id=i.ingredient_id))
        price += i.price
        if not i.vegetarian:
            vegetarian = False
    pizza.price = round(price * 1.09 * 1.4, 2)
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

deliverers = [
    Deliverer(phone_number="123 456", postal_code_id=postal_codes[0].postal_code_id),
    Deliverer(phone_number="123 453", postal_code_id=postal_codes[0].postal_code_id)
]

for deliverer in deliverers:
    db.session.add(deliverer)
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


def get_ingredients(pizza_id):
    ingredient_list = []
    for instance in db.session.query(PizzaIngredient).where(
            PizzaIngredient.pizza_id == pizza_id
    ):
        for i in db.session.query(Ingredient).where(
             Ingredient.ingredient_id == instance.ingredient_id
        ):
            ingredient_list.append(i)
    return ingredient_list


class SessionOrder:

    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.order = None
        self.time = None
        self.initiate_order()

    def initiate_order(self):
        _deliverer = self.find_deliverer()
        if not _deliverer:
            # no deliverer found at the moment, try to place an order later
            self.time = time.time()
            self.cancel_order()
            print("no deliverer found")
        else:
            print("Deliverer found!")
            self.order = Order(customer_id=self.customer_id, deliverer_id=self.find_deliverer().deliverer_id)
            db.session.add(self.order)
            db.session.commit()

    def add_pizza(self, pizza_id):
        db.session.add(PizzaOrder(pizza_id=pizza_id, order_id=self.order.order_id))
        db.session.commit()

    def add_drink(self, drink_id):
        db.session.add(DrinkOrder(drink_id=drink_id, order_id=self.order.order_id))
        db.session.commit()

    def add_dessert(self, dessert_id):
        db.session.add(DessertOrder(dessert_id=dessert_id, order_id=self.order.order_id))
        db.session.commit()

    def finalize_order(self):
        # Check number of pizzas
        if len(db.session.query(PizzaOrder).where(PizzaOrder.order_id == self.order.order_id)) < 1:
            return False

        self.time = time.time()
        return True

    def cancel_order(self):
        cancel_time = time.time()
        minutes_elapsed = (cancel_time - self.time) / 60
        if minutes_elapsed > 10:
            # Time to cancel the order has passed
            return False
        return True

    def detect_order_action(self, post_request):
        for instance in db.session.query(Pizza):
            try:
                if post_request.form["pizza_" + str(instance.pizza_id)] == "Add to basket":
                    self.add_pizza(instance.pizza_id)
            except werkzeug.exceptions.BadRequestKeyError:
                pass

        for instance in db.session.query(Drink):
            try:
                if post_request.form["drink_" + str(instance.drink_id)] == "Add to basket":
                    self.add_drink(instance.drink_id)
            except werkzeug.exceptions.BadRequestKeyError:
                pass

        for instance in db.session.query(Dessert):
            try:
                if post_request.form["dessert_" + str(instance.dessert_id)] == "Add to basket":
                    self.add_dessert(instance.dessert_id)
            except werkzeug.exceptions.BadRequestKeyError:
                pass

    def find_deliverer(self):
        customer = db.session.query(Customer)\
            .where(Customer.customer_id == self.customer_id)[0]
        for _deliverer in db.session.query(Deliverer)\
                .where(Deliverer.postal_code_id == customer.postal_code_id):
            if not _deliverer.occupied:
                return _deliverer
        return None


ORDER = None
