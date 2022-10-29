from ctypes.wintypes import CHAR
from pickle import FALSE
from pymongo import MongoClient, mongo_client
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response
from bson.objectid import ObjectId
import json
import uuid
import time


client = MongoClient('mongodb://localhost:27017/')

# Choose database
db = client['DsAirlines']

# Choose collections
flights = db['Flights']
users = db['Users']
bookings=db['Booking']

# Initiate Flask App
app = Flask(__name__, template_folder="templates")

#global dictionaries
users_sessions = {}
some_dictionary = {}
products_bought = []
product = {}
returnDict = {}
iteratingDict2={}

#unique id creation
def create_session(email):
    user_uuid = str(uuid.uuid1())
    users_sessions[user_uuid] = (email, time.time())
    some_dictionary[user_uuid] = email
    return user_uuid

#uuid validation
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
        passport = data['passport']
        existing_user = users.find_one(({'name': name}))
        existing_passport= users.find_one(({'passport': passport}))
        existing_email = users.find_one(({'email': email}))
        first =passport[:2]
        rest=passport[2:9]
        print(first,rest,rest.isnumeric(),len(passport),existing_email,existing_user,existing_passport)
        if (len(passport) != 9 or first.isnumeric()==True  or rest.isnumeric()==False):
            return Response("wrong passport type . Passport must be in this form : AB1234567 ", status=400)

        if existing_user is None and existing_passport is None and existing_email is None   and len(passport) == 9 and first.isnumeric()==False  and rest.isnumeric()==True :
            newUser = {
                "name": name,
                "email": email,
                "password": password,
                "passport": passport,
                "category": "user",
                "enabled":"0"
            }
            users.insert_one(newUser)
            return Response(data['name']+" was added to the MongoDB", mimetype='application/json', status=200)
        return Response("User already exists", status=400)
 #define if user is admin or not   
def checkIsAdmin(someUuid):
    isAdmin = False
    for x in users.find():
        if(some_dictionary[someUuid] == x['email']):
            if(x['category'] == 'admin'):
                isAdmin = True
    return isAdmin

# ΕΡΩΤΗΜΑ 2: login στο Σύστημα
@app.route('/login', methods=['POST'])
def login():
    # Request JSON data
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content", status=500, mimetype='application/json')
    if data == None:
        return Response("bad request", status=500, mimetype='application/json')    
    else:
        if not "email" in data :
            name= data['name']
            password = data['password']
            existing_password = users.find_one(({'password': password}))
            existing_name = users.find_one(({'name': name}))
            if  existing_password is not None and existing_name is not None:
                for x in users.find():
                    if x['name']==name:
                        if x['enabled']=="0" :
                            if x['category']=="user":
                                user_uuid = create_session(x['email'])
                                res = {"uuid": user_uuid, "email": x['email']}
                                return Response(json.dumps(res), mimetype='application/json', status=200)
                            elif x['category']=="admin":
                                newpassword = data['newpassword']
                                users.update_one({'name':name},{"$set":{"password":newpassword}})
                                user_uuid = create_session(x['email'])
                                res = {"uuid": user_uuid, "email": x['email']}
                                return Response(json.dumps(res), mimetype='application/json', status=200)
                        elif x['enabled']=="1":
                            return Response("account is currently disabled. activation code is: 123456789011", mimetype='application/json', status=200)
        if not "name" in data :
            
            email = data['email']
            password = data['password']
            existing_username = users.find_one(({'email': email}))
            existing_password = users.find_one(({'password': password}))
            if existing_username is not None and existing_password is not None :
                for x in users.find():
                    if x['email']==email:
                        if x['enabled']=="0" :
                            if x['category']=="user":
                                user_uuid = create_session(email)
                                res = {"uuid": user_uuid, "email": data['email']}
                                return Response(json.dumps(res), mimetype='application/json', status=200)
                            elif x['category']=="admin":
                                newpassword = data['newpassword']
                                users.update_one({'name':name},{"$set":{"password":newpassword}})
                                user_uuid = create_session(email)
                                res = {"uuid": user_uuid, "email": data['email']}
                                return Response(json.dumps(res), mimetype='application/json', status=200)
                        elif x['enabled']=="1":
                            return Response("account is currently disabled. activation code is: 123456789011", mimetype='application/json', status=200)                   
        return Response("Wrong email or password.", mimetype='application/json', status=400)

