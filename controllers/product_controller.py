from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from yourapp.extensions import db
from yourapp.models.product import Product

product_bp = Blueprint('product_ctrl', __name__, url_prefix='/products', template_folder='templates/products')

class ProductForm:
    def __init__(self, data): self.data = data
    def validate_on_submit(self): return request.method == 'POST'
    @property
    def name(self): return self.data.get('name')
    @property
    def description(self): return self.data.get('description')
    @property
    def price(self): 
        try:
            return float(self.data.get('price'))
        except (ValueError, TypeError):
            return 0.0

@product_bp.route('/')
@login_required 
def list_products():
    """Lista todos os produtos do usuário logado."""
    products = Product.query.filter_by(user_id=current_user.id).all()
    return render_template('products/list.html', title='Meus Produtos', products=products)

@product_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_product():
    """Adiciona um novo produto."""
    form = ProductForm(request.form)
    
    if form.validate_on_submit():
        if form.price <= 0:
            flash('O preço deve ser maior que zero.', 'danger')
            return render_template('products/create_product.html', title='Novo Produto', form=form)

        product = Product(
            name=form.name,
            description=form.description,
            price=form.price,
            user_id=current_user.id  
        )
        
        try:
            db.session.add(product)
            db.session.commit()
            flash(f'Produto "{form.name}" adicionado com sucesso!', 'success')
            return redirect(url_for('product_ctrl.list_products'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao adicionar produto: {e}', 'danger')

    return render_template('products/create_product.html', title='Novo Produto', form=form)

def get_product_or_404(product_id):
    product = Product.query.get_or_404(product_id)
    if product.user_id != current_user.id:
        abort(403) 
    return product


@product_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    """Edita um produto existente."""
    product = get_product_or_404(product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.form)
    else:
        form = ProductForm({
            'name': product.name,
            'description': product.description,
            'price': product.price
        })

    if form.validate_on_submit():
        if form.price <= 0:
            flash('O preço deve ser maior que zero.', 'danger')
            return render_template('edit_product.html', title='Editar Produto', form=form, product=product)

        try:
            # Atualiza o objeto do modelo
            product.name = form.name
            product.description = form.description
            product.price = form.price
            
            db.session.commit()
            flash(f'Produto "{form.name}" atualizado com sucesso!', 'success')
            return redirect(url_for('product_ctrl.list_products'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar produto: {e}', 'danger')

    # Para requisição GET ou falha na validação
    return render_template('products/edit_product.html', title='Editar Produto', form=form, product=product)


@product_bp.route('/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    """Exclui um produto."""
    product = get_product_or_404(product_id)
    
    try:
        db.session.delete(product)
        db.session.commit()
        flash(f'Produto "{product.name}" excluído com sucesso.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir produto: {e}', 'danger')
        
    return redirect(url_for('product_ctrl.list_products'))
