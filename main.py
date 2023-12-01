from flask import Flask, render_template, request, redirect, url_for, session , flash
from classes_table import Customer, Products , Category , Cart 
import classes_table
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user 
from wtforms.validators import ValidationError
from flask_restful import Resource, Api
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt


# current_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['max_content_length'] = 16 * 1024 * 1024
app.secret_key = os.urandom(24)

app.config['upload_folder'] = 'static'

@app.route('/')
@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        valid = classes_table.session.query(Customer).filter_by(user_name=username, password=password).first()
        if valid:
            session['user'] = valid.id
            return redirect(url_for('products'))
        else:
            flash('Invalid username or password')
    return render_template('login_twin.html')


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "admin" and password == "admin":
            session['admin'] = username 
            return redirect(url_for('home_admin'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('user_login'))
    return render_template('login_twin.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        address = request.form['address']
        phone = request.form['phone']

        def valid_username(self, username):
            excisting_user = classes_table.session.query(Customer).filter_by(user_name=username).first()
            if excisting_user:
                raise ValidationError('Username already exists')
            else:
                return True

        if valid_username:
            customer = Customer(user_name=username, password=password, email=email, address=address, phone=phone)
            classes_table.session.add(customer)
            classes_table.session.commit()
        return redirect(url_for('user_login'))
    return render_template('register.html')


@app.route('/home_admin', methods=['GET', 'POST'])
def home_admin():
    if "admin" in session:
        products=classes_table.session.query(Products).order_by(Products.product_quantity.asc()).limit(5)
        if request.method == 'POST':
            # accessing first 5 elements of the list
            print(products,'====================')	
            return render_template('home_admin.html', products=products)
        else:
            return render_template('home_admin.html', products=products)
    else:
        return redirect(url_for('admin_login'))
        

@app.route('/products')
def products():
    if "user" in session:
        if request.method == 'POST':
            quantity = request.form['quantity']
            product_price = request.form['product_price']  
            product_name = request.form['product_name']
            userId = current_user.id
            total_price = request.form['total_price']
            ca_rt=Cart(userId,product_name,product_price,quantity,total_price)
            classes_table.session.add(ca_rt)
            classes_table.session.commit()
        products = classes_table.session.query(Products).all()
        categories = classes_table.session.query(Category).all()
        return render_template('products2.html', products=products , categories=categories) 


@app.route('/adminproducts')
def admin_products():
    if "admin" in session:
        products = classes_table.session.query(Products).all()
        categories = classes_table.session.query(Category).all()
        print(products)
        return render_template('admin_products.html', products=products , categories=categories)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admincategories')
def admin_categories():
    if "admin" in session:
        categories = classes_table.session.query(Category).all()
        return render_template('admincategories.html', categories=categories,)#flag = True
    else:
        return redirect(url_for('admin_login'))


@app.route('/admincategories/add', methods=['GET', 'POST'])
def add_categories():
    if "admin" in session:
        if request.method == 'POST':
            category_name = request.form['category_name']
            category_description = request.form['category_description']
            category = Category(category_name=category_name, category_description=category_description)
            classes_table.session.add(category)
            classes_table.session.commit()
            return redirect(url_for('admin_categories'))
        else:
            return render_template('admincategories.html')
    else:
        return redirect(url_for('admin_login'))


@app.route('/admincategories/delete/<int:id>', methods=['GET', 'POST'])
def delete_categories(id):
    if "admin" in session:
        # delete using api
        if request.method == 'GET':
            category = classes_table.session.query(Category).filter(Category.id==id).delete()
            classes_table.session.commit()
            return redirect(url_for('admin_categories'))
        else:
            return redirect(url_for('admin_categories'))
    else:
        return redirect(url_for('admin_login'))


@app.route('/admincategories/edit/<int:id>', methods=['GET', 'POST'])
def edit_categories(id):
    if "admin" in session:
        category = classes_table.session.query(Category).filter_by(id=id).first()
        if request.method == 'POST':
            category.category_name = request.form['category_name']
            category.category_description = request.form['category_description']
            classes_table.session.commit()
            return redirect(url_for('admin_categories'))
        return render_template('editcategory.html', category=category)
    else:
        # return redirect(url_for('admin_categories'))
        return redirect(url_for('admin_login'))
    
    
@app.route('/adminproducts/add', methods=['GET', 'POST'])
def add_products():
    if "admin" in session:
        if request.method == 'POST':
            product_name = request.form['product_name']
            product_price = request.form['product_price']
            product_quantity = request.form['product_quantity']
            product_description = request.form['product_description']
            category_id = request.form['category']
            best_before = request.form['best_before']
            product_image = request.files['product_image']
            def allowed_file(filename):
                return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}
            if product_image and allowed_file(product_image.filename):
                image_filename = secure_filename(product_image.filename)
                # image_path = os.path.join(app.config['templates/static/'], image_filename)
                # print(image_filename, "==========================================")
                image_path = os.path.join(app.config['upload_folder'], image_filename)
                product_image.save(image_path)
            product = Products(product_name=product_name, product_price=product_price, product_quantity=product_quantity, product_description=product_description, product_image=image_filename, category_id=category_id, best_before=best_before)
            classes_table.session.add(product)
            classes_table.session.commit()
            return redirect(url_for('admin_products'))
        elif request.method == 'GET':
            categories = classes_table.session.query(Category).all()
            return render_template('admin_products.html', categories=categories)
    else:
        return redirect(url_for('admin_login'))
    


@app.route('/adminproducts/delete/<int:id>', methods=['GET', 'POST'])
def delete_products(id):
    if "admin" in session:
        if request.method == 'POST':
            classes_table.session.query(Products).filter_by(id=id).delete()
            classes_table.session.commit()
            return redirect(url_for('admin_products'))
        else:
            return redirect(url_for('admin_products'))
    else:
        return redirect(url_for('admin_login'))


@app.route('/adminproducts/edit/<int:id>', methods=['GET', 'POST'])
def edit_products(id):
    if "admin" in session:
        product = classes_table.session.query(Products).filter(Products.id==id).first()
        if request.method == 'POST':
            product.product_name = request.form['product_name']
            product.product_price = request.form['product_price']
            product.product_quantity = request.form['product_quantity']
            product.product_description = request.form['product_description']
            product_image = request.files['product_image']
            def allowed_file(filename):
                return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}
            if product_image and allowed_file(product_image.filename):
                image_filename = secure_filename(product_image.filename)
                # image_path = os.path.join(app.config['templates/static/'], image_filename)
                # print(image_filename, "==========================================")
                image_path = os.path.join(app.config['upload_folder'], image_filename)
                product_image.save(image_path)
            product.product_image = image_filename
            product.category_id = request.form['category']
            product.best_before = request.form['best_before']
            classes_table.session.commit()
            return redirect(url_for('admin_products'))
        else:
            categories = classes_table.session.query(Category).all()
            return render_template('edit_products.html', product=product, categories=categories)
    else:
        return redirect(url_for('admin_login'))
    

