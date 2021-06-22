from pymongo import MongoClient, mongo_client
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response
from bson.objectid import ObjectId
import json
import uuid
import time
import copy

client = MongoClient('mongodb://localhost:27017/')

# Choose database
db = client['DSMarkets']

# Choose collections
products = db['Products']
users = db['Users']

# Initiate Flask App
app = Flask(__name__, template_folder="templates")

users_sessions = {}
some_dictionary = {}
products_bought = []
product = {}
returnDict = {}


def create_session(email):
    user_uuid = str(uuid.uuid1())
    users_sessions[user_uuid] = (email, time.time())
    some_dictionary[user_uuid] = email
    return user_uuid


def is_session_valid(user_uuid):

    return user_uuid in users_sessions


# ΕΡΩΤΗΜΑ 1: Δημιουργία χρήστη
@app.route('/createUser', methods=['POST'])
def create_user():
    # Request JSON data
    data = None

    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content", status=500, mimetype='application/json')
    if data == None:
        return Response("bad request", status=500, mimetype='application/json')
    if not "name" in data and not "password" in data and not "email" in data:
        return Response("Information incomplete", status=500, mimetype="application/json")
    else:
        name = data['name']
        email = data['email']
        password = data['password']
        existing_user = users.find_one(({'email': email}))
        if existing_user is None:
            newUser = {
                "name": name,
                "email": email,
                "password": password,
                "category": "user",
                "orderHistory": []
            }
            users.insert_one(newUser)
            return Response(data['name']+" was added to the MongoDB", mimetype='application/json', status=200)
        return Response("User already exists", status=400)

# ΕΡΩΤΗΜΑ 2: Login στο σύστημα


def checkIsAdmin(someUuid):
    isAdmin = False
    for x in users.find():
        if(some_dictionary[someUuid] == x['email']):
            if(x['category'] == 'admin'):
                isAdmin = True
    return isAdmin


@app.route('/login', methods=['POST'])
def login():
    # Request JSON data
    print('login')
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content", status=500, mimetype='application/json')
    if data == None:
        return Response("bad request", status=500, mimetype='application/json')
    if not "email" in data or not "password" in data:
        return Response("Information incomplete", status=500, mimetype="application/json")
    else:
        email = data['email']
        password = data['password']
        existing_username = users.find_one(({'email': email}))
        existing_password = users.find_one(({'password': password}))

        if existing_username is not None and existing_password is not None:
            user_uuid = create_session(email)

            res = {"uuid": user_uuid, "email": data['email']}
            return Response(json.dumps(res), mimetype='application/json', status=200)

        return Response("Wrong email or password.", mimetype='application/json', status=400)

# ΕΡΩΤΗΜΑ 3:  Αναζητηση Προϊόντος


@app.route('/getProduct', methods=['GET'])
def get_Product():
    # Request JSON data

    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content", status=500, mimetype='application/json')
    if data == None:
        return Response("bad request", status=500, mimetype='application/json')
    if not "name" in data and not "category" in data and not "_id" in data:
        return Response("Information incomplete", status=500, mimetype="application/json")
    else:
        uuid = request.headers.get('uuid')
        user_uuid = is_session_valid(uuid)
        productsList = []
        if user_uuid is True:
            isAdmin = checkIsAdmin(uuid)
            isNotAdmin = not isAdmin
            if isNotAdmin:
                name = data['name']
                category = data['category']
                id = data['_id']
                existing_name = products.find_one(({'name': name}))
                existing_category = products.find_one(({'category': category}))
                iteratingDict1 = {}
                iteratingDict2 = {}
                if existing_name is not None:
                    for x in products.find():
                        if x['name'] == name:
                            iteratingDict1 = {"id": str(x['_id']),
                                              "name": x['name'],
                                              "price": x['price'],
                                              "desc": x['desc'],
                                              "category": x['category'],
                                              }
                            productsList.append(iteratingDict1)
                    if(productsList.count == 0):
                        return Response("there are no products ", status=401)
                    return Response(json.dumps(productsList), mimetype='application/json', status=200)
                elif existing_category is not None:
                    for x in products.find():
                        if x['category'] == category:
                            iteratingDict2 = {"id": str(x['_id']),
                                              "name": x['name'],
                                              "price": x['price'],
                                              "desc": x['desc'],
                                              "category": x['category'],
                                              }
                        productsList.append(iteratingDict2)
                    if(productsList.count == 0):
                        return Response("there are no products ", status=401)
                    return Response(json.dumps(productsList), mimetype='application/json', status=200)
                else:
                    for x in products.find():
                        if str(x['_id']) == id:
                            product = {
                                "id": str(x['_id']),
                                "name": x['name'],
                                "price": x['price'],
                                "desc": x['desc'],
                                "category": x['category'],

                            }
                            return Response(json.dumps(product), mimetype='application/json', status=200)
                return Response(" does no exist", status=401)
            return Response("user does no exist", status=401)

        return Response("user is not authenticated", status=401, mimetype='application/json')


