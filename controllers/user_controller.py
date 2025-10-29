from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from yourapp.models.user import User

user_bp = Blueprint('user_ctrl', __name__, url_prefix='/user', template_folder='templates/users')

@user_bp.route('/profile')
@login_required 
def profile():
    return render_template('users/profile.html', title='Perfil', user=current_user)

