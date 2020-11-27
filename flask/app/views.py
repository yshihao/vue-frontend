from app import app,db,auth
from flask import json,jsonify,request,g
from app.models import *
import k8s_connection 


@app.route("/login",methods=['POST','GET'])
def login():
    json = request.get_json()
    #print(json['username'])
    user = User.query.filter_by(username = json['username']).first()
    if user is None:
        return "wrong user"
    if user.verify_password(json['password']):
        g.current_user = user
        token = user.generate_auth_token()
        #print(token)
        return token
    return "wrong password"
@app.route("/register",methods=['POST'])
def new_user():
    json = request.get_json()
    isexist = User.query.filter(User.username==json['username']).first()
    if isexist:
        return "userexist"
    newuser = User(username=json['username'],set_password=json['password'])
    #newuser = User(username="admin",set_password="123456")
    db.session.add(newuser)
    db.session.commit()
    print("yes")
    return "200 OK"
@auth.verify_password
def verify_password(username_or_token,password):

    username_token = request.headers.get('accessToken')
    print(username_token)
    if username_token =='':
        return False
    else:
        g.current_user = User.verify_auth_token(username_token)
        g.token_used = True
        return g.current_user is not None
@app.route('/api/deployment/list',methods=['get'])
@auth.login_required
def deployment_list():
    '''
    deployments = k8s_connection.list_namespaced_deployment()
    print(deployments)
    result = []
    today = datetime.date.today()
    for deploy in deployments.items:
        v = {}
        v['name'] = deploy.metadata.name
        v['ready'] = '{}/{}'.format(deploy.status.ready_replicas,deploy.status.replicas)
        v['uptodate'] = '{}'.format(deploy.status.updated_replicas)
        v['available'] = '{}'.format(deploy.status.available_replicas)
        age = today.__sub__(deploy.metadata.creation_timestamp.date())
        v['age'] = '{}天'.format(age.days)
        result.append(v)
    return {
        "code": 200,
        "data": result
    }
    '''
    #newd = Deployment(name="test4",ready="1/1",uptodate="20",available="2",age="2 month",user_id=10)
    #db.session.add(newd)
    #db.session.commit()
    result = []
    v = {}
    alldeploy = Deployment.query.filter(Deployment.user_id==g.current_user.id).all()
    for value in alldeploy:
        v['name'] = value.name
        v['ready'] = value.ready
        v['uptodate'] = value.uptodate
        v['available'] = value.available
        v['age'] = value.age
        result.append(v)
    return {
        "code": 200,
        "data": result
    }
@app.route('/api/addcontainer',methods=['post','get'])
@auth.login_required
def add_container():
    containername = request.args.get('containername')
    imagename = request.args.get('imagename')
    print(g.current_user.username)
    # print(os.getcwd())
    #k8s_connection.create_namespaced_deployment(containername,[{'image':imagename}],'default')
    return {
        "code":200
    }
@app.route('/api/login')
@auth.login_required
def get_auth_token():
    token = g.current_user.generate_auth_token()
    return jsonify(token)