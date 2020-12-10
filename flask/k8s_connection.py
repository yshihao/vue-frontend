from kubernetes import client,config
from kubernetes import watch as _watch
import yaml
import datetime
from app.models import *

def k8sInitial():
    '''
    初始化，加载配置
    '''
    conf = client.Configuration()
    conf.host = "https://192.168.1.199:40005"
    conf.verify_ssl = False
    # conf.ssl_ca_cert = "./kube-apiserver"
    conf.api_key = {"authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Il9PWnlqaUstcV8yYjdoUWFIdlQyMzduMVlVZ3gxeU00ak1fOTR2OGVzcncifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi10b2tlbi13cW5xOSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJhZG1pbiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjIxMTc1NWFmLTQ2MjMtNDA3Mi05YmFhLTQ2MDNiMmI0ZTgzNSIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlLXN5c3RlbTphZG1pbiJ9.f3N2T68H_aSSu_ADo1oimuWOuH_pyGdvOsoxzA9Njny9cp16z1yPbvQsRCUj0xNXSoG2DdGzBJq3pszdA5Z5HVrf2SJ769_zK4NzyxVH2FjpXW8MjYD1gEvJ1VmASL3PGcVXU6BVGufWX6qAsFXleOPMaIHcDxkNeUDmAemi6riHatM1JLD3cC_urN06wQKPFLRYM4_1DF14FmXiZEoiHcmpMohoDB-cpuWcRix-vYyrw525QLHJMUyB7cwpiaZOUbT0gRnIz38Pfozihoaj5V1aKvciqk0P6iPOO8mjcbvFGjVC-dmG9h88GuC4CeErFRyDAhNUjo_xPGgeMeBbxw"}
    
    client.Configuration.set_default(conf)


def list_all_namespaces():
    '''
    获得所有的命名空间
    ret: list 所有namespaces
    '''
    api = client.CoreV1Api() 

    res=api.list_namespace()
    print(res)


def list_namespaced_deployment(namespace='default', watch=False):
    '''
    获得特定命名空间的所有deployment
    namespace: string 命名空间的名字
    watch: bool 是否追踪变化
    ret: list deployments
    '''
    api = client.AppsV1Api()

    if watch:
        w = _watch.Watch()
        for event in w.stream(api.list_namespaced_deployment, namespace=namespace):
            # print(event)
            deploy = format_deployment_event(event)
            for key,value in deploy.items():
                print(key, value)
    else:
        res = api.list_namespaced_deployment(namespace, pretty='true')
        print(res)


def list_deployment_for_all_namespaces():
    '''
    追踪所有命名空间的deployment，并将其储存进数据库。
    ret: null
    '''
    api = client.AppsV1Api()

    w = _watch.Watch()
    for event in w.stream(api.list_deployment_for_all_namespaces):
        deploy = format_deployment_event(event)
        deploy_old = Deployment.query.filter(Deployment.name==deploy['name'],Deployment.user_id==deploy['user_id']).all()
        if deploy_old == []:
            new_deployment = Deployment(name=deploy['name'], ready=deploy['ready'],
                            uptodate=deploy['uptodate'], available=deploy['available'],
                            creation_timestamp=deploy['creation_timestamp'],
                            user_id=deploy['user_id'])
            db.session.add(new_deployment)
            db.session.commit()
        else:
            # 更新数据表中对应的变量
            # print(deploy_old[0])
            # updatable_keys = ['name','ready','uptodate','available']
            change_flag = 0
            if deploy_old[0].name != deploy['name']:
                deploy_old[0].name = deploy['name']
                change_flag = 1
            if deploy_old[0].ready != deploy['ready']:
                deploy_old[0].ready = deploy['ready']
                change_flag = 1
            if deploy_old[0].uptodate != deploy['uptodate']:
                deploy_old[0].uptodate = deploy['uptodate']
                change_flag = 1
            if deploy_old[0].available != deploy['available']:
                deploy_old[0].available = deploy['available']
                change_flag = 1
            if change_flag:
                db.session.commit()
            # print(2)

