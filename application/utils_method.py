from flask import session
from pymorphy2 import MorphAnalyzer

from application import db
from application.models import Dish


def get_cart_info(ids):
    cart = []
    for id in ids:
        cart.append(db.session.query(Dish).get(id).price)
    return [len(ids), sum(cart)]


def get_right_cart_end():
    morph = MorphAnalyzer()
    word = morph.parse('блюдо')[0]
    cart = session.get("cart")
    cart_info = [0, 0]
    if cart:
        cart_info = get_cart_info(session['cart'])
        cart_info1 = '{} {}'.format(cart_info[0], word.make_agree_with_number(cart_info[0]).word)
        cart_info[0] = cart_info1
    return cart_info
