from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, BooleanField, FloatField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError 
from market.models import User

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username already exist!")


    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError("Email alredy exist!")


    username = StringField(label='username', validators=[Length(min=3, max=30), DataRequired()])
    email_address = StringField(label='email', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='confirm password', validators=[EqualTo('password1'), DataRequired()])
    referral_code = StringField(label='Referral Code')
    submit = SubmitField(label='submit')

class LoginForm(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Login')


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase')

class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell')

class WithdrawlForm(FlaskForm):
    ac_name = StringField(label='bank name', validators=[DataRequired()])
    ac_number = IntegerField(label='Account number', validators=[DataRequired()])
    ac_ifsc = StringField(label='Ifsc code', validators=[DataRequired()])
    withdraw = IntegerField(label='Enter amount', validators=[DataRequired()])
    submit = SubmitField(label='Withdraw')
    
class ReferralForm(FlaskForm):
    campaign_name = TextAreaField('Campaign Name:', validators=[DataRequired()])
    redirect_link = TextAreaField('Redirect Link:', validators=[DataRequired()], default='http://127.0.0.1:5000/register')