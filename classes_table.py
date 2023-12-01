#DEFINE CLASSES FOR USER AND ADMIN
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey , BLOB , DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

engine = create_engine('sqlite:///MAD1.db')
Base = declarative_base()

Sessions = sessionmaker()
Sessions.configure(bind=engine)
session = Sessions()


class Customer(Base):
    __tablename__ = 'Customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column('username',String , unique=True, nullable=False)
    email = Column('email',String , nullable=False)
    password = Column('password', String , nullable=False)
    address = Column('address', String , nullable=True)
    phone = Column('phone', String , nullable=True)
    cart = relationship('Cart', backref='customer', lazy=True)


    def __init__(self,user_name,email,password,address,phone):
        self.user_name = user_name
        self.email = email
        self.password = password
        self.address = address
        self.phone = phone

    def __repr__(self):
        return f"Customer('{self.username}','{self.email}')"


class Category(Base):
    def __init__(self,category_name,category_description):
        self.category_name = category_name
        self.category_description = category_description
        self.created_at = datetime.now()

    
    def __repr__(self):
        return f"Category('{self.category_name}','{self.category_description}')"
    
    __tablename__ = 'Category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column('category_name',String , unique=True, nullable=False)
    category_description = Column('category_description',String , nullable=False)
    created_at = Column('created_at',DateTime , nullable=False)

# category1 = Category('category1', 'category1_description')
# category2 = Category('category2', 'category2_description')
# category3 = Category('category3', 'category3_description')

# category1 = session.query(Category).filter_by(category_name='category1').first()
# category2 = session.query(Category).filter_by(category_name='category2').first()
# category3 = session.query(Category).filter_by(category_name='category3').first()

# session.add(category1)
# session.add(category2)
# session.add(category3)
# session.commit()


class Products(Base):
    def __init__(self,product_name,product_price, product_quantity , product_description , product_image, category_id , best_before ,id=None ):
        self.product_name = product_name
        self.product_price = product_price
        self.product_quantity = product_quantity
        self.product_description = product_description
        self.category_id = category_id
        self.best_before = best_before
        self.created_at = datetime.now()
        self.product_image = product_image
    
    def __repr__(self):
        return f"Products('{self.product_name}','{self.product_price}','{self.product_quantity}','{self.product_description}','{self.product_image}')"
    def serialize(self):
        return {
            "id": self.id,
            "product_name": self.product_name,
            "product_price": self.product_price,
            "product_quantity": self.product_quantity,
            "product_description": self.product_description,
            "product_image": self.product_image,
            "best_before": self.best_before,
            "created_at": self.created_at,
            "category_id": self.category_id
        }
    def to_json(self):
        return {
        "id": self.id,
        "product_name": self.product_name,
        "product_price": self.product_price,
        "product_quantity": self.product_quantity,
        "product_description": self.product_description,
        "product_image": self.product_image,
    }
    
    __tablename__ = 'Products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column('product_name',String , unique=True, nullable=False)
    product_price = Column('product_price',Float , nullable=False)
    product_quantity = Column('product_quantity',Integer , nullable=False)
    product_description = Column('product_description',String , nullable=False)
    product_image = Column('product_image', String , nullable=False)
    best_before = Column('best_before', String, nullable=False)
    created_at = Column('created_at', DateTime, nullable=False, default=datetime.utcnow)
    category_id = Column(Integer, ForeignKey('Category.id'), nullable=False)
    category = relationship(Category, backref='products')


# product1 = Products('product1', 100, 10, 'product1_description', 'product1.jpg', 1, 'jan 2024')
# product1.category = category1

# product2 = Products('product2', 200, 20, 'product2_description', 'product2.jpg' , 2, 'Mar 2024')
# product2.category = category2

# product3 = Products('product3', 300, 30, 'product3_description', 'product3.jpg', 3, 'Apr 2024')
# product3.category = category3

# session.add(product1)
# session.add(product2)
# session.add(product3)
# session.commit()





class Cart(Base):
    def __init__(self, user_id ,product_name, product_quantity , created_at, id=None ):
        pro_duct= session.query(Products).filter(Products.product_name == product_name).first()
        self.product_name = product_name
        self.product_id = pro_duct.id
        self.product_price = pro_duct.product_price
        self.product_description = pro_duct.product_description
        self.product_quantity = product_quantity
        self.category_id = pro_duct.category_id
        self.total_price = float(self.product_price) * float(self.product_quantity)
        self.added_at = created_at
        self.user_id = user_id
        # self.user_id = #tba
    
    def __repr__(self):
        return f"Cart('{self.product_name}','{self.product_price}','{self.product_quantity}','{self.product_description}','{self.product_image}')"
    
    __tablename__ = 'Cart'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column('product_name',String , nullable=False)
    product_price = Column('product_price',Float , nullable=False)
    product_quantity = Column('product_quantity',Integer , nullable=False)
    product_description = Column('product_description',String , nullable=False)
    total_price = Column('total_price',Float , nullable=False)
    added_at = Column('created_at',DateTime , nullable=False)
    user_id = Column(Integer, ForeignKey('Customer.id'), nullable=False)
    user = relationship(Customer)
    product_id = Column(Integer, ForeignKey('Products.id'), nullable=False)
    product = relationship(Products)
    category_id = Column(Integer, ForeignKey('Category.id'), nullable=False)
    category = relationship(Category)







    #----------------------------------------------------------------------------------------------------------------
    # product_image = Column('product_image', blob , nullable=False)




# a=datetime.now()
# product1=Products('product1',100,10,'product1_description','product1.jpg',a)
# a=datetime.now()
# product2=Products('product2',200,20,'product2_description','product2.jpg',a)
# a=datetime.now()
# product3=Products('product3',300,30,'product3_description','product3.jpg',a)

# session.add(product1)
# session.add(product2)
# session.add(product3)
# session.commit()



# creating an object of the class
# customer1 = Customer('blue_flame','blue@gmail','123456789')
# session.add(customer1)
# session.commit()

# username='blue_flame'
# pasw='123456789'
# valid = session.query(Customer).filter_by(Customer.password==pasw).all()
# print(valid)
# Assuming you have already defined the Customer class and set up the SQLAlchemy engine and session as shown in the previous code

# new_customer = Customer(user_name='blue_flame', email='blue@gmail.com', password='123456789')
# session.add(new_customer)
# session.commit()


Base.metadata.create_all(engine)
# creating all the tables in the database

# category = session.query(Category).filter(Category.id==2).delete()
# session.commit()