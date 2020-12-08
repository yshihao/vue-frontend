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
@app.route("/testlogin",methods=['POST','GET'])
def logins():
    #json = request.get_json()
    #print(json['username'])
    user = User.query.filter_by(username = "admin2").first()
    if user is None:
        return "wrong user",404,[("token","123456")]
    if user.verify_password("123456"):
        g.current_user = user
        token = user.generate_auth_token()
        print(token)
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
    #print(username_token)
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
    '''
    #newd = Deployment(name="test4",ready="1/1",uptodate="20",available="2",age="2 month",user_id=10)
    #db.session.add(newd)
    #db.session.commit()
    result = []
    alldeploy = Deployment.query.filter(Deployment.user_id==g.current_user.id).all()
    for value in alldeploy:
        v = {}
        print(value,value.name)
        v['name'] = value.name
        v['ready'] = value.ready
        v['uptodate'] = value.uptodate
        v['available'] = value.available
        v['age'] = value.creation_timestamp
        result.append(v)
    return {
        "code": 200,
        "data": result
    }
@app.route('/api/addDeployment',methods=['post','get'])
@auth.login_required
def add_deployment():
    '''
    处理前端发来的创建deployment请求，甚至包括service和ingress
    '''
    data = request.get_json(force=True)

    # 注解与标签处理
    w_name = data['deploy_infos']['name']
    data['deploy_infos']['annotations']['k8s.webserver/workload'] = w_name
    data['deploy_infos']['labels']['k8s.webserver/workload'] = w_name
    data['service_infos']['annotations']['k8s.webserver/workload'] = w_name
    data['service_infos']['labels']['k8s.webserver/workload'] = w_name
    data['ingress_infos']['annotations']['k8s.webserver/workload'] = w_name
    data['ingress_infos']['labels']['k8s.webserver/workload'] = w_name
   
    # dry_run 并得到结果（需要格式化，但还没测试）
    deploy_res = k8s_connection.create_namespaced_deployment(data['namespace'],data['deploy_infos'],data['containers'],data['volumes'],data['pod_infos'],data['initial_contianers'],True)
    service_res = k8s_connection.create_namespaced_service(data['namespace'],data['service_infos'],True)
    ingress_res = k8s_connection.create_namespaced_ingress(data['namespace'],data['ingress_infos'],True)

    # 考虑临时文件储存一下这个配置，给个有效时间

    return {
        "code":200,
        "data":{
            "deploy_res": deploy_res,
            "service_res": service_res,
            "ingress_res": ingress_res
        }
    }

@app.route('/api/confirmDeployment',methods=['post','get'])
@auth.login_required
def confirm_deployment():
    '''
    '''
    data = None # 加载临时文件
    res = k8s_connection.create_namespaced_deployment(data.deploy_infos,data.containers,data.volumes,data.pod_infos,data.initail_containers)

@app.route('/get/username',methods=['get'])
@auth.login_required
def get_username():
    
    print(g.current_user.username)
    return {
        "code":200,
        "username":g.current_user.username
    }
@app.route('/api/login')
@auth.login_required
def get_auth_token():
    token = g.current_user.generate_auth_token()
    return jsonify(token)