from myblog import app 
from flask import render_template  , request
from myblog.models import Post



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
    

@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_not_found.html')
