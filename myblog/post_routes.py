from myblog import app , db 
from flask import render_template , redirect , url_for , flash , request 
from flask_login import current_user , login_required
from myblog.models import User , Post
from werkzeug.utils import secure_filename
import os
from uuid import uuid1



@app.route('/posts')
def posts_page():
    # for m in Post.query.all():
    #     db.session.delete(m) 
    # db.session.commit()
    posts = Post.query.all()
    users = User.query.all()
    return render_template('blog.html', posts=posts)


@app.route('/posts/<public_id>')
def post_details_page(public_id):
    post = Post.query.filter_by(public_id=public_id).first()
    if post:
        more = Post.query.filter(Post.id != post.id).limit(2) 
        return render_template('blog-details.html', post=post ,  more=more)
    return redirect(url_for('page_not_found'))




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS'] 

@app.route('/posts/create'  , methods=['POST', 'GET'])
@login_required
def post_create():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        image = request.files.get('image', None)
        new_post = Post(title=title , content=content , author=current_user.id)
        if image != None:
            filename =  secure_filename(image.filename)
            name = 'posts_' + str(uuid1()) + '_' + filename
            image_url = url_for('static', filename='uploads/' + name )
            new_post.image = image_url
        try:
            new_post.save()
            if image != None:
                image.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'] , name))
        except:
            db.session.rollback()
        return redirect(url_for('post_details_page', id=new_post.id))
    return render_template('editor.html')


@app.route('/posts/<public_id>/edit'  , methods=['POST', 'GET'])
@login_required
def post_edit(public_id):
    post = Post.query.filter_by(public_id=public_id).first()
    if post:

        post = Post.query.get_or_404(id)
        if request.method == 'POST':
            post.title = request.form.get('title')
            post.content = request.form.get('content')
            image = request.files.get('image', None)  
            if image != None:
                filename =  secure_filename(image.filename)
                name = 'posts_' + str(uuid1()) + '_' + filename
                image_url = url_for('static', filename='uploads/' + name )
                post.image = image_url
            try:
                post.save()
                if image != None:
                    image.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'] , name))
            except:
                db.session.rollback()
                flash('An error occurred while updating blog, try again', 'err')
                return render_template('edit-blog.html', post=post)
            return redirect(url_for('post_details_page' , id=post.id ))
        return render_template('edit-blog.html', post=post)
    return redirect(url_for('page_not_found'))
    



@app.route('/posts/<public_id>/delete')
@login_required
def post_delete(public_id):
    post = Post.query.filter_by(public_id=public_id).first()
    if post:
        try:
            post.delete()
        except:
            db.session.rollback()
    return redirect(url_for('posts_page'))







