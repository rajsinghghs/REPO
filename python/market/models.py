from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin
from datetime import datetime
from pytz import utc
from flask_login import current_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    today_income = db.Column(db.Integer(), nullable=False, default=0)
    yesterday_income = db.Column(db.Integer(), nullable=False, default=0)
    referral_code = db.Column(db.String(), unique=True)
    referred_by = db.Column(db.String())
    referred_bonus = db.Column(db.Float(), default=0)
    recharge_amount = db.Column(db.Integer(), default=0)
    register_time = db.Column(db.DateTime, default=datetime.now)
    refer_code = db.Column(db.Integer(), default='link_id')
    items = db.relationship('Item', backref='owned_user', lazy=True)
    payouts = db.relationship('Payout', backref='owned_payout', lazy=True)

    def update_referred_bonus(self):
        user = current_user
        bonus = user.recharge_amount*0.2
        self.referred_bonus = bonus
        db.session.commit()

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password )


            

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    income = db.Column(db.Integer(), nullable=False, unique=True)
    total_income = db.Column(db.Integer(), nullable=False)
    cycle = db.Column(db.Integer(), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

class Payout(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    ac_name= db.Column(db.String(), nullable=False)
    ac_number = db.Column(db.Integer(), nullable=False)
    ac_ifsc = db.Column(db.String(), nullable=False)
    withdraw = db.Column(db.Integer())
    withdraw_time = db.Column(db.DateTime, default=datetime.now)
    check = db.Column(db.Integer(), db.ForeignKey('user.id'))

class Buyer(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    item_owner = db.Column(db.Integer(), nullable=False)
    item_name = db.Column(db.String())

    def __repr__(self):
        return f'Item {self.name}'


