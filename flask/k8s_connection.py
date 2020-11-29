from kubernetes import client,config
from kubernetes import watch as _watch
import yaml
# import datetime
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
        for event in w.stream(api.list_namespaced_deployment,namespace=namespace):
            # print(event)
            deploy = format_deployment_event(event)
            for key,value in deploy.items():
                print(key,value)
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
            new_deployment = Deployment(name=deploy['name'],ready=deploy['ready'],
                            uptodate=deploy['uptodate'],available=deploy['available'],
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


def create_namespaced_deployment(name, containers, namespace, labels=[], replicas=1, volumes={}, service={}, ingress={}):
    '''
    创建deployment
    '''
    res = []
    with open('./template.yml') as f:
        res = yaml.safe_load(f.read())

    #name 字段
    res['metadata']['name'] = name
    res['metadata']['labels']['app'] = name
    res['spec']['selector']['matchLabels']['app'] = name
    res['spec']['template']['metadata']['labels']['app'] = name

    # containers 字段
    for i,container in enumerate(containers):
        res['spec']['template']['spec']['containers'][i]['image']=container['image']
        if 'name' in container:
            res['spec']['template']['spec']['containers'][i]['name']=container['name']
        else:
            res['spec']['template']['spec']['containers'][i]['name']=container['image']

    # print(res)
    
    api = client.AppsV1Api()
    response = api.create_namespaced_deployment(namespace,res)
    print(response)

def delete_namespaced_deployment(name, namespace):
    '''
    删除给定命名空间下的deployment
    name: string deployment的名字
    namespace: string namespace的名字
    ret: 错误代码 0成功 1异常
    '''
    api = client.AppsV1Api()
    try:
        res = api.delete_namespaced_deployment(name,namespace)
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




if __name__ == '__main__':
    k8sInitial()
    # list_all_namespaces()
    # list_namespaced_deployment(watch=True)
    list_deployment_for_all_namespaces()
    # create_namespaced_deployment('test1',[{'image':'nginx'}],'default')
    # print(delete_namespaced_deployment('test1','default'))