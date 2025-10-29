from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from yourapp.extensions import db
from yourapp.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates/auth')

class LoginForm:
    def __init__(self, data): self.data = data
    def validate_on_submit(self): return request.method == 'POST'
    @property
    def username(self): return self.data.get('username')
    @property
    def password(self): return self.data.get('password')

class RegistrationForm:
    def __init__(self, data): self.data = data
    def validate_on_submit(self): return request.method == 'POST'
    @property
    def username(self): return self.data.get('username')
    @property
    def email(self): return self.data.get('email')
    @property
    def password(self): return self.data.get('password')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user_ctrl.profile')) 
    
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User(username=form.username, email=form.email)
        user.set_password(form.password)
        db.session.add(user)
        db.session.commit()
        flash('Sua conta foi criada! Faça login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Registro')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user_ctrl.profile'))
    
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username).first()
        
        if user and user.check_password(form.password):
            login_user(user, remember=True) 
            next_page = request.args.get('next')
            flash('Login bem-sucedido!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('user_ctrl.profile'))
        else:
            flash('Login inválido. Verifique o usuário e a senha.', 'danger')

    return render_template('auth/login.html', title='Login')

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('auth.login'))