def create_namespaced_deployment(namespace,deploy_infos, containers, volumes={}, pod_infos={}, initail_containers=[], dry_run = True):
# def create_namespaced_deployment(name, containers, namespace, annotations={}, labels={},restartPolicy='Always',serviceAccountName='default', replicas=1, volumes={}, dry_run = True):
    '''
    创建给定命名空间的deployment
    namespace: str deployment所属的ns
    deploy_infos: dict {'name':str name, 'annotations':dict annotation, 'labels':dict label, 'replicas':int replicas} deploy模块的信息
    volumes: dict 数据集模块的信息
    pod_infos: dict {'restartPolicy':str policy, 'serviceAccountName':str name} 容器组设定模块
    containers: dict 太复杂了....见yaml
    initail_containers: dict 同上
    dry_run: bool 是否干跑,也即不执行具体内容，只是看配置是否可行
    ret: -> dict 成功则是返回的yaml，失败则是包含错误代码与错误提示信息的dict
    '''
    with open('./flask/template/template.yml') as f:
        res = yaml.safe_load(f.read())

    # name 字段 
    res['metadata']['name'] = deploy_infos['name']

    # labels 字段
    res['metadata']['labels'] = deploy_infos['labels']
    res['spec']['selector']['matchLabels'] = deploy_infos['labels']
    res['spec']['template']['metadata']['labels'] = deploy_infos['labels']
    # res['metadata']['labels']['app'] = name
    # res['spec']['selector']['matchLabels']['app'] = name
    # res['spec']['template']['metadata']['labels']['app'] = name

    # annotations 字段
    res['metadata']['annotations'] = deploy_infos['annotations']

    # replicas 字段
    res['spec']['replicas'] = deploy_infos['replicas']

    # volumes 字段 需要完善！
    res['spec']['template']['spec']['volumes'] = None

    # containers 字段 
    res['spec']['template']['spec']['containers'] = containers
    res['spec']['template']['spec']['initContainers'] = initail_containers

    # restartPolicy 字段
    res['spec']['template']['spec']['restartPolicy'] = pod_infos['restartPolicy']

    # serviceAccountName 字段
    res['spec']['template']['spec']['serviceAccountName'] = pod_infos['serviceAccount']

    # print(res)  
    api = client.AppsV1Api()
    if dry_run:
        response = api.create_namespaced_deployment(namespace, res, dry_run='All')
    else:
        response = api.create_namespaced_deployment(namespace, res)
    # print(response)
    return response


def create_namespaced_service(namespace, service_info, dry_run=True):
    '''
    创建给定命名空间的Service
    namespace: str 给定的命名空间
    service_info: {'}
    '''
    with open('./flask/template/service.yml') as f:
        body = yaml.safe_load(f.read())

    # 基本信息
    body['metadata']['name'] = service_info['name']
    body['metadata']['annotations'] = service_info['annotations']
    body['metadata']['labels'] = service_info['labels']
    body['spec']['selector'] = service_info['labels']

    # 配置信息
    body['spec']['type'] = service_info['type']
    body['spec']['ports'] = service_info['ports']

    api = client.CoreV1Api()
    if dry_run:
        response = api.create_namespaced_service(namespace=namespace, body=body, dry_run="All")
    else:
        response = api.create_namespaced_service(namespace=namespace, body=body)
    print(response)
    return response

def create_namespaced_ingress(namespace, ingress_info,dry_run=True):
    '''
    '''
    with open('./flask/template/ingress.yml') as f:
        body = yaml.safe_load(f.read())

    # 基本信息
    body['metadata']['name'] = ingress_info['name']
    body['metadata']['annotations'] = ingress_info['annotations']
    body['metadata']['labels'] = ingress_info['labels']

    # 配置信息
    body['spec']['rules'] = ingress_info['rules']
    body['spec']['tls'] = ingress_info['tls']

    api = client.NetworkingV1beta1Api()
    if dry_run:
        response = api.create_namespaced_ingress(namespace=namespace,body=body,dry_run='All')
    else:
        response = api.create_namespaced_ingress(namespace=namespace,body=body)
    print(response)
    return response

