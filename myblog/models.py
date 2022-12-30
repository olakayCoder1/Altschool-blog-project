from myblog import db , bcrypt
from datetime import datetime
from flask_login import UserMixin
from myblog import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)




followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


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
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')


    @classmethod
    def get(cls, id:int ):
        return cls.query.get(id)

    @classmethod
    def email_exist(cls, email:str ):
        user = cls.query.filter_by(email=email).first()
        if user :
            return True
        return False


    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, text_password):
        self.password_hash = bcrypt.generate_password_hash(text_password).decode('utf-8')


    def check_password(self, text_password):
        return bcrypt.check_password_hash(self.password_hash, text_password)


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return self.email


    
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0



    # def followed_users(self):
    #     return User.query.join(
    #         followers, (followers.c.followed_id == User.user_id)).filter(
    #             followers.c.follower_id == self.id).order_by(
    #                 User.timestamp.desc())






class Post(db.Model):
    id = db.Column(db.Integer() , primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text() , nullable=False)
    author = db.Column(db.Integer(), db.ForeignKey('user.id'))
    image = db.Column(db.Text(), nullable=True)
    date_posted = db.Column(db.DateTime() , nullable=False , default=datetime.utcnow)

    def __repr__(self) -> str:
        return self.title


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self): 
        db.session.delete(self)
        db.session.commit()





class Token(db.Model):
    id = db.Column(db.Integer() , primary_key=True)
    user =  db.Column(db.Integer(), db.ForeignKey('user.id'))
    token = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime() , nullable=False , default=datetime.utcnow)
    is_blacklisted = db.Column(db.Boolean(),  default=False)
    is_password = db.Column(db.Boolean(),  default=False)
    is_2fa = db.Column(db.Boolean(),  default=False)



    def save(self):
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()