#ΕΡΩΤΗΜΑ 3: Αναζήτηση Πτήσης
@app.route('/getFlight', methods=['GET'])
def get_Flight():
    # Request JSON data
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content", status=500, mimetype='application/json')
    if data == None:
        return Response("bad request", status=500, mimetype='application/json')
    if not "destination" in data and not "departure" and not "date" in data :
        return Response("Information incomplete", status=500, mimetype="application/json")
    else:
        uuid = request.headers.get('uuid')
        user_uuid = is_session_valid(uuid)
        flightsList = []
        if user_uuid is True:
            isAdmin = checkIsAdmin(uuid)
            isNotAdmin = not isAdmin
            if isNotAdmin:
                destination = data['destination']
                departure = data['departure']
                date = data['date']
                existing_destination = flights.find_one(({'destination': destination}))
                existing_departure = flights.find_one(({'departure': departure}))
                existing_date=flights.find_one(({'date':date}))
                iteratingDict1 = {}
                iteratingDict2 = {}
                if existing_destination is not None and existing_date is not None and existing_departure is not None:
                    for x in flights.find():
                        if x['destination'] == destination and x['departure']==departure and x['date']==date:
                            first_departure = departure[:1]
                            first_destination=destination[:1]
                            day=date[:2]
                            month=date[3:5]
                            year=date[6:10]
                            hour=date[11:13]
                            y=first_departure+first_destination+year+month+day+hour                                                    
                            iteratingDict1 = {"destination": (x['destination']),
                                              "departure": x['departure'],
                                              "date": x['date'],
                                              "price": x['price'],
                                              "tickets": x['tickets'],
                                              "flightId" : y
                                              }
                            flightsList.append(iteratingDict1)
                    if(flightsList.count == 219):
                        return Response("there are no flights on this day ", status=401)
                    return Response(json.dumps(flightsList), mimetype='application/json', status=200) 
                return Response(" does no exist", status=401)
            return Response("user does no exist", status=401)
        return Response("user is not authenticated", status=401, mimetype='application/json')
    
#ΕΡΩΤΗΜΑ 4: Κράτηση Εισιτηρίου
@app.route('/booking', methods=['GET'])
def booking():
    # Request JSON data
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content", status=500, mimetype='application/json')
    if data == None:
        return Response("bad request", status=500, mimetype='application/json')
    else:
        uuid = request.headers.get('uuid')
        user_uuid = is_session_valid(uuid)
        if user_uuid is True:
            isAdmin = checkIsAdmin(uuid)
            isNotAdmin = not isAdmin
            if isNotAdmin:
                flightsList=[]
                id = data['_id']
                name=data['name']
                passport=data['passport']
                credit=data['credit']
                if (len(credit)==16) is True:
                    for x in flights.find():
                        if str(x['_id']) == id:
                            originalStock = int(x['tickets'])
                            maxtickets=220
                            if maxtickets - originalStock >=0 :
                                # Afairw apo to stock
                                y = int(x['tickets']) - 1
                                #dictionary gia na emfanistei sto postman.
                                iteratingDict1 = {
                                                "bookingID":str(y),
                                                "name":name,
                                                "passport":passport,
                                                "destination": (x['destination']),
                                                "departure": x['departure'],
                                                "date": x['date'],
                                                "price": x['price'],
                                                "flightId" : id
                                              }
                                #dictionary gia na apothikeutei se mongodb.
                                iteratingDict2 = {
                                                "_id":str(y),
                                                "name":name,
                                                "passport":passport,
                                                "destination": (x['destination']),
                                                "departure": x['departure'],
                                                "date": x['date'],
                                                "price": x['price'],
                                                "flightId" : id,
                                                "credit":credit
                                              }
                                #vazoume to 1o dictionary se mia lista gia na to emfanisoume.
                                flightsList.append(iteratingDict1)
                                #kanoume update ta eisitiria kai ta apothikeuoume sto 2o dictionary.
                                flights.update_one({'_id':id},{"$set":{"tickets":y}})
                                bookings.insert_one(iteratingDict2)                                                                         
                        else:
                                return "NOT IN STOCK"      
                        return Response(json.dumps(flightsList), status=200, mimetype='application/json')
                    return "NO ID FOUND"
                else:
                    return Response("wrong credit card form")
            return Response("user does no exist", status=401)
    return Response("user is not authenticated", status=401, mimetype='application/json')

