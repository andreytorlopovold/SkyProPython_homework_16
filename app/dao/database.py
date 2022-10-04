import json

from sqlalchemy.orm import relationship
import run

db = run.db

# Database models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text(100))
    last_name = db.Column(db.Text(100))
    age = db.Column(db.Integer)
    email = db.Column(db.Text(50))
    role = db.Column(db.Text(50))
    phone = db.Column(db.Text(20))
    offers = relationship('Offer')


class Offer(db.Model):
    __tablename__ = 'offers'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(100))
    description = db.Column(db.Text(200))
    start_date = db.Column(db.Text(50))
    end_date = db.Column(db.Text(50))
    address = db.Column(db.Text(200))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    customer = relationship("User", foreign_keys=[customer_id], backref='customer', lazy=True)
    executor = relationship("User", foreign_keys=[executor_id])


def setup_database():
    db.drop_all()
    db.create_all()

    users = []
    with open('static/data/users.json', 'rt', encoding='utf-8') as file:
        ary = json.load(file)
        for item in ary:
            model = User(**item)
            users.append(model)

    orders = []
    with open('static/data/orders.json', 'rt', encoding='utf-8') as file:
        ary = json.load(file)
        for item in ary:
            model = Order(**item)
            orders.append(model)

    offers = []
    with open('static/data/offers.json', 'rt', encoding='utf-8') as file:
        ary = json.load(file)
        for item in ary:
            model = Offer(**item)
            offers.append(model)

    with db.session.begin():
        db.session.add_all(users)
        db.session.add_all(orders)
        db.session.add_all(offers)
