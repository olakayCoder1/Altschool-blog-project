from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField , SubmitField , FileField
from wtforms.validators import Length , EqualTo , Email , DataRequired






class RegisterForm(FlaskForm):
    username = StringField(label='Username', validators=[Length(min=2, max=30) , DataRequired()])
    email = StringField(label='Email' , validators=[Email() , DataRequired()])
    first_name = StringField(label='First name'  , validators=[DataRequired()])
    last_name = StringField(label='Last name'  , validators=[ DataRequired()])
    password1 = PasswordField(label='Password' , validators=[Length(min=6) , DataRequired()])
    password2 = PasswordField(label='Confirm password', validators=[EqualTo('password1') , DataRequired() ])
    submit = SubmitField(label='Register')




class AccountForm(FlaskForm):
    username = StringField(label='Username', validators=[Length(min=2, max=30) , DataRequired()])
    email = StringField(label='Email' , validators=[Email() , DataRequired()])
    first_name = StringField(label='First name' , validators=[ DataRequired()])
    last_name = StringField(label='Last name', validators=[ DataRequired()] )
    profile_pic = FileField(label='Profile picture')
    submit = SubmitField(label='Register')




class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[ DataRequired()])
    password = PasswordField(label='Password' , validators=[ DataRequired()])
    submit = SubmitField(label='Login')



class PostCreateForm(FlaskForm):
    title = StringField(label='Title', validators=[Length(min=2, max=30) , DataRequired()])
    content = StringField('Content' , validators=[ DataRequired()])
    submit = SubmitField(label='Publish')



class PasswordResetRequestForm(FlaskForm):
    email = StringField(label='Email' , validators=[Email() , DataRequired()])
    submit = SubmitField(label='Send instruction')


class PasswordResetConfirmForm(FlaskForm):
    password1 = StringField(label='Password' , validators=[DataRequired()])
    password2 = StringField(label='Confirm password' , validators=[DataRequired()])
    submit = SubmitField(label='Reset password')
