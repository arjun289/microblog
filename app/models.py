from app import db
from hashlib import md5

followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id'))
                     )



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(60),unique=True)
    email = db.Column(db.String(120),unique=True)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic' )
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    followed = db.relationship('User',
                               secondary = followers,
                               primaryjoin = (followers.c.follower_id == id),
                               secondaryjoin = (followers.c.follower_id == id),
                               backref = db.backref('followers', lazy = 'dynamic'),
                               lazy = 'dynamic'
                            )

    def is_following(self, user):
        return self.followed.filter(followers.c.follower_id == user.id).count() > 0

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
         if self.is_following(user):
             self.followed.remove(user)
             return self




    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>'%(self.nickname)

    def avatar(self,size):
       # return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)
       return 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTTKtYBBr8doTiJ7TjTwLgXAq_G7QDZ4HtbWoeWcsi0_ghBHap_QGVdr9k'

    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname = nickname).first() is None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname+str(version)
            if User.query.filter_by(nickname = new_nickname).first() is None:
                break
            version +=1
        return new_nickname

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' %(self.body)


