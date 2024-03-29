from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120) )
    password = db.Column(db.String(80), nullable=False)
    avatar = db.Column(db.String(220), default='avatar.png')
    wallet = db.Column(db.Float(5), default=0)
    admin = db.Column(db.Integer)

    def __repr__(self):
        return '<Users %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "avatar": self.avatar,
            "wallet": self.wallet,
            "admin": self.admin
        }

class Btnvalues(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20))
    value = db.Column(db.Integer())

    def __repr__(self):
        return '<Btnvalues %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "value": self.value
        }

class WalletTransactions(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    trans_time = db.Column(db.String(220))
    trans_id = db.Column(db.String(220))
    trans_status = db.Column(db.String(220))
    paypal_payer_email = db.Column(db.String(220))
    paypal_payer_name = db.Column(db.String(220))
    paypal_payer_surname = db.Column(db.String(220))
    paypal_payer_id = db.Column(db.String(220))
    old_amount = db.Column(db.Float(5))
    trans_amount = db.Column(db.Float(5))
    new_amount = db.Column(db.Float(5))
    user_id = db.Column(db.Integer())
    user_email = db.Column(db.String(220))

    def __repr__(self):
        return '<WalletTransactions %r>' % self.user_email

    def serialize(self):
        return {
            "id": self.id,
            "trans_time": self.trans_time,
            "trans_id": self.trans_id,
            "trans_status": self.trans_status,
            "paypal_payer_email": self.paypal_payer_email,
            "paypal_payer_name": self.paypal_payer_name,
            "paypal_payer_surname": self.paypal_payer_surname,
            "paypal_payer_id": self.paypal_payer_id,
            "old_amount": self.old_amount,
            "trans_amount": self.trans_amount,
            "new_amount": self.new_amount,
            "user_id": self.user_id,
            "user_email": self.user_email
        }


class Washers(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(220))
    number = db.Column(db.Integer())
    postal = db.Column(db.Integer())
    locationNum = db.Column(db.Integer())
    available = db.Column(db.String(12), default='available')
    cicle_1 = db.Column(db.String(120))
    time_1 = db.Column(db.Integer())
    price_1 = db.Column(db.Float(5))
    cicle_2 = db.Column(db.String(120))
    time_2 = db.Column(db.Integer())
    price_2 = db.Column(db.Float(5))
    cicle_3 = db.Column(db.String(120))
    time_3 = db.Column(db.Integer())
    price_3 = db.Column(db.Float(5))
    cicle_4 = db.Column(db.String(120))
    time_4 = db.Column(db.Integer())
    price_4 = db.Column(db.Float(5))
    cicle_5 = db.Column(db.String(120))
    time_5 = db.Column(db.Integer())
    price_5 = db.Column(db.Float(5))

    def __repr__(self):
        return '<Washers %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "number": self.number,
            "postal": self.postal,
            "locationNum": self.locationNum,
            "available": self.available,
            "cicle_1": self.cicle_1,
            "time_1": self.time_1,
            "price_1": self.price_1,
            "cicle_2": self.cicle_2,
            "time_2": self.time_2,
            "price_2": self.price_2,
            "cicle_3": self.cicle_3,
            "time_3": self.time_3,
            "price_3": self.price_3,
            "cicle_4": self.cicle_4,
            "time_4": self.time_4,
            "price_4": self.price_4,
            "cicle_5": self.cicle_5,
            "time_5": self.time_5,
            "price_5": self.price_5
        }

class Dryers(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(220))
    number = db.Column(db.Integer())
    postal = db.Column(db.Integer())
    locationNum = db.Column(db.Integer())
    available = db.Column(db.String(12), default='available')
    cicle = db.Column(db.String(120))
    time = db.Column(db.Integer())
    price = db.Column(db.Float(5))

    def __repr__(self):
        return '<Dryers %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "number": self.number,
            "postal": self.postal,
            "locationNum": self.locationNum,
            "available": self.available,
            "cicle": self.cicle,
            "time": self.time,
            "price": self.price
        }

class CurrentWashing(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    userID = db.Column(db.Integer())
    userEmail = db.Column(db.String(220))
    machineId = db.Column(db.Integer())
    machineNumber = db.Column(db.Integer())
    locationNum = db.Column(db.Integer())
    price = db.Column(db.Float(5))
    cicle = db.Column(db.String(120))
    time = db.Column(db.Integer())
    start = db.Column(db.BigInteger())
    end = db.Column(db.BigInteger())
    cycleComplete = db.Column(db.String(120))


    def __repr__(self):
        return '<CurrentWashing %r>' % self.locationNum

    def serialize(self):
        return {
            "id": self.id,
            "userID": self.userID,
            "userEmail": self.userEmail,
            "machineId": self.machineId,
            "machineNumber": self.machineNumber,
            "locationNum": self.locationNum,
            "price": self.price,
            "cicle": self.cicle,
            "time": self.time,
            "start": self.start,
            "end": self.end,
            "cycleComplete": self.cycleComplete
        }