# ΕΡΩΤΗΜΑ 4 :Προσθηκη Προϊόντων στο καλάθι
yeahYeah = {}


@app.route('/shoppingCart', methods=['GET'])
def shopping_cart():
    # Request JSON data

    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content", status=500, mimetype='application/json')
    if data == None:
        return Response("bad request", status=500, mimetype='application/json')
    if not "name" in data and not "category" in data and not "stock" and not "price" in data:
        return Response("Information incomplete", status=500, mimetype="application/json")
    else:
        uuid = request.headers.get('uuid')
        user_uuid = is_session_valid(uuid)

        if user_uuid is True:
            isAdmin = checkIsAdmin(uuid)
            isNotAdmin = not isAdmin
            if isNotAdmin:
                productAmount = int(data['amount'])
                id = data['_id']
                for x in products.find():
                    if str(x['_id']) == id:
                        originalStock = int(x['stock'])
                        if productAmount < originalStock:
                            # Afairw apo to stock
                            x['stock'] = int(x['stock']) - productAmount
                            products.save(x)

                            # Vazw sto kalathi
                            if(id in yeahYeah):
                                yeahYeah[id] = yeahYeah[id] + productAmount
                            else:
                                yeahYeah[id] = productAmount

                            returnDict = copy.deepcopy(yeahYeah)
                            returnDict[id] = [x['name'],
                                              yeahYeah[id],
                                              yeahYeah[id] * int(x['price'])]
                            return Response(json.dumps(returnDict), status=200, mimetype='application/json')

                        else:
                            return "NOT IN STOCK"
                return "NO ID FOUND"
            return Response("user does no exist", status=401)

        return Response("user is not authenticated", status=401, mimetype='application/json')

# ΕΡΩΤΗΜΑ 5 : Εμφανιση καλαθιου


@app.route('/getShoppingCart', methods=['GET'])
def getshopping_cart():
    # Request JSON data

    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content", status=500, mimetype='application/json')
    if data == None:
        return Response("bad request", status=500, mimetype='application/json')
    if not "name" in data and not "category" in data and not "stock" and not "price" in data:
        return Response("Information incomplete", status=500, mimetype="application/json")
    else:
        uuid = request.headers.get('uuid')
        user_uuid = is_session_valid(uuid)

        if user_uuid is True:
            isAdmin = checkIsAdmin(uuid)
            isNotAdmin = not isAdmin
            if isNotAdmin:
                rd = {}
                for key in yeahYeah:
                    name = "none"
                    price = 0
                    for x in products.find():
                        if(key == str(x['_id'])):
                            name = x['name']
                            price = int(x['price'])
                    rd[key] = [name, yeahYeah[key], yeahYeah[key] * price]
                return Response(json.dumps(rd), status=200, mimetype='application/json')
            return Response("user does no exist", status=401)
        return Response("user is not authenticated", status=401, mimetype='application/json')

# ΕΡΩΤΗΜΑ 6 : Δαγραφη προϊόντος απο το καλάθι


@app.route('/deleteshoppingCart', methods=['DELETE'])
def deleteshopping_cart():
    # Request JSON data

    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content", status=500, mimetype='application/json')
    if data == None:
        return Response("bad request", status=500, mimetype='application/json')
    if not "_id" in data:
        return Response("Information incomplete", status=500, mimetype="application/json")
    else:
        uuid = request.headers.get('uuid')
        user_uuid = is_session_valid(uuid)

        if user_uuid is True:
            isAdmin = checkIsAdmin(uuid)
            isNotAdmin = not isAdmin
            if isNotAdmin:
                id = data['_id']
                for x in products.find():
                    if str(x['_id']) == id:
                        if(id in yeahYeah):
                            yeahYeah.pop(id)

                            rd = {}
                            for key in yeahYeah:
                                name = "none"
                                price = 0
                                for x in products.find():
                                    if(key == str(x['_id'])):
                                        name = x['name']
                                        price = int(x['price'])
                                rd[key] = [name, yeahYeah[key],
                                           yeahYeah[key] * price]
                            return Response(json.dumps(rd), status=200, mimetype='application/json')

                        else:
                            return Response("user id is not inside the dictionary ", status=401, mimetype='application/json')
            return Response("user does no exist", status=401)
        return Response("user is not authenticated", status=401, mimetype='application/json')

