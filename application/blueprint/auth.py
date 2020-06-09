from flask import Blueprint, redirect, request, render_template, flash, url_for
from flask_login import current_user, login_user, login_required, logout_user

from application import db, login_manager
from application.form_login import LoginForm, SignupForm
from application.models import Order
from application.models_user import User
from application.utils_method import get_right_cart_end

auth_bp = Blueprint('auth_bp', __name__,
                    template_folder='templates',
                    static_folder='static')


@auth_bp.route("/login/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth_bp.account'))

    cart_info = get_right_cart_end()

    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(password=form.password.data):
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('auth_bp.account'))
        flash('Invalid username/password combination')
        return redirect(url_for('auth_bp.login'))
    return render_template('login.html',
                           cart_info=cart_info,
                           form=form)


@auth_bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    """
    Sign-up form to create new user accounts.
    GET: Serve sign-up page.
    POST: Validate form, create account, redirect user to main.
    """
    form = SignupForm()
    cart_info = get_right_cart_end()
    if form.validate_on_submit():
        existing_user = User.query.filter(User.email == form.email.data).first()
        if existing_user is None:
            user = User()
            user.username = form.username.data
            user.email = form.email.data
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()  # Create new user
            login_user(user)  # Log in as newly created user
            return redirect(url_for('main_bp.home'))
        flash('A user already exists with that email address.')
    return render_template('signup.html',
                           form=form,
                           cart_info=cart_info
                           )


@auth_bp.route("/account/", methods=["GET"])
@login_required
def account():
    cart_info = get_right_cart_end()
    orders = Order.query.filter(Order.buyer_id == User.id).all()
    return render_template('account.html',
                           cart_info=cart_info,
                           orders=orders
                           )


@auth_bp.route("/logout/")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('main_bp.home'))


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in upon page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))
