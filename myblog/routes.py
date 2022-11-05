from myblog import app 
from flask import render_template  , request , flash
from myblog.models import Post
from myblog.utils import MailService
from threading import Thread

from myblog import account_routes
from myblog import post_routes


@app.route('/')
def index():
    posts = Post.query.order_by(Post.date_posted.desc())
    page = request.args.get('page', None)

    if page and page.isdigit():
        try:
            page = int(page)
        except:
            page = 1
    else:
        page = 1    
    pages = posts.paginate(page=page , per_page=6)
    return render_template('home.html', posts=posts , pages=pages)


@app.route('/about')
def about():
    return render_template('about.html')
    

@app.route('/contact')
def contact():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        content = request.form.get('content')
        subject = request.form.get('subject')
        Thread(target=MailService.send_reset_mail, kwargs={
                    'email': email ,'first_name': first_name , 'last_name ':last_name  , 'subject': subject , 'content': content
                }).start()
        flash('Mail successfully sent' , 'success')
        return render_template('contact.html')
    return render_template('contact.html')
    

@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_not_found.html')