# ΕΡΩΤΗΜΑ 9 : Διαγραφη του λογαριασμου


@app.route('/deleteUser', methods=['DELETE'])
def delete_user():
    # Request JSON data

    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content", status=500, mimetype='application/json')
    if data == None:
        return Response("bad request", status=500, mimetype='application/json')
    if not "email" in data:
        return Response("Information incomplete", status=500, mimetype="application/json")
    else:
        uuid = request.headers.get('uuid')
        user_uuid = is_session_valid(uuid)
        email = data['email']

        y = 0
        if user_uuid is True:
            isAdmin = checkIsAdmin(uuid)
            isNotAdmin = not isAdmin
            if isNotAdmin:
                for x in users.find():
                    if(x['email']) == email:
                        msg = x['name'] + "   deleted."
                        users.delete_one(x)
                        y = 1

                if(y == 0):
                    return Response("there is no user with this id ", status=401)
                return Response(msg, status=200, mimetype='application/json')
            return Response("user is not admin")
        return Response("user is not authenticated", status=401, mimetype='application/json')

# ΕΡΩΤΗΜΑ 10 : εισαγωγη νεου προϊόντος


@app.route('/addProducts', methods=['PATCH'])
def add_products():
    # Request JSON data

    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content", status=500, mimetype='application/json')
    if data == None:
        return Response("bad request", status=500, mimetype='application/json')
    if not "name" in data and not "category" in data and not "stock" and not "price" in data:
        return Response("Information incomplete", status=500, mimetype="application/json")
    else:
        uuid = request.headers.get('uuid')
        user_uuid = is_session_valid(uuid)

        if user_uuid is True:
            isAdmin = checkIsAdmin(uuid)
            isAdminn = isAdmin
            if isAdminn:
                name = data['name']
                category = data['category']
                price = data['price']
                stock = data['stock']
                desc = data['desc']
                products.insert_one(
                    {'name': name, 'category': category, 'price': price, 'stock': stock, 'desc': desc})

                msg = name + " was added"

                return Response(msg, status=200, mimetype='application/json')
            return Response("user is not admin", status=401)
        return Response("user is not authenticated", status=401, mimetype='application/json')

# ΕΡΩΤΗΜΑ 11 : Διαγραφη προϊόντος απο το συστημα


@app.route('/deleteProduct', methods=['DELETE'])
def delete_product():
    # Request JSON data

    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content", status=500, mimetype='application/json')
    if data == None:
        return Response("bad request", status=500, mimetype='application/json')
    if not "_id" in data:
        return Response("Information incomplete", status=500, mimetype="application/json")
    else:
        uuid = request.headers.get('uuid')
        user_uuid = is_session_valid(uuid)
        id = data['_id']

        y = 0
        if user_uuid is True:
            isAdmin = checkIsAdmin(uuid)
            isAdminn = isAdmin
            if isAdminn:
                for x in products.find():
                    if(str(x['_id']) == id):
                        msg = x['name'] + " was deleted."
                        products.delete_one(x)
                        y = 1

                if(y == 0):
                    return Response("there is no product with this id ", status=401)
                return Response(msg, status=200, mimetype='application/json')
            return Response("user is not admin")
        return Response("user is not authenticated", status=401, mimetype='application/json')

# ΕΡΩΤΗΜΑ 12 : Ενημέρωση κάποιου προϊόντος


@app.route('/updateProduct', methods=['PUT'])
def update_product():
    # Request JSON data

    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content", status=500, mimetype='application/json')
    if data == None:
        return Response("bad request", status=500, mimetype='application/json')
    if not "_id" in data:
        return Response("Information incomplete", status=500, mimetype="application/json")
    else:
        uuid = request.headers.get('uuid')
        user_uuid = is_session_valid(uuid)
        if user_uuid is True:
            isAdmin = checkIsAdmin(uuid)
            isAdminn = isAdmin
            if isAdminn:
                name = data['name']
                price = data['price']
                id = data['_id']
                desc = data['desc']
                stock = data['stock']

                for x in products.find():
                    if str(x['_id']) == id:
                        if name is not None:
                            x['name'] = name
                        if price is not None:
                            x['price'] = price
                        if desc is not None:
                            x['desc'] = desc
                        if stock is not None:
                            x['stock'] = stock
                        products.save(x)
                        msg = "product updated"

                return Response(msg, status=200, mimetype='application/json')
            return Response("user is not admin", status=401, mimetype='application/json')
        return Response("user is not authenticated", status=401, mimetype='application/json')


        # Εκτέλεση flask service σε debug mode, στην port 5000.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
