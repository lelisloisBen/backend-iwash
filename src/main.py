"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap, sha256
from models import db, Users, Washers, Dryers, CurrentWashing, Btnvalues, WalletTransactions
from flask_jwt_simple import JWTManager, jwt_required, create_jwt


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'dfsh3289349yhoelqwru9g'
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/rasp')
def rasp():
    return 'hello vic'

@app.route('/')
def home():
    return "<div style='text-align: center; background-color: orange'><h1>Backend running...</h1><br/><h3>Welcome back samir</h3><img src='https://media.gettyimages.com/photos/woman-sitting-by-washing-machine-picture-id117852649?s=2048x2048' width='80%' /></div>"

@app.route('/users', methods=['GET'])
def handle_users():

    if request.method == 'GET':
        users = Users.query.all()

        if not users:
            return jsonify({'msg':'User not found'}), 404

        return jsonify( [x.serialize() for x in users] ), 200

    return "Invalid Method", 404

@app.route('/values', methods=['GET', 'POST'])
def get_value():
    if request.method == 'GET':
        values = Btnvalues.query.all()

        if not values:
            return jsonify({'msg':'Value not found'}), 404

        return jsonify( [x.serialize() for x in values] ), 200

    if request.method == 'POST':
        body = request.get_json()
        db.session.add(Btnvalues(
            name = body['name'],
            value = body['value']
        ))
        db.session.commit()
        return jsonify({
            'created': 'success',
            'msg': 'Successfully Created'
        })

    return "Invalid Method", 404

@app.route('/transaction', methods=['POST'])
def add_transaction():
    if request.method == 'POST':
        body = request.get_json()

        updateUser = Users.query.get(body['user_id'])

        if updateUser is None:
            raise APIException('User not found', status_code=404)

        if "new_amount" in body:
            updateUser.wallet = body["new_amount"]
            db.session.add(WalletTransactions(
                trans_time = body['trans_time'],
                trans_id = body['trans_id'],
                trans_status = body['trans_status'],
                paypal_payer_email = body['paypal_payer_email'],
                paypal_payer_name = body['paypal_payer_name'],
                paypal_payer_surname = body['paypal_payer_surname'],
                paypal_payer_id = body['paypal_payer_id'],
                old_amount = body['old_amount'],
                trans_amount = body['trans_amount'],
                new_amount = body['new_amount'],
                user_id = body['user_id'],
                user_email = body['user_email']
            ))

        db.session.commit()
        return jsonify({
            'updated': 'success',
            'msg': 'Successfully Updated'
        })

@app.route('/testing', methods=['POST'])
def test():
    return jsonify({'token':'hello world'})
    return jsonify(request.get_json())

@app.route('/login', methods=['POST'])
def handle_login():

    body = request.get_json()

    user = Users.query.filter_by(email=body['email'], password=sha256(body['password'])).first()

    if not user:
        return 'User not found', 404

    return jsonify({
              'token': create_jwt(identity=1),
              'id': user.id,
              'email': user.email,
              'firstname': user.firstname,
              'lastname': user.lastname,
              'avatar': user.avatar,
              'wallet': user.wallet
              })

@app.route('/addwasher', methods=['POST'])
def washer_add():
    body = request.get_json()
    db.session.add(Washers(
        type = body['type'],
        name = body['name'],
        number = body['number'],
        postal = body['postal'],
        locationNum = body['locationNum'],
        available = body['available'],
        cicle_1 = body['cicle_1'],
        time_1 = body['time_1'],
        price_1 = body['price_1'],
        cicle_2 = body['cicle_2'],
        time_2 = body['time_2'],
        price_2 = body['price_2'],
        cicle_3 = body['cicle_3'],
        time_3 = body['time_3'],
        price_3 = body['price_3'],
        cicle_4 = body['cicle_4'],
        time_4 = body['time_4'],
        price_4 = body['price_4'],
        cicle_5 = body['cicle_5'],
        time_5 = body['time_5'],
        price_5 = body['price_5']
    ))
    db.session.commit()
    return jsonify({
        'added': 'success',
        'msg': 'Successfully Added'
    })

