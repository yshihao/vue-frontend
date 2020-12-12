from app import app,db,auth
from flask import json,jsonify,request,g
from app.models import *
import k8s_connection 
import datetime


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

    # test
    data['namespace'] = 0
    data['fileId'] = 1

    # 注解与标签处理
    w_name = data['deploy_infos']['name']
    data['deploy_infos']['annotations']['k8s.webserver/workload'] = w_name
    try:
        data['deploy_infos']['labels']['k8s.webserver/name'] = w_name
    except TypeError:
        data['deploy_infos']['labels'] = {}
        data['deploy_infos']['labels']['k8s.webserver/name'] = w_name
    try:
        data['service_infos']['annotations']['k8s.webserver/workload'] = w_name
    except KeyError:
        data['service_infos']['annotations'] = {}
        data['service_infos']['annotations']['k8s.webserver/workload'] = w_name
    try:
        data['service_infos']['labels']['k8s.webserver/name'] = w_name
    except KeyError:
        data['service_infos']['labels'] = {}
        data['service_infos']['labels']['k8s.webserver/name'] = w_name
    try:
        data['ingress_infos']['annotations']['k8s.webserver/workload'] = w_name
    except KeyError:
        data['ingress_infos']['annotations']['k8s.webserver/workload'] = w_name
    try:
        data['ingress_infos']['labels']['k8s.webserver/name'] = w_name
    except KeyError:
        data['ingress_infos']['labels'] = {}
        data['ingress_infos']['labels']['k8s.webserver/name'] = w_name

    # 名称处理
    data['service_infos']['name'] = w_name
    data['ingress_infos']['name'] = w_name

    # # dry_run 并得到结果（需要格式化，但还没测试）
    try:
        deploy_res = k8s_connection.create_namespaced_deployment(data['namespace'],data['deploy_infos'],data['containers'],data['volumes'],data['pod_infos'],data['initial_contianers'],True)
        deploy_succeed = True
    except k8s_connection.client.exceptions.ApiException as err:
        deploy_res = k8s_connection.format_create_failure(err)
        deploy_succeed = False
    try:
        service_res = k8s_connection.create_namespaced_service(data['namespace'],data['service_infos'],True)
        service_succeed = True
    except k8s_connection.client.exceptions.ApiException as err:
        service_res = k8s_connection.format_create_failure(err)
        service_succeed = False
    try:
        ingress_res = k8s_connection.create_namespaced_ingress(data['namespace'],data['ingress_infos'],True)
        ingress_succeed = True
    except k8s_connection.client.exceptions.ApiException as err:
        ingress_res = k8s_connection.format_create_failure(err)
        ingress_succeed = False

    # 考虑临时文件储存一下这个配置，给个有效时间
    path = "/home/werthy/TempFiles/"+data['namespace']+'_'+data['fileId']+'.yml'
    with open(path,'w+') as f:
        yaml.safe_dump(data,f)
    new_deployment_creation = DeploymentCreation(id=data['file'],path=path,
                                                creation_timestamp=datetime.datetime.now().timestamp(),
                                                user_id=data['namespace'])
    db.session.add(new_deployment_creation)
    db.session.commit()

    return {
        "code":200,
        "data":{
            "deploy_succeed": deploy_succeed,
            "deploy_res": deploy_res,
            "service_succeed": service_succeed,
            "service_res": service_res,
            "ingress_succeed": ingress_succeed,
            "ingress_res": ingress_res
        }
    }

@app.route('/api/confirmDeployment',methods=['post','get'])
@auth.login_required
def confirm_deployment():
    '''
    读取暂存的临时文件，校验其时间，如果在有效期内，则发往k8s执行.
    '''
    user_id = request.args.get('id')
    file_id = request.args.get('fileId')
    
    res = {
        'not_find_file': False,
        'out_of_time': False,
        'deploy_succeed': False,
        'service_succeed': False,
        'ingress_succeed': False
    }
    record = DeploymentCreation.query.filter(DeploymentCreation.id==file_id,DeploymentCreation.user_id==user_id).first()
    now_time = datetime.datetime.now().timestamp()
    if record == None:
        res['not_find_file'] = True
    elif now_time - record.creation_timestamp > 5 * 60:
        res['out_of_time'] = True
    else:
        path = record.path
        with open(path) as f:
            data = yaml.safe_load(f.read())
        try:
            res['deploy_res'] = k8s_connection.create_namespaced_deployment(data['namespace'],data['deploy_infos'],data['containers'],data['volumes'],data['pod_infos'],data['initial_contianers'],False)
            res['deploy_succeed']= True
        except k8s_connection.client.exceptions.ApiException as err:
            res['deploy_res'] = k8s_connection.format_create_failure(err)
        try:
            res['service_res'] = k8s_connection.create_namespaced_service(data['namespace'],data['service_infos'],False)
            res['service_succeed'] = True
        except k8s_connection.client.exceptions.ApiException as err:
            res['service_res'] = k8s_connection.format_create_failure(err)
        try:
            res['ingress_res'] = k8s_connection.create_namespaced_ingress(data['namespace'],data['ingress_infos'],False)
            res['ingress_succeed'] = True
        except k8s_connection.client.exceptions.ApiException as err:
            res['ingress_res'] = k8s_connection.format_create_failure(err)
    return {
        "code":200,
        "data":res
    }

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
