# Grocery Store
## create virtual enviroment
```
command: pip install virtualenv
```
```
command: virtualenv <venv_name>
```
- use requirements.txt to install compatible packages
```
command: pip install -r requirment.txt
```
- To run flask server
```
command: python app.py
```

## Description
Flask-shoppee is an application same as e-commerce website to create a direct link between customers & the shop like Amazon, eBay or Walmart etc. It has been designed as 2 parts one is for the customers and other is for admin the store manager .<br><br>
Admin part contains features like creation, updation or deletion of any products as well as categories as per change due to many various varying factors <br>
User part contains many features such as  search, add-to-cart, remove-from-cart, order of any product etc..<br><br>
It consists of 2 APIs for CRUD operations on CATEGORY and PRODUCT
<br><br>
### Technologies used
1. Python (Programming Language)
2. Flask (Web Framework)
3. HTML (Web Page)
4. Bootstrap (Frontend)
5. Flask-SQLAlchemy==3.0.5 (SQLite connection)
6. Jinja2==3.1.2 (HTML injection)
7. SQLAlchemy==2.0.19 (SQLite connection)
8. Werkzeug==2.3.6 (To secure file)
9. Seaborn==0.12.2 (Data Visualization)

## APIs are for CRUD Operations on CATEGORY and PRODUCT
- For CATEGORY
```
GET:- localhost:8080/category_api/{id}
```
```
GET:- localhost:8080/category_api/
```
```
POST:- localhost:8080/category_api/
```
```
PUT:- localhost:8080/category_api/{id}
```
```
DELETE:- localhost:8080/category_api/{id}
```

- For PRODUCT
```
GET:- localhost:8080/product_api/{id}
```
```
GET:- localhost:8080/product_api/
```
```
POST:- localhost:8080/product_api/
```
```
PUT:- localhost:8080/product_api/{id}
```
```
DELETE:- localhost:8080/product_api/{id}
```
# Architecture and Features
└── MAD-1-Project<br>
&nbsp;&nbsp;&nbsp;&nbsp;├── 22f2000957Report.pdf<br>
&nbsp;&nbsp;&nbsp;&nbsp;└── CODE<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── static<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── templates<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── main.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── API.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── api.yaml<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── MAD1.db<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── classes_table.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── requirements.txt<br>

### For testing purpose, use this email_id password:
email_id: admin<br>
password: admin
