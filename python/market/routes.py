from market import app
from flask import render_template, redirect, url_for, flash, request, session
from market.forms import RegisterForm,  LoginForm, PurchaseItemForm, SellItemForm, WithdrawlForm, ReferralForm                          
from market.models import Item, User, Payout, Buyer
from market import db, bcrypt
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from datetime import date, time, timedelta
import  datetime 
import datetime as dt
from pytz import utc
from random import randint 
import random
import string

@app.route('/')
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    register_time = datetime.datetime.now()
    if form.validate_on_submit():
        referral_code=form.referral_code.data
        link_id=generate_referral_code()
     # Check if referral code exists in the database
        referred_by = None 
        if referral_code:
            referred_by_user = User.query.filter_by(referral_code=referral_code).first()
            
        if referred_by_user:
            referred_by = referred_by_user.id 

        # Add referral bonus to referred user's account
        if referred_by:
            referred_by_user.referred_bonus += 100
            db.session.commit()

        user_to_create = User(username=form.username.data, email_address=form.email_address.data, password=form.password1.data, refer_code=link_id, referral_code=generate_referral_code(), referred_by=referred_by)
        db.session.add(user_to_create)    
        db.session.commit()
        return redirect(url_for('login_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error: {err_msg}', category='danger')
    return render_template('index.html', form=form)      

@app.route('/market', methods=['GET', 'POST'])
def market_page():
    purchase_form = PurchaseItemForm()
    if request.method =="POST":
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            p_item_object.owner = current_user.id
            current_user.budget -= p_item_object.price
            db.session.commit()
            create = Buyer(item_owner=current_user.id, item_name=p_item_object.name)
            db.session.add(create)
            db.session.commit()
    items = Item.query.all()
    return render_template('market.html', items=items, purchase_form=purchase_form)              


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()   
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            return redirect(url_for('market_page'))
        else:
            flash('Username and password are not match!', category='danger')    
    return render_template('login.html', form=form)       

@app.route('/logout')
def logout_page():
    logout_user()
    return redirect(url_for("login_page"))

@app.route('/withdrawl', methods=['GET', 'POST'])
def withdrawl_page():  
    withdraw_time = datetime.datetime.now()
    attempted_withdraw = Payout.query.filter_by(check=current_user.id).first()
    attempted_withdrawl = Payout.query.filter_by(check=current_user.id).order_by(Payout.ac_number.desc()).first()
    form = WithdrawlForm(obj=attempted_withdrawl) if attempted_withdrawl else WithdrawlForm()
    enter_amount = form.withdraw.data 
    if form.validate_on_submit():
        if attempted_withdraw:
            flash('Per day 1 withdraw allowed')
        else:
            if enter_amount>=100 and current_user.budget>=enter_amount:
                current_user.budget -= enter_amount
                ac = Payout(ac_name=form.ac_name.data, ac_number=form.ac_number.data, ac_ifsc=form.ac_ifsc.data,withdraw=form.withdraw.data, check=current_user.id)
                db.session.add(ac)
                db.session.commit()
                acc = Payout
            else:
                flash('Withdraw must be greater than or equal 100', category='danger')
    return render_template('withdrawl.html', form=form)

@app.route('/Income')
def income_page():
    buy = Buyer.query.filter_by(item_owner=current_user.id).first()
    return render_template('income.html')

@app.route('/icon')
def icon_page():
    return render_template('icon.html')


@app.route('/referrals/<referral_code>')
@login_required
def referrals(referral_code):
    referral_link = request.host_url + 'register?referral_code=' + referral_code
    return render_template('referrals.html', referral_link=referral_link)

def generate_referral_code():
    letters = string.ascii_lowercase
    digits = string.digits
    return ''.join(random.choice(letters + digits) for i in range(6))


@app.route('/team')
def team():
    frineds = User.query.filter_by(referred_by=current_user.id).all()
    user = current_user
    bonus = user.recharge_amount*0.2
    user.referred_bonus += bonus
    user.update_referred_bonus()
    return render_template('team.html', frineds=frineds)
    
@app.route('/my')
def my():
    return render_template('my.html')

@app.route('/my product')
def record():
    return render_template('record.html')

@app.route('/account record')
def account():
    children = Payout.query.filter_by(check=current_user.id).all()
    return render_template('account.html', children=children)

@app.route('/personal info')
def personal():
    return render_template('info.html')

@app.route('/company')
def company():
    return render_template('company.html')

@app.route('/withdrawls')
def withdrawls():
    children = Payout.query.filter_by(check=current_user.id).all()
    return render_template('with.html', children=children )

@app.route('/recharges')
def recharge():
    return render_template('recharge.html')

