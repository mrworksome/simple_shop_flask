from datetime import datetime

from flask import Blueprint, render_template, session, redirect, url_for
from flask_login import login_required, current_user

from application import db
from application.form_order import OrderForm
from application.models import Category, Dish, Order
from application.models_user import User
from application.utils_method import get_right_cart_end

main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates',
                    static_folder='static')


@main_bp.route('/', methods=['GET'])
def home():
    # cook the dict 'dishes_d' for main page
    cart_info = get_right_cart_end()
    dishes_d = dict()
    cats = Category.query.order_by(Category.c_id).all()
    dishes = Dish.query.order_by(Dish.category_id).all()
    for cat in cats:
        dishes_d[cat.title] = []
        for dish in dishes:
            if cat.c_id == dish.category_id:
                dishes_d[cat.title].append(dish)
    return render_template('main.html',
                           dishes_d=dishes_d,
                           cart_info=cart_info)


@main_bp.route("/cart/", methods=['GET', 'POST'])
def cart():
    cart_info = get_right_cart_end()
    cart_session = session.get("cart", [])
    dishes_for_buy = []
    for d in cart_session:
        dishes_for_buy.append(Dish.query.get(d))

    form = OrderForm()
    if form.validate_on_submit():
        dishes_ids = session['cart']
        user = User.query.get(current_user.get_id())
        user.address = form.address.data
        user.name = form.username.data
        order = Order(final_price=form.price.data,
                      date=datetime.today(),
                      buyer_id=user.id)
        for ident in dishes_ids:
            dish = Dish.query.get(ident)
            order.dishes.append(dish)
        db.session.add(order, user)
        db.session.commit()
        session.pop('cart')
        return redirect(url_for('main_bp.ordered'))
    form = OrderForm(price=cart_info[1])
    return render_template('cart.html', cart_info=cart_info, form=form, dishes=dishes_for_buy)


@main_bp.route("/ordered/", methods=["GET"])
def ordered():
    cart_info = ['0 блюд', 0]
    return render_template('ordered.html', cart_info=cart_info)


@main_bp.route("/addtocart/<int:d_id>/")
def add_to_cart(d_id):
    cart = session.get("cart", [])
    cart.append(d_id)
    session['cart'] = cart
    return redirect(url_for('main_bp.cart'))


@main_bp.route("/delfromcart/<int:d_id>/")
def del_from_cart(d_id):
    cart = session.get("cart")
    cart.remove(d_id)
    session['cart'] = cart
    session['cart_del'] = True
    return redirect(url_for('main_bp.cart'))