@app.route('/addtocart' , methods=['GET', 'POST'])
def add_to_cart():
    if "user" in session:
        if request.method=="POST":
            quantity = request.form['quantity-input']
            product_name = request.form['product_name']
            userId = session['user']
            created_at = datetime.utcnow()
            ca_rt=Cart(userId, product_name, quantity, created_at)
            classes_table.session.add(ca_rt)
            classes_table.session.commit()
            return redirect(url_for('products'))
        else:
            return render_template('products2.html')
    else:
        return redirect(url_for('user_login'))


@app.route('/adminusers')
def admin_users():
    if "admin" in session:
        users = classes_table.session.query(Customer).all()
        return render_template('users.html', users=users)
    else:
        return redirect(url_for('admin_login'))


@app.route('/cart' , methods=['GET', 'POST'])
def cart():
    if "user" in session:
        if request.method == 'GET':
            userId = session['user']
            cart=classes_table.session.query(Cart).filter(Cart.user_id==userId).all()
            # cart = classes_table.session.query(Cart).filter_by(userId=userId).all()
            return render_template('cart.html', cart=cart)
        # elif request.method == 'POST':
        #     userId = session['user']
        #     cart = classes_table.session.query(Cart).filter_by(userId=userId).all()
        #     Products.product_quantity -= Cart.product_quantity
        #     classes_table.session.commit()
        #     cart.delete()
        #     classes_table.session.commit()
            
    else:
        return redirect(url_for('user_login'))


@app.route('/buy' , methods=['GET', 'POST'])
def buy():
    if "user" in session:
        if request.method == 'POST':
            userId = session['user']
            # cart = classes_table.session.query(Cart).filter_by(userId=userId).all()
            cart=classes_table.session.query(Cart).filter(Cart.user_id==userId).all()
            for item in cart:
                # product = classes_table.session.query(Products).filter_by(product_name=item.product_name).first()
                product = classes_table.session.query(Products).filter(Products.product_name==item.product_name).first()
                product.product_quantity -= item.product_quantity
                classes_table.session.commit()
            cart = classes_table.session.query(Cart).filter_by(user_id=userId).delete()
            classes_table.session.commit()
            return redirect(url_for('products'))
        else:
            return render_template('cart.html')
    else:
        return redirect(url_for('user_login'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('admin', None)
    # return redirect('/user_login')
    return redirect(url_for('user_login'))


@app.route('/summary')
def summary():
    # if 'admin' in session:
        # Sample data
        product = classes_table.session.query(Products).all()
        product_quantity = classes_table.session.query(Products.product_quantity).all()
        x_value = [i.product_name for i in product]
        y_value = [i.product_quantity for i in product]
        # print(x_value )
        # print(y_value)
        # graph size
        plt.figure(figsize=(15, 10))
        sns.set(style="whitegrid")
        sns.barplot(x=x_value, y=y_value)

        # Add a title and labels
        plt.title("Graph of Products and Quantity")
        plt.xlabel("Products")
        plt.ylabel("Quantity")

        # Save the plot as an image
        plt.savefig("static/graph.png")
        
        return render_template('summary.html')

        
# @app.route('search', methods=['GET', 'POST'])
# def search():
#     if request.method == 'POST':
#         search = request.form['search']
#         products = classes_table.session.query(Products).filter(Products.product_name.like(f'%{search}%')).all()
#         return render_template('products2.html', products=products)
#     else:
#         return render_template('products2.html')
    
@app.route('/search' , methods=['GET', 'POST'])
def search():
    if "user" in session:
        if request.method == 'POST':
            search = request.form['search']
        products = classes_table.session.query(Products).filter(Products.product_name.like(f'%{search}%')).all()
        categories = classes_table.session.query(Category).filter(Category.category_name.like(f'%{search}%')).all()
        return render_template('search.html', products=products , categories=categories) 
    else:
        return redirect(url_for('user_login'))



from API import ProductAPI, CategoryAPI     
api=Api(app)
api.add_resource(ProductAPI, '/api/products', '/api/products/<int:id>')
api.add_resource(CategoryAPI, '/api/categories', '/api/categories/<int:id>')



if __name__ == '__main__':
    app.run(debug=True)

    