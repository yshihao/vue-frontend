from kubernetes import client,config,watch
import datetime
import yaml

def k8sInitial():
    '''
    初始化，加载配置
    '''
    # config.load_kube_config(config_file="./config")
    conf = client.Configuration()
    conf.host = 'http://192.168.1.199:40004'

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
        w = watch.Watch()
        for event in w.stream(api.list_namespaced_deployment,namespace=namespace):
            # print(event)
            return event
    else:
        res = api.list_namespaced_deployment(namespace, pretty='true')
        # print(res)
        return res

def create_namespaced_deployment(name, containers, namespace, labels=[], replicas=1, volumes={}, service={}, ingress={}):
    '''
    '''
    res = []
    with open('/home/werthy/Web/vue-frontend/mybackend/template.yml') as f:
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
    return response
    # print(response)

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



if __name__ == '__main__':
    k8sInitial()
    # list_all_namespaces()
    res=list_namespaced_deployment()
    # create_namespaced_deployment('test1',[{'image':'nginx'}],'default')
    # print(delete_namespaced_deployment('test1','default'))
    
    # # deploy-list test
    # today = datetime.date.today()
    # # age = today.__sub__(res.items[0].metadata.creation_timestamp.date())
    # # print(type(res.items[0].metadata.creation_timestamp),age.days)
    # result = []
    # for deploy in res.items:
    #     v = {}
    #     v['name'] = deploy.metadata.name
    #     v['ready'] = '{}/{}'.format(deploy.status.ready_replicas,deploy.status.replicas)
    #     v['uptodate'] = '{}'.format(deploy.status.updated_replicas)
    #     v['available'] = '{}'.format(deploy.status.available_replicas)
    #     age = today.__sub__(deploy.metadata.creation_timestamp.date())
    #     v['age'] = '{}天'.format(age.days)
    #     result.append(v)
    #     # print(v)
    # print(result)