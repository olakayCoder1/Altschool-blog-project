from myblog import app 
from flask import render_template 




from myblog import account_routes
from myblog import post_routes

@app.route('/')
def index():
    return render_template('home.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_not_found.html')
