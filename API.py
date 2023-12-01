
from flask_restful import Resource
from flask import request, jsonify
from classes_table import *



class CategoryAPI(Resource):
    def get(self, id=None):
        if id:
            print("line_12" , id)
            category = session.query(Category).filter(Category.id == id).first()
            if category:
                return {
                    "name": category.category_name,
                    "desc": category.category_description,
                }, 200
            else:
                return {"message": "Category not found"}, 404
        else:
            category = session.query(Category).all()
            if category:
                result = {}
                for cat in category:
                    result[cat.id] = {
                        "name": cat.category_name,
                        "desc": cat.category_description,
                    }

                return result

    def post(self):
        data = request.get_json()
        name = data.get("name")
        category_discription = data.get("desc")
        username = data.get("username")
        password = data.get("password")
        admin = (
            session.query(Customer)
            .filter(Customer.user_name == username)
            .filter(Customer.password == password)
            .first()
        )
        if admin :
            add_category = Category(category_name=name, category_description=category_discription)
            session.add(add_category)
            session.commit()
            return {"message": "Category created successfully"}, 201
        else:
            return {"message": "Admin not found"}, 404

    def put(self, id):
        category = session.query(Category).filter(Category.id == id).first()
        data = request.get_json()
        name = data.get("name")
        Category_discription = data.get("disc")
        username = data.get("username")
        password = data.get("password")
        admin = (
            session.query(Customer)
            .filter(Customer.user_name == username)
            .filter(Customer.password == password)
            .first()
        )
        if admin :
            if category:
                category.name = name
                session.commit()
                return {"message": "Category name changed"}, 201
            else:
                return {"message": "Category not found"}, 404
        else:
            return {"message": "Not authorized"}

    def delete(self, id):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        admin = (
            session.query(Customer)
            .filter(Customer.user_name == username)
            .filter(Customer.password == password)
            .first()
        )
        if admin :
            try:
                session.query(Category).filter(Category.id == id).delete()
                session.flush()
                session.commit()
                return {"message": "Category deleted"}, 201
            except:
                return {"message": "Category not found"}, 404
        else:
            return {"message": "Not authorized"}


class ProductAPI(Resource):

    def get(self, id=None):
        if id:
            product = session.query(Products).filter(Products.id == id).first()
            # product = session.query(Products).filter(Products.id == product_id).first()

            if product:
                return {
                    "name": product.product_name,
                    "image": "http://127.0.0.1:5000/static/assets/products/"
                    + product.product_image,
                    "quantity": product.product_quantity,
                    "price": product.product_price,
                    "cat": product.category_id,
                }, 200
            else:
                return {"message": "product not found"}, 404
        else:
            product = session.query(Products).all()
            if product:
                result = dict()
                for pro in product:
                    result[pro.id] = {
                        "name": pro.product_name,
                        "image": "http://127.0.0.1:5000/static/assets/products/"
                        + pro.product_image,
                        "quantity": pro.product_quantity,
                        "price": pro.product_price,
                        "cat": pro.category_id
                    }
                return result

    def post(self):
        session.flush()
        data = request.get_json()
        name = data.get("name")
        username = data.get("username")
        password = data.get("password")
        image = "/static/temp.jpg"
        quantity = data.get("quantity")
        price = data.get("price")
        category = data.get("category")
        best_before = data.get("best_before")
        category_id = data.get("cat")
        description = data.get("desc") 
        # admin = (
        #     session.query(Customer).filter(Customer.user_name == username).filter(Customer.password == password).first()
        # )
        # if admin :
        if username == "admin" and password == "admin":
            add_product = Products(
                product_name=name, product_image=image, product_quantity=quantity, product_price=price, category_id=category_id, best_before=best_before,product_description=description
            )
            session.add(add_product)
            session.commit()
            return {"message": "product created successfully"}, 201
        else:
            return {"message": "Admin not found"}, 404

    def put(self, id):
        product = Products.query.filter_by(id=id).first()
        data = request.get_json()
        name = data.get("name")
        username = data.get("username")
        password = data.get("password")
        image = "/static/temp.jpg"
        quantity = data.get("quantity")
        price = data.get("price")
        category = data.get("category")
        category_id = data.get("cat")
        description = data.get("desc")
        admin = (
            session.query(Customer)
            .filter(Customer.user_name == username)
            .filter(Customer.password == password)
            .first()
        )
        if admin :
            if product:
                product.name=name
                product.image=image
                product.quantity=quantity
                product.price=price
                product.category=category 
                product.category_id=category_id 
                product.description=description
                session.flush()
                session.commit()
                return {"message": "product name changed"}, 201
            else:
                return {"message": "product not found"}, 404
        else:
            return {"message": "Not authorized"}

    def delete(self, id):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        
        if username=='admin' and password=='admin'  :
            try:
                session.query(Products).filter_by(id=id).delete()
                session.flush()
                session.commit()
                return {"message": "product deleted"}, 201
            except:
                return {"message": "product not found"}, 404
        else:
            return {"message": "Not authorized"}