@app.route('/adddryer', methods=['POST','PUT'])
def dryers_add():
    body = request.get_json()

    if request.method == 'POST':
        db.session.add(Dryers(
            type = body['type'],
            name = body['name'],
            number = body['number'],
            postal = body['postal'],
            locationNum = body['locationNum'],
            available = body['available'],
            cicle = body['cicle'],
            time = body['time'],
            price = body['price']
        ))
        db.session.commit()
        return jsonify({
            'added': 'success',
            'msg': 'Successfully Added'
        })

    if request.method == 'PUT':
        updateDryer = Dryers.query.get(body['id'])

        if updateDryer is None:
            raise APIException('Dryer not found', status_code=404)

        if "cicle" in body:
            updateDryer.cicle = body["cicle"],
            updateDryer.available = body["available"],
            updateDryer.locationNum = body["locationNum"],
            updateDryer.name = body["name"],
            updateDryer.number = body["number"],
            updateDryer.postal = body["postal"],
            updateDryer.price = body["price"],
            updateDryer.time = body["time"],
            updateDryer.type = body["type"]

            db.session.commit()
            return jsonify({
                'added': 'success',
                'msg': 'Successfully Updated'
            })

    return "Invalid Method, try again", 404


@app.route('/register', methods=['POST'])
def handle_register():

    body = request.get_json()

    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'firstname' not in body and 'lastname' not in body:
        raise APIException("You need to specify the first name and last name", status_code=400)
    if 'password' not in body and 'email' not in body:
        raise APIException("You need to specify the password and email", status_code=400)
    if 'firstname' not in body:
        raise APIException('You need to specify the first name', status_code=400)
    if 'lastname' not in body:
        raise APIException('You need to specify the last name', status_code=400)
    if 'password' not in body:
        raise APIException('You need to specify the password', status_code=400)
    if 'email' not in body:
        raise APIException('You need to specify the email', status_code=400)



    db.session.add(Users(
        email = body['email'],
        firstname = body['firstname'],
        lastname = body['lastname'],
        password = sha256(body['password'])
    ))
    db.session.commit()

    return jsonify({
        'register': 'success',
        'msg': 'Successfully Registered'
    })

@app.route('/washers', methods=['GET'])
def get_washers():
    if request.method == 'GET':
        getWashers = Washers.query.all()
        if not getWashers:
            return jsonify({'msg':'Washers not found'}), 404

        return jsonify( [x.serialize() for x in getWashers] ), 200

    return "Invalid Method", 404


@app.route('/dryers', methods=['GET'])
def get_dryers():
    if request.method == 'GET':
        getDryers = Dryers.query.all()
        if not getDryers:
            return jsonify({'msg':'Dryers not found'}), 404

        return jsonify( [x.serialize() for x in getDryers] ), 200

    return "Invalid Method", 404

@app.route('/start_washing', methods=['POST'])
def start_wash():
    if request.method == 'POST':

        body = request.get_json()

        db.session.add(CurrentWashing(
            userID = body['userID'],
            userEmail = body['userEmail'],
            machineId = body['machineId'],
            machineNumber = body['machineNumber'],
            locationNum = body['locationNum'],
            price = body['price'],
            cicle = body['cicle'],
            time = body['time'],
            start = body['start_at'],
            end = body['end_at'],
            cycleComplete = body['cycleComplete']
        ))

        updateWallet = Users.query.get(body['userID'])
        updateWallet.wallet = body['new_wallet']

        db.session.commit()

        return jsonify({
            'washing': 'success',
            'msg': 'The washing Machine started'
        })

    return "Invalid Method", 404

@app.route('/user_wash', methods=['POST'])
def get_user_current_wash():
    body = request.get_json()
    if request.method == 'POST':

        getWashing = CurrentWashing.query.filter_by(userID=body['user_id'], userEmail=body['user_email'], cycleComplete='no')
        if not getWashing:
            return jsonify({'msg':'No washing in pregress'}), 404

        return jsonify( [x.serialize() for x in getWashing] ), 200

    return "Invalid Method", 404

@app.route('/wash_history', methods=['POST'])
def get_wash_history():
    body = request.get_json()
    if request.method == 'POST':

        getWashing = CurrentWashing.query.filter_by(userID=body['user_id'], userEmail=body['user_email'], cycleComplete='yes')
        if not getWashing:
            return jsonify({'msg':'No washing in pregress'}), 404

        return jsonify( [x.serialize() for x in getWashing] ), 200

    return "Invalid Method", 404

@app.route('/done_washing', methods=['PUT'])
def wash_done():
    body = request.get_json()
    if request.method == 'PUT':
        updateCycle = CurrentWashing.query.get(body['id'])
            
        if "id" in body:
            updateCycle.cycleComplete = 'yes'
            
            db.session.commit()
            return jsonify({
                'updated': 'success',
                'msg': 'Successfully Updated'
                })


    return "Invalid Method", 404

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
