from distutils.command.config import config
from turtle import update
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required, current_user
from . import db 
from .models import products

views = Blueprint('views', __name__)

### home ###
@views.route('/')
def home():
    return render_template("home.html", user=current_user, products = products.query.all()) 

### Shop ###
@views.route('/shop')
def shop():
    return render_template("shop.html", user=current_user, products = products.query.all())

### Product Details ###
@views.route('/product/<int:id>')
def product(id):
    return render_template("product.html", user=current_user, products = products.query.get_or_404(id))

### User Products ###

#View user prodcuts
@views.route('/user-products')
def user_products():
    return render_template("user-products.html", user=current_user, products = products.query.all())

# Add Product
@views.route('/add-product', methods = ['GET', 'POST']) 
def add_product():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['description']: 
            flash('Please enter all the fields', 'error')
        else:   
            name = request.form['name']
            price = request.form['price']
            keywords= request.form['keywords']
            description = request.form['description']
            sold = "not sold"
            user = current_user.id 
            
            product = products(sold=sold, name=name, price=price, keywords=keywords, description=description, user_id=user)
            db.session.add(product)
            db.session.commit()
            
            flash('Product was successfully added') 
            return redirect(url_for('views.user_products'))
    return render_template('add-product.html', user=current_user)

# Edit Product
@views.route('/edit-product/<id>', methods = ['GET', 'POST'])
def edit_product(id):
    update_product = products.query.filter_by(id = id).first() 
    if request.method == 'POST':
        if not request.form['name'] or not request.form['price'] or not request.form['description']: 
            flash('Please enter all the fields', 'error')
        else:
            update_product.name = request.form['name']
            update_product.price = request.form['price']
            update_product.keywords = request.form['keywords'] 
            update_product.description = request.form['description']
            update_product.sold = request.form.get('sold')
            db.session.commit()
            flash('Record was successfully updated') 
            return redirect(url_for('views.user_products'))
    return render_template('edit-product.html', user=current_user, product = update_product)

# Delete Product
@views.route('/delete/<name>') 
def delete(name):
    product = products.query.filter_by(name = name).first() 
    db.session.delete(product)
    db.session.commit()
    return	render_template('user-products.html', products = products.query.all(), user=current_user)

# follow user 
@views.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    user = User.query.filter_by(username= username).first()
    if user is None:
        flash('User {} not found.'.format(username))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('views.shop', products = products.query.all()))
    else:
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('views.shop', products = products.query.all()))

