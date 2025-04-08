from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson.objectid import ObjectId


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": "GET,POST,DELETE,OPTIONS"}})

app.config["MONGO_URI"] = "mongodb+srv://rinat:rinat1212@cluster0.ja5xn.mongodb.net/super-market?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    users_collection = mongo.db.provides
    user = users_collection.find_one({
        "name": username,
        "password": password
    })

    if user:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "redirect": True})

@app.route('/regist', methods=['POST'])
def regist():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')
    company = data.get('company')
    phone = data.get('phone')
    representative = data.get('representative')
    products = data.get('products')

    providers_collection = mongo.db.provides
    providers_collection.insert_one({
        "name": name,
        "password": password,
        "company": company,
        "phone": phone,
        "representative": representative,
        "products": products,
    })

    return jsonify({"success": True})

@app.route('/get_suppliers', methods=['GET'])
def get_suppliers():
    providers_collection = mongo.db.provides
    all_suppliers = providers_collection.find()

    result = {}
    for supplier in all_suppliers:
        name = supplier.get("company", "ללא שם")
        products = supplier.get("products", [])
        result[name] = products

    return jsonify(result)


@app.route('/save_order', methods=['POST'])
def save_order():
    data = request.json
    supplier = data.get('supplier')
    products = data.get('products')

    orders_collection = mongo.db.orders
    orders_collection.insert_one({
        "supplier": supplier,
        "products": products,
        "status": "ממתין לאישור"
    })

    return jsonify({"success": True})


@app.route('/get_orders', methods=['GET'])
def get_orders():
    orders_collection = mongo.db.orders
    all_orders = orders_collection.find()

    result = []
    for order in all_orders:
        result.append({
            "_id": str(order["_id"]),
            "supplier": order.get("supplier", "ללא ספק"),
            "products": order.get("products", []),
            "status": order.get("status", "לא ידוע")
        })

    return jsonify(result)


from flask import jsonify, request


@app.route('/get_pending_orders', methods=['GET'])
def get_pending_orders():

    supplier_name = str(request.args.get('supplier')).strip()

    providers_collection = mongo.db.provides
    provider1 = providers_collection.find_one({"name": supplier_name})

    company_name = provider1.get("company", "ללא חברה") if provider1 else "ללא חברה"

    query = {"status": "ממתין לאישור", "supplier": company_name}
    orders_collection = mongo.db.orders
    pending_orders = orders_collection.find(query)

    pending_orders_list = list(pending_orders)

    if len(pending_orders_list) == 0:
        print("לא נמצאו הזמנות תואמות!")
        return jsonify({"message": "לא נמצאו הזמנות עבור ספק זה."})


    result = {}
    for order in pending_orders_list:
        result[str(order["_id"])] = {
            "supplier": order.get("supplier", "ללא ספק"),
            "_id": str(order["_id"]),
            "products": order.get("products", []),
            "status": order.get("status", "לא ידוע")
        }

    return jsonify(result)


@app.route('/approve_order', methods=['POST'])
def approve_order():
    data = request.get_json()
    order_id = data.get('order_id')

    orders_collection = mongo.db.orders
    orders_collection.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": "מאושר"}}
    )

    return jsonify({"success": True})


@app.route('/delete_order/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    orders_collection = mongo.db.orders
    result = orders_collection.delete_one({"_id": ObjectId(order_id)})

    if result.deleted_count > 0:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False}), 404




if __name__ == '__main__':
    app.run(debug=True)