#ΕΡΩΤΗΜΑ 5: Εμφάνιση Υπάρχουσας Κράτησης
@app.route('/getBooking', methods=['GET'])
def getBooking():
    # Request JSON data
    flightsList2 = []
    iteratingDict3 = {}
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content", status=500, mimetype='application/json')
    if data == None:
        return Response("bad request", status=500, mimetype='application/json')
    if not "_id" in data :
        return Response("Information incomplete", status=500, mimetype="application/json")
    else:
        uuid = request.headers.get('uuid')
        user_uuid = is_session_valid(uuid)
        if user_uuid is True:
            isAdmin = checkIsAdmin(uuid)
            isNotAdmin = not isAdmin
            if isNotAdmin:
                id = data['_id']
                print(id)
                for x in bookings.find():  
                    if str(x['_id']) == id:
                        print(str(x['_id']))  
                        iteratingDict3 = {
                                    "bookingID":id,
                                    "name":x['name'],
                                    "passport":x['passport'],
                                    "destination": x['destination'],
                                    "departure": x['departure'],
                                    "date": x['date'],
                                    "price": x['price'],
                                    "flightId" : x['flightId']
                                    }
                             
                        flightsList2.append(iteratingDict3)
                             
                        return Response(json.dumps(flightsList2), status=200, mimetype='application/json')
            return Response("id does no exist", status=401)
        return Response("user is not authenticated", status=401, mimetype='application/json')

#ΕΡΩΤΗΜΑ 6: Ακύρωση Κράτησης
@app.route('/deleteBooking', methods=['DELETE'])
def deleteBooking():
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
                z=0
                id = data['_id']
                for x in bookings.find():
                    if (str(x['_id']) == id):
                       msg=x['credit'] + "  money has been returned to this card."
                       bookings.delete_one(x)
                       z=1
                if(z == 0):
                    #an den vrethei id
                    return Response("there is no product with this id ", status=401)        
                return Response(json.dumps(msg), status=200, mimetype='application/json')            
            return Response("user does no exist", status=401)
        return Response("user is not authenticated", status=401, mimetype='application/json')
    
