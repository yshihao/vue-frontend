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

def create_namespaced_deployment(namespace,deploy_infos, containers, volumes=[], pod_infos={'restartPolicy':'Always', 'serviceAccount':'default'}, initail_containers=[], dry_run = True):
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
    ret: -> 成功则是返回的yaml，失败则抛出ApiException异常并带有错误信息
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

    # volumes 字段 
    for i,volume in enumerate(volumes):
        volume_kind = volume['kind']
        if volume_kind == 'nfs':
            res['spec']['template']['spec']['volumes'][i]['nfs']['server'] = volume['nfsServer']
            res['spec']['template']['spec']['volumes'][i]['nfs']['path'] = volume['nfsPath']
        elif volume_kind == 'pvc':
            res['spec']['template']['spec']['volumes'][i]['persistentVolumeClaim']['claimName'] = volume['pvcName']
        elif volume_kind == 'hostPath':
            res['spec']['template']['spec']['volumes'][i]['hostPath']['path'] = volume['path']
            res['spec']['template']['spec']['volumes'][i]['hostPath']['type'] = volume['type']
        elif volume_kind == 'configMap':
            res['spec']['template']['spec']['volumes'][i]['configMap']['name'] = volume['configMap']
            res['spec']['template']['spec']['volumes'][i]['configMap']['items'] = volume['keyToPath']
        elif volume_kind == 'secret':
            res['spec']['template']['spec']['volumes'][i]['secret']['secretName'] = volume['secret']
            res['spec']['template']['spec']['volumes'][i]['secret']['items'] = volume['keyToPath']
        else:
            res['spec']['template']['spec']['volumes'][i] = None
            break
        # volume 的名称
        res['spec']['template']['spec']['volumes'][i]['name'] = volume['name']

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
    service_info: {'name':str name, 'annotations':dict annotation, 'labels':dict label, 'type':str type, 'ports':list port}
    dry_run: bool 是否是空跑
    ret: -> 成功则是返回的yaml，失败则抛出ApiException异常并带有错误信息
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
    创建给定命名空间的ingress
    namespace:str 命名空间的名称
    ingress_info: {'name':str name, 'annotations':dict annotation, 'labels':dict label, 'rules':dict rule, 'tls':dict tls}
    ret: -> 成功则是返回的yaml，失败则抛出ApiException异常并带有错误信息
    '''
    with open('./flask/template/ingress.yml') as f:
        body = yaml.safe_load(f.read())

    # 基本信息
    body['metadata']['name'] = ingress_info['name']
    body['metadata']['annotations'] = ingress_info['annotations']
    body['metadata']['labels'] = ingress_info['labels']

    # 配置信息
    if ingress_info['https']:
        body['spec']['tls']['hosts'][0] = ingress_info['host'] # 存疑，我得再研究一下
        body['spec']['tls']['secretName'] = ingress_info['tlsSecret']

    body['spec']['rules']['host'] = ingress_info['host']
    for i,rule in enumerate(rules):
        body['spec']['rules']['http']['paths'][i]['path'] = ingress_info['url']
        body['spec']['rules']['http']['paths'][i]['backend']['service']['name'] = ingress_info['serviceName']
        body['spec']['rules']['http']['paths'][i]['backend']['service']['port'] = ingress_info['port']

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

def database_test(user_id, file_id):
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


if __name__ == '__main__':
    k8sInitial()
    # list_all_namespaces()
    # list_namespaced_deployment(watch=True)
    # list_deployment_for_all_namespaces()
    print(create_namespaced_deployment('1',{'name':'ss','replicas':1,'labels':{},'annotations':{}},[{'image':'nginx', 'name':'test-pod', "imagePullPolicy":'Always'}]))
    # print(delete_namespaced_deployment('test1','default'))
    # database_test(0,1)