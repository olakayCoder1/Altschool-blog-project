from myblog import app , db , bcrypt
from flask import render_template , redirect , url_for , flash , request 
from flask_login import login_user , logout_user , login_required
from flask_login import login_user , current_user , logout_user , login_required
from .forms import RegisterForm , LoginForm ,  AccountForm , PasswordResetConfirmForm , PasswordResetRequestForm
from .models import User , Post  , Token
from werkzeug.utils import secure_filename
from myblog.utils import authenticated_not_allowed
from myblog.utils import MailService  , TokenService 
import os
import uuid
from threading import Thread


@app.route('/account')
@login_required
def account(): 
    print("***"*100)
    print(request.referrer)
    print("***"*100)  
    user = User.query.get_or_404(current_user.id)
    posts = Post.query.filter_by(author=user.id)
    return render_template('account.html', user=user , posts=posts)


@app.route('/account/edit' ,  methods=['POST', 'GET'])
@login_required
def account_edit():
    form = AccountForm()
    if request.method == 'POST':
        user = User.query.get(current_user.id)
        username = request.form.get('username', None)
        last_name = request.form.get('last_name', None)
        first_name = request.form.get('first_name', None)
        email = request.form.get('email', None)
        image = request.files.get('image', None)

        """
        check if the updated email is same as the current email 
        else : check if there is a user with the email
        """
        if current_user.email != email :
            user = User.query.filter_by(email=email).first()
            if user :
                flash('Email already exist ', 'error')
                return render_template('account-edit.html' , form=form)
        """
        check if the updated username is same as the current email 
        else : check if there is a user with the username
        """
        if current_user.username != username :
            user = User.query.filter_by(username=username).first()
            if user :
                flash('Username already exist ', 'error')
                return render_template('account-edit.html' , form=form)
        if image != None : 
            filename =  secure_filename(image.filename)
            name = 'profiles_' + str(uuid.uuid1()) + '_' + filename
            image_url = url_for('static', filename='uploads/' + name )
            user.image = image_url
        try:
            user.save()
            if image != None :
                image.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'] , name))
        except:
            db.session.rollback()
            flash('An error occurred updating ', 'error')
            return render_template('account-edit.html' , form=form)
        flash('Account updated successfully', 'success')
        return redirect(url_for('account'))
    return render_template('account-edit.html' , form=form)


@app.route('/register' , methods=['POST', 'GET'])
@authenticated_not_allowed
def register():
    print(Token.__dict__)

    form = RegisterForm()
    if form.validate_on_submit():
        username_exist = User.query.filter_by(username=form.username.data).first()
        if form.password1.data != form.password2.data :
            flash('Password does not match' , 'error')
            return render_template('register.html', form=form)
        if username_exist:
            flash('Username already exist' , 'error')
            return render_template('register.html', form=form)
        email_exist = User.query.filter_by(email=form.email.data).first()
        if email_exist:
            flash('Email already exist' , 'error')
            return render_template('register.html', form=form)
        public_id = str(uuid.uuid4().int & (1<<64)-1)
        new_user = User(username=form.username.data , email=form.email.data , first_name=form.first_name.data , last_name=form.last_name.data , password=form.password1.data , public_id=public_id)
        try:
            new_user.save() 
        except:
            db.session.rollback()
        login_user(new_user)
        return redirect(url_for('posts_page'))
    return render_template('register.html', form=form)


@app.route('/login' , methods=['POST', 'GET'])
@authenticated_not_allowed
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(user)
        if user and user.check_password(form.password.data) :
            login_user(user)
            return redirect(url_for('posts_page'))
        flash('Invalid login credentials', 'error')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out. See you next time', category='success')          
    return redirect(url_for('index'))



@app.route('/password-reset', methods=['POST', 'GET'])
def password_reset_email():
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            print('***'*100)
            print(user.id)
            print('***'*100)
            ## SEND EMAIL TO USER
            token = TokenService.create_password_reset_token(user.id)
            public_id=user.public_id
            Thread(target=MailService.send_reset_mail, kwargs={
                    'email': user.email ,'token': token , 'public_id':public_id
                }).start()
    flash('Instruction to reset your password has been sent to the provided email') 
    return render_template('password-reset-request.html' , form=form)



@app.route('/password-reset/<token>/<user_public_id>/confirm', methods=['POST', 'GET'])
def password_reset_confirm(token, user_public_id ):
    form = PasswordResetConfirmForm()
    if form.validate_on_submit():
        password = request.form['password1']
        confirm_password = request.form['password2']
        if password and confirm_password :
            if password == confirm_password :
                if TokenService.validate_password_token(token , user_public_id ) :
                    user = User.query.filter_by(public_id=user_public_id ).first()
                    try:
                        user.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
                        user.save()
                        flash('Password updated successfully')
                        return redirect(url_for('login'))
                    except:
                        db.session.rollback()
                        flash('Password reset token is invalid')
                        return render_template('password-reset-confirm.html' , form=form)
                flash('Password reset token is invalid')
                return render_template('password-reset-confirm.html' , form=form)
            flash('Password does not match')
            return render_template('password-reset-confirm.html' , form=form)
    return render_template('password-reset-confirm.html' , form=form)