#ΕΡΩΤΗΜΑ 7: Εμφάνιση Όλων Των Κρατήσεων Σε Χρονολογική Σειρά
@app.route('/getBookingDate', methods=['GET'])
def getBookingDate():
    # Request JSON data
    flightsList2 = []
    iteratingDict3 = {}
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content", status=500, mimetype='application/json')
    if data == None:
        return Response("bad request", status=500, mimetype='application/json')
    else:
        uuid = request.headers.get('uuid')
        user_uuid = is_session_valid(uuid)
        if user_uuid is True:
            isAdmin = checkIsAdmin(uuid)
            isNotAdmin = not isAdmin
            if isNotAdmin:
                flightsList2=[]
                #o user dinei ena input, asc gia auksousa desc gia fthinousa . Analogws to input kanei kai to analogo sort.
                sort=data['sort']
                if sort=="asc":
                    #auksousa taksinomisi
                    for x in bookings.find().sort("_id",1):  
                        iteratingDict3 = {
                                        "bookingID":x['_id'],
                                        "name":x['name'],
                                        "passport":x['passport'],
                                        "destination": x['destination'],
                                        "departure": x['departure'],
                                        "date": x['date'],
                                        "price": x['price'],
                                        "flightId" : x['flightId']
                                                }
                        flightsList2.append(iteratingDict3)
                elif sort=="desc":
                    #fthinousa taksinomisi
                    for x in bookings.find().sort("_id",-1):         
                        iteratingDict3 = {
                                        "bookingID":x['_id'],
                                        "name":x['name'],
                                        "passport":x['passport'],
                                        "destination": x['destination'],
                                        "departure": x['departure'],
                                        "date": x['date'],
                                        "price": x['price'],
                                        "flightId" : x['flightId']
                                                }
                        flightsList2.append(iteratingDict3)
                return Response(json.dumps(flightsList2), status=200, mimetype='application/json')
            return Response("user does no exist", status=401)
        return Response("user is not authenticated", status=401, mimetype='application/json')

#ΕΡΩΤΗΜΑ 8: Εμφάνιση Ακριβότερης και Φθινότερης Κράτησης
@app.route('/getBookingPrice', methods=['GET'])
def getBookingPrice():
    # Request JSON data
    flightsList2 = []
    uuid = request.headers.get('uuid')
    user_uuid = is_session_valid(uuid)
    if user_uuid is True:
        isAdmin = checkIsAdmin(uuid)
        isNotAdmin = not isAdmin
        if isNotAdmin:
            flightsList2=[] 
            #min price
            x=bookings.find_one(sort=[("price",-1)])
            #max price             
            y=bookings.find_one(sort=[("price",1)])  
            flightsList2.append(x)
            flightsList2.append(y)
            #copy ta 2 dictionaries stin lista
            return Response(json.dumps(flightsList2), status=200, mimetype='application/json')
        return Response("user does no exist", status=401)
    return Response("user is not authenticated", status=401, mimetype='application/json')

#ΕΡΩΤΗΜΑ 9:Εμφάνιση όλων των κρατήσεων βάσει προορισμού
@app.route('/getBookingDestination', methods=['GET'])
def getBookingDestination():
    # Request JSON data
    flightsList2 = []
    iteratingDict3 = {}
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content", status=500, mimetype='application/json')
    if data == None:
        return Response("bad request", status=500, mimetype='application/json')
    if not "destination" in data :
        return Response("Information incomplete", status=500, mimetype="application/json")
    else:
        uuid = request.headers.get('uuid')
        user_uuid = is_session_valid(uuid)
        if user_uuid is True:
            isAdmin = checkIsAdmin(uuid)
            isNotAdmin = not isAdmin
            if isNotAdmin:
                destination = data['destination']
                for x in bookings.find():  
                    
                        if x['destination'] == destination :  
                            iteratingDict3 = {
                                                "bookingID":x['_id'],
                                                "name":x['name'],
                                                "passport":x['passport'],
                                                "destination": x['destination'],
                                                "departure": x['departure'],
                                                "date": x['date'],
                                                "price": x['price'],
                                                "flightId" : x['flightId']
                                            }
                            flightsList2.append(iteratingDict3)
                        else:
                            return Response("booking with that destination does not exist")
                return Response(json.dumps(flightsList2), status=200, mimetype='application/json')
            return Response("user does no exist", status=401)
        return Response("user is not authenticated", status=401, mimetype='application/json')
    
#ΕΡΩΤΗΜΑ 10: Απενεργοποίηση του λογαριασμού του από την υπηρεσία   
@app.route('/disableAccount', methods=['GET'])
def disableAccount():
    
    uuid = request.headers.get('uuid')
    user_uuid = is_session_valid(uuid)
    if user_uuid is True:
       y= some_dictionary[uuid]
       for x in users.find():
           if x['email']==y:      
            users.update_one({'email':y},{"$set":{"enabled":"1"}})    
    return Response("user is now disabled. The activation code is 123456789011", status=200, mimetype='application/json')   
    
