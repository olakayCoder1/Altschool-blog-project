# Altschool Second Semester Examination Project

![image](https://user-images.githubusercontent.com/95700260/200096389-0da5ce67-3664-4a0f-b3a0-041f2c7fb21a.png)

# (Zenith ) Simple Blog App With Flask

Zenith is a blogging website,The following are the stack used in creating this projects:
- Html/css
- Javascript
- Python (Flask)

## Environment setup
To run this website locally on your system make sure you have python install on your device. The list of packages that this project required can be found [here](https://github.com/olakayCoder1/Altschool-blog-project/blob/main/requirements.txt).

```sh
mkdir <folder name>
``` 
in this case I will call it zenith. ```mkdir zenith```

navigate to the newly created folder 
```sh
cd <folder name> 
``` 
.ie ```cd zenith ```

clone the projects
```sh
git clone https://github.com/olakayCoder1/Altschool-blog-project . 
```
as you can see I added a dot (.) at the end, this will make the project be cloned in the current directory.

## Folder structure 

```
├── migrations
├── myblog
│   └── static
|   |   └── css
|   |   └── img
|   |   └── uploads
|   |   └── js
|   └── template
|        └── (html files)
|   └── __init__.py
|   └── account_routes.py
|   └── forms.py
|   └── models.py
|   └── post_routes.py
|   └── routes.py
|   └── utils.py
├── .flaskenv
├── .gitignore
├── configurations.py
├── README.md
├── requirements.txt
└── run.py
```

- #### migrations
  - This folder contains the database migration history
- #### myblog
  - This folder contain the project engine, which are:
    - #### static
      - This contain both the static files( html, css , img ) and 
      - The media files ( upload file by user )
    -  #### templates
       -  This contain the html files
    -  #### __init__.py
       -  This make the current directory a package
    - #### account_routes.py
      - The file for the user account routes
    - #### forms.py
      - The file that hold the forms used in the project
    - #### models.py
      - The file that contain the database base schema in python format ( class)
    - #### post_routes.py
      - The file that contain the post/blog routes
    - #### utils.py
      - The file contain utility function that are reused throughout the project
- #### .flaskenv
  - This file contain the environmental variable config  
- #### .gitignore
  - This file contain the list of ignore files( files that should not be inclusive in github)
-  #### configurations.py
   -  This file contains the project status ( development/ production/testing)
- #### README.py
  - This file contains the description fo the projects
- #### requirements.txt
  - This file contains the necessary packages required to run this project
- #### run.py
  - This file handles the running of the server



## How it works

- The app is available for all users and any user that wish to contribute to content is required to logged in.
- The home page contains the list of post in descending order of the creation date and signed in and non signed in users can visit this page.
- Each blog shows the user that created it and the time the blog was created.
- If a user is signed in and visits an article they created, they should see an edit button to edit either the title or the body of the article.
- A post can be edited or deleted only if the user is the author of the post
- User is able to reset password

### Database schema

```sh
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), nullable=False , unique=True)
    email =  db.Column( db.String(100) , nullable=False , unique=True )
    first_name = db.Column(db.String(100), nullable=False )
    last_name = db.Column(db.String(100), nullable=False )
    image = db.Column(db.String(200), nullable=True )
    password_hash = db.Column(db.String(64) , nullable=False )
    created_at = db.Column(db.DateTime() , nullable=False , default=datetime.utcnow)
    post = db.relationship('Post', backref='post_author', lazy=True) 


class Post(db.Model):
    id = db.Column(db.Integer() , primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text() , nullable=False)
    author = db.Column(db.Integer(), db.ForeignKey('user.id'))
    image = db.Column(db.Text(), nullable=True)
    date_posted = db.Column(db.DateTime() , nullable=False , default=datetime.utcnow)

```

All the fields of the tables on both User and Post are well explanatory themselves. 
```post = db.relationship('Post', backref='post_author', lazy=True) ``` This line describe a one to many relationship with the Post table and ```author = db.Column(db.Integer(), db.ForeignKey('user.id'))``` This line describe a many to one relationship with the User table.


### User Authentication
User authentication is a method that keeps unauthorized users from accessing sensitive information. 

#### Authentication
The following are user registration and authentication routes:
| ROUTE | FUNCTIONALITY |ACCESS|
| ----- | ------------- | ------------- |
| ```/register``` | _Register new user_| _Any user_|
| ```/login``` | _Login user_| _Any_|
| ```/logout``` | _Logout user_| _Authenticated user_|
| ```/password-reset``` | _Request password reset_| _Any_|
| ```/password-reset``` | _ Change password_| _Authenticated user_|
| ```/password-reset/<token>/<public_id>``` | _Confirm password reset & create new password_| _Any_|
| ```/account``` | _User account_| _Authenticated user_|
| ```/account/edit``` | _Edit account_| _Authenticated user_|
| ```/account/delete``` | _Delete account_| _Authenticated user_|

-   import registration form from forms.py ( flask_wtf is required for this to work )
-   The registration form fields are ( username , first_name , last_name , email , password1 and password2 )
   


#### Blog Creation
The following are blog routes:
| ROUTE | FUNCTIONALITY |ACCESS|
| ----- | ------------- | ------------- |
| ```/posts``` | _Get a posts_| _Authenticated user_|
| ```/posts/<public_id>``` | _Retrieve a post_| _Authenticated user_|
| ```/posts/<public_id>/create``` | _Create a post_| _Authenticated user_|
| ```/posts/<public_id>/edit``` | _Edit a post_| _Authenticated user and post author_|
| ```/posts/<public_id>/delete``` | _Delete a post_| _Authenticated user and post author_|


