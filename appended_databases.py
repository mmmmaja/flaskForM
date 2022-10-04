from base import db
from databases import Deliverer, Customer


deliverers = [
    Deliverer(phone_number="1234567", postal_code_id=1, occupied=False)
]


customers = [
    Customer(username="marian", password="pass", phone_number="2345678", postal_code_id=1, point_number=0, used_discount=False)
]
# TODO Discount


for deliverer in deliverers:
    db.session.add(deliverer)
for customer in customers:
    db.session.add(customer)


db.session.commit()

