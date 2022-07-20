from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField, IntegerField, FloatField, DecimalField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, NumberRange
from shop.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Please enter your username'), Length(min=3, max=15)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Regexp('^.{6,12}$',
                              message='Your password should be between 6 and 12 characters long.')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username has already been taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('This email is already registered. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class CheckoutForm(FlaskForm):
    FirstName = StringField('First Name', validators=[DataRequired('Please enter your First Name'), Length(min=3, max=15)])
    LastName = StringField('Last Name', validators=[DataRequired('Please enter your Last Name'), Length(min=3, max=15)])
    Address = StringField('Address', validators=[DataRequired('Please enter your Address')])
    Card_No = PasswordField('Card_No', validators=[DataRequired('Please enter your 16-digit card number'), Length(min=16, max=16)])
    CVC = PasswordField('CVC', validators=[DataRequired('Please enter your 3-digit CVC'), Length(min=3, max=3)])
    ExpDate = PasswordField('ExpDate', validators=[DataRequired('Please enter your expiry date in form MMYYYY'), Length(min=6, max=6)])
    Submit = SubmitField('Checkout')

class UpdateEmailForm(FlaskForm):
	email = StringField('New Email', validators=[DataRequired(), Email()])
	password = PasswordField('Current Password', validators=[DataRequired()])
	submit = SubmitField('Update Email')

class UpdatePasswordForm(FlaskForm):
	password =  PasswordField('Current Password', validators=[DataRequired(),Regexp('^.{6,12}$',
                              message='Your password should be between 6 and 12 characters long.')])
	new_password =  PasswordField('Password', validators=[DataRequired(),Regexp('^.{6,12}$',
                              message='Your password should be between 6 and 12 characters long.')])
	confirm_new_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
	submit = SubmitField('Update Password')
