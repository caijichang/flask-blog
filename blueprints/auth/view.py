from flask import render_template, Blueprint, url_for, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required
from blueprints.auth.forms import LoginForm
from utils import redirect_back
from blueprints.models import Admin

auth_bp = Blueprint('auth',__name__,url_prefix='/auth')

@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        #return redirect_back(url_for('admin.index'))
        return redirect(url_for('admin.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.first()
        if admin:
            if username == admin.username and admin.check_password(password):
                login_user(admin, remember)
                flash('Welcome back', 'info')
                return redirect_back(url_for('admin.index'))
        else:
            flash('No account', 'warning')
    else:
        flash('No account', 'warning')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect_back(url_for('auth.login'))