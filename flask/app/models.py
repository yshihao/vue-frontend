
from app import db,app
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,SignatureExpired,BadSignature

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")
    @password.setter
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
    def generate_auth_token(self, expiration = 6000):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id }) #生成token
    @staticmethod
    def verify_auth_token(token):
        #不用实例化就能调用
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user

class Deployment(db.Model):
    __tablename__ = 'deployments'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True,nullable=False)
    ready = db.Column(db.String(64),nullable=False)
    uptodate = db.Column(db.String(64),nullable=False)
    available = db.Column(db.String(64),nullable=False)
    age = db.Column(db.String(64),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    


    


