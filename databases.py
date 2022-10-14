import threading
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
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(100), nullable=False)
    postal_code_id = db.Column(db.Integer, db.ForeignKey('postal_code.postal_code_id'), nullable=False)

    point_number = db.Column(db.Integer, default=0)
    discount_used = db.Column(db.Boolean, default=False)


class Deliverer(db.Model):
    deliverer_id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(100), nullable=False)
    postal_code_id = db.Column(db.Integer, db.ForeignKey('postal_code.postal_code_id'), nullable=False)
    occupied = db.Column(db.Boolean)

    def occupy(self):
        # Set the timer for deliverer: for 30 minutes it will be marked as occupied
        start_time = threading.Timer(30 * 60, self.end_task)
        self.occupied = True
        start_time.start()

    def end_task(self):
        # Delivery finished
        self.occupied = False


class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    deliverer_id = db.Column(db.Integer, db.ForeignKey('deliverer.deliverer_id'), nullable=False)
    order_time = db.Column(db.DateTime)

    price = 0
    products = [[], [], []]
    valid = False
    discount_available = False

    def use_discount_code(self):
        # Lower the current price by when discount code is used
        customer_id = self.customer_id
        _customer = db.session.query(Customer).where(Customer.customer_id == customer_id)[0]
        _customer.discount_used = True
        self.price = self.price * 0.9
        db.session.commit()

    def order_details(self):
        # Sets all additional parameters for the order from the queries
        if self.price != 0:
            return

        # collect price and products
        for pizza_order in db.session.query(PizzaOrder).where(PizzaOrder.order_id == self.order_id):
            _pizza = db.session.query(Pizza).where(Pizza.pizza_id == pizza_order.pizza_id)[0]
            self.price += _pizza.price
            self.products[0].append(_pizza.name)
        for drink_order in db.session.query(DrinkOrder).where(DrinkOrder.order_id == self.order_id):
            _drink = db.session.query(Drink).where(Drink.drink_id == drink_order.drink_id)[0]
            self.products[2].append(_drink.name)
            self.price += _drink.price
        for dessert_order in db.session.query(DessertOrder).where(DessertOrder.order_id == self.order_id):
            _dessert = db.session.query(Dessert).where(Dessert.dessert_id == dessert_order.dessert_id)[0]
            self.products[1].append(_dessert.name)
            self.price += _dessert.price
        self.price = round(self.price, 2)

        # Check if discount is possible
        customer_id = self.customer_id
        _customer = db.session.query(Customer).where(Customer.customer_id == customer_id)[0]
        if _customer.point_number > 10 and not _customer.discount_used:
            self.discount_available = True
        self.valid = len(self.products[0]) > 0


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
    """
    Add new pizza to the databases with all the ingredient dependencies
    :param name: name of the pizza
    :param ingredient_list: list of the ingredient objects for this pizza
    :return: None
    """
    _pizza = Pizza(name=name)
    db.session.add(_pizza)
    db.session.commit()

    vegetarian = True
    price = 0

    for i in ingredient_list:
        db.session.add(PizzaIngredient(pizza_id=_pizza.pizza_id, ingredient_id=i.ingredient_id))
        price += i.price
        if not i.vegetarian:
            vegetarian = False
    _pizza.price = round(price * 1.09 * 1.4, 2)
    _pizza.vegetarian = vegetarian
    db.session.commit()


# Add ingredients to the session
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
    mozzarella, basil, olives, mushrooms, salami, chicken, pepperoni, tomato_sauce, onions, spinach, feta
]
for ingredient in ingredients:
    db.session.add(ingredient)

# ADD DRINKS
db.session.add(Drink(name="water", price=2.3))
db.session.add(Drink(name="cappuccino", price=4.1))
db.session.add(Drink(name="white wine", price=5.2))
db.session.add(Drink(name="red wine", price=6.0))
db.session.add(Drink(name="red wine", price=6.0))
db.session.add(Drink(name="orange juice", price=3.5))
db.session.add(Drink(name="lemonade", price=4.5))


# ADD DESSERTS
db.session.add(Dessert(name="tiramisu", price=6.6))
db.session.add(Dessert(name="ice cream", price=4.8))
db.session.add(Dessert(name="apple pie", price=5.2))
db.session.add(Dessert(name="waffles", price=5.7))
db.session.add(Dessert(name="cheese cake", price=6.1))
db.session.add(Dessert(name="strawberry sorbet", price=3.2))


postal_codes = [
    PostalCode(code="123"),
    PostalCode(code="456"),
    PostalCode(code="789"),
    PostalCode(code="098"),
    PostalCode(code="654"),
]

for postal_code in postal_codes:
    db.session.add(postal_code)

db.session.commit()

deliverers = [
    Deliverer(phone_number="1231456", postal_code_id=postal_codes[0].postal_code_id),
    Deliverer(phone_number="123DS53", postal_code_id=postal_codes[0].postal_code_id),
    Deliverer(phone_number="838385", postal_code_id=postal_codes[1].postal_code_id),
    Deliverer(phone_number="123553", postal_code_id=postal_codes[1].postal_code_id),
    Deliverer(phone_number="3363453", postal_code_id=postal_codes[2].postal_code_id)
]

for deliverer in deliverers:
    db.session.add(deliverer)
db.session.commit()


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


customers = [
    Customer(username="maja", password="maja", phone_number="123", postal_code_id=postal_codes[0].postal_code_id),
    Customer(username="random", password="random", phone_number="456", postal_code_id=postal_codes[1].postal_code_id),
    Customer(username="pizza", password="123", phone_number="789", postal_code_id=postal_codes[2].postal_code_id),
    Customer(username="x", password="x", phone_number="09875", postal_code_id=postal_codes[1].postal_code_id),
]
customers[0].point_number = 11
for customer in customers:
    db.session.add(customer)
db.session.commit()


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


def get_customer_ID(username, password):
    for instance in db.session.query(Customer).where(
            Customer.username == username
    ):
        if instance.password == password:
            return instance.customer_id
    return None


all_products = [Pizza.query.all(), Drink.query.all(), Dessert.query.all()]
all_ingredients = []
for pizza in all_products[0]:
    all_ingredients.append(get_ingredients(pizza.pizza_id))