#ΕΡΩΤΗΜΑ 11: Αίτηση ενεργοποίησης λογαριασμού    
@app.route('/enableAccount', methods=['GET'])
def enableAccount():
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content", status=500, mimetype='application/json')
    if data == None:
        return Response("bad request", status=500, mimetype='application/json')
    else:
        uuid = request.headers.get('uuid')
        user_uuid = is_session_valid(uuid)
        if user_uuid is True:
            y= some_dictionary[uuid]
            activation = data['activation']
            if activation=="123456789011":
                for x in users.find():
                    if x['email']==y:
                        users.update_one({'email':y},{"$set":{"enabled":"0"}})
            return Response("user is now enabled. ", status=200, mimetype='application/json')       
    
#ΕΡΩΤΗΜΑ 12: Εισαγωγή νέου διαχειριστή    
@app.route('/createAdmin', methods=['POST'])
def create_admin():
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
     
        existing_user = users.find_one(({'name': name}))
        existing_email = users.find_one(({'email': email}))
     
        if existing_user is None and existing_email is None   :
            newUser = {
                "name": name,
                "email": email,
                "password": password,
                "category": "admin",
                "enabled":"0"
            }
            users.insert_one(newUser)
            return Response(data['name']+" was added to the MongoDB", mimetype='application/json', status=200)
        return Response("User already exists", status=400)
def checkIsAdmin(someUuid):
    isAdmin = False
    for x in users.find():
        if(some_dictionary[someUuid] == x['email']):
            if(x['category'] == 'admin'):
                isAdmin = True
    return isAdmin

#ΕΡΩΤΗΜΑ 13: Δημιουργία πτήσης
@app.route('/addFlights', methods=['PATCH'])
def add_flights():
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
                date = data['date']
                destination = data['destination']
                departure = data['departure']
                price = data['price']
                flightTime = data['flightTime']
                first_departure = departure[:1]
                first_destination=destination[:1]
                day=date[:2]
                month=date[3:5]
                year=date[6:10]
                hour=date[11:13]
                y=first_departure+first_destination+year+month+day+hour
                flights.insert_one(
                    {'date': date, 'destination': destination, 'departure': departure, 'price': price, 'flightTime': flightTime ,'_id':y,'tickets':"220"})
                msg =  "flight was added"
                return Response(msg, status=200, mimetype='application/json')
            return Response("user is not admin", status=401)
        return Response("user is not authenticated", status=401, mimetype='application/json')
    
#ΕΡΩΤΗΜΑ 14: Αλλαγή / Διόρθωση τιμής πτήσης    
@app.route('/updateFlight', methods=['PUT'])
def update_flight():
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
                id = data['_id']
                price = data['price']        
                for x in flights.find():
                    if str(x['_id']) == id:
                        if x['tickets']=="220" and int(price)>0:
                            flights.update_one({'_id':id},{"$set":{"price":price}})
                            msg = "product updated"
                        else:
                            if int(price)<=0:
                                msg = "wrong input price"
                            if x['tickets']!="220":
                               msg = "flight is not empty"
                    else:
                        msg="flight not found"                       
                return Response(msg, status=200, mimetype='application/json')
            return Response("user is not admin", status=401, mimetype='application/json')
        return Response("user is not authenticated", status=401, mimetype='application/json')

#ΕΡΩΤΗΜΑ 15: Διαγραφή πτήσης
@app.route('/deleteFlight', methods=['DELETE'])
def deleteFlight():
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
                for x in flights.find():
                    if(str(x['_id']) == id):
                        msg = x['destination'] + " was deleted."
                        flights.delete_one(x)
                        y = 1
                if(y == 0):
                    return Response("there is no flight with this id ", status=401)
                return Response(msg, status=200, mimetype='application/json')
            return Response("user is not admin")
        return Response("user is not authenticated", status=401, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
