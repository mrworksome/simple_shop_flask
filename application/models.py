from . import db


orders_dishes_association = db.Table(
    "orders_dishes",
    db.Column("dish_id", db.Integer, db.ForeignKey("dishes.d_id")),
    db.Column("order_id", db.Integer, db.ForeignKey("orders.o_id")),
)


class Dish(db.Model):
    __tablename__ = 'dishes'
    d_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=180), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    picture = db.Column(db.String, nullable=False)
    description = db.Column(db.String(length=250), nullable=False)
    category = db.relationship("Category", back_populates="dishes")
    category_id = db.Column(db.Integer, db.ForeignKey("categories.c_id"))
    orders = db.relationship("Order", secondary=orders_dishes_association, back_populates="dishes")


class Order(db.Model):
    __tablename__ = 'orders'
    o_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Boolean)
    final_price = db.Column(db.Float, nullable=False)
    user = db.relationship("User", back_populates="orders")
    buyer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    dishes = db.relationship("Dish", secondary=orders_dishes_association, back_populates="orders")


class Category(db.Model):
    __tablename__ = 'categories'
    c_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=50), nullable=False)
    dishes = db.relationship("Dish", back_populates="category")