def delete_namespaced_deployment(name, namespace):
    '''
    删除给定命名空间下的deployment
    name: string deployment的名字
    namespace: string namespace的名字
    ret: 错误代码 0成功 1异常
    '''
    api = client.AppsV1Api()
    try:
        res = api.delete_namespaced_deployment(name, namespace)
        print(res)
        if(res['status']=='Success'):
            return 0
        else:
            return 1
    except client.exceptions.ApiException as err :
        print(err.reason)
        return 1


def format_deployment_event(event):
    '''
    将监听到的event格式化输出
    event: k8s.event 监听到的事件
    ret: dict 格式化的信息
    '''
    # print(type(event['object']))
    # today = datetime.date.today()
    deploy = {}
    deploy['name']=event['object'].metadata.name
    deploy['ready'] = '{}/{}'.format(event['object'].status.ready_replicas,event['object'].status.replicas)
    deploy['uptodate'] = '{}'.format(event['object'].status.updated_replicas)
    deploy['available'] = '{}'.format(event['object'].status.available_replicas)
    deploy['creation_timestamp'] = '{}'.format(event['object'].metadata.creation_timestamp.date())
    # age = today.__sub__(event['object'].metadata.creation_timestamp.date())
    # deploy['age'] = '{}天'.format(age.days)
    deploy['namespace'] = '{}'.format(event['object'].metadata.namespace)
    try:
        deploy['user_id']=int(deploy['namespace'])
    except ValueError:
        deploy['user_id']=0
    return deploy

def format_create_failure(err):
    '''
    格式化输出创建错误
    err: k8s.client.exceptions.ApiException
    ret: string 错误信息
    '''
    body = err.body
    body_dict = yaml.safe_load(body)
    return body_dict['message']

if __name__ == '__main__':
    k8sInitial()
    # list_all_namespaces()
    # list_namespaced_deployment(watch=True)
    # list_deployment_for_all_namespaces()
    # create_namespaced_deployment('test1',[{'image':'nginx', 'name':'test-pod', "imagePullPolicy":'Always'}],'default',labels={'label1':'124'})
    # print(delete_namespaced_deployment('test1','default'))
    with open('/home/werthy/Documents/basic_test.yml') as f:
        data = yaml.safe_load(f.read())

    w_name = data['deploy_infos']['name']
    try:
        data['deploy_infos']['labels']['k8s.webserver/name'] = w_name
    except TypeError as err:
        data['deploy_infos']['labels'] = {}
        data['deploy_infos']['labels']['k8s.webserver/name'] = w_name        
    try:
        data['service_infos']['labels']['k8s.webserver/name'] = w_name
    except KeyError:
        data['service_infos']['labels'] = {}
        data['service_infos']['labels']['k8s.webserver/name'] = w_name
    
    data['deploy_infos']['annotations']['k8s.webserver/workload'] = w_name
    try:
        data['service_infos']['annotations']['k8s.webserver/workload'] = w_name
    except KeyError:
        data['service_infos']['annotations'] = {}
        data['service_infos']['annotations']['k8s.webserver/workload'] = w_name
    # data['ingress_infos']['annotations']['k8s.webserver/workload'] = w_name
    # data['ingress_infos']['labels']['k8s.webserver/workload'] = w_name
   
    # 名称处理
    data['service_infos']['name'] = w_name
    # data['ingress_infos']['name'] = w_name

    # # dry_run 并得到结果（需要格式化，但还没测试）
    # deploy_res = create_namespaced_deployment(data['namespace'],data['deploy_infos'],data['containers'],pod_infos=data['pod_infos'])
    try:
        service_res = create_namespaced_service(data['namespace'],data['service_infos'],True)
        print(service_res)
    except client.exceptions.ApiException as err:
        print(format_create_failure(err))
    # print(deploy_res)