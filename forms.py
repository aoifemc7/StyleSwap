from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, PasswordField, SubmitField, FileField
from wtforms.validators import InputRequired, EqualTo

class RegistrationForm(FlaskForm):
    user_id = StringField("User id:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    password2 = PasswordField("Confirm Password:",
        validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    user_id = StringField("User id:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    submit = SubmitField("Submit")

class SellForm(FlaskForm):
    name =  StringField("Product name:", validators=[InputRequired()])
    price = IntegerField("Product price:", validators=[InputRequired()])
    type = StringField("Product type:", validators=[InputRequired()])
    description = StringField("Product description:", validators=[InputRequired()])
    #image = FileField("Image:", validators=[InputRequired()])
    submit = SubmitField("Submit")

