#coding=utf-8
from flask import Flask, make_response, request
from flask_cors import CORS
from mysql import init
import json
import pymysql
import k8s_connection
import datetime
import os

app = Flask(__name__)
#解决跨域请求
CORS(app,supports_credential=True)

# 生成数据包
def gen_DataPack(codestatus):
    rsp = make_response("Response Page")
    rsp.status = codestatus
    rsp.headers['Connection'] = 'Keep-Alive'
    rsp.headers['Accept-Language'] = 'zh-CN'
    rsp.headers['Accept'] = 'text/html, application/xhtml+xml, */*'
    return rsp
@app.route('/api/file/send_yaml',methods=['post','get'])
def test():
    isRight=True #出现错误时设为false
    data = request.get_json(silent=True)
    datap = data['keys']
    datap = datap.encode('utf-8')
    # file = open('file.txt','w')
    # file.write(datap)
    print(datap)

    if isRight:
        rsp = gen_DataPack('200')
        value = {'tag': 0, 'data': "you have success"}
        rsp.headers['res'] = {'code':200,'data':value}
        return rsp
    else:
        rsp = gen_DataPack('404')
        value = {'tag': 1, 'data': "something wrong"}
        rsp.headers['res'] = {'code':404,'data':value}
        return rsp
        
@app.route('/api/deployment/list',methods=['get'])
def deployment_list():
    deployments = k8s_connection.list_namespaced_deployment()
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
@app.route('/api/addcontainer',methods=['post','get'])
def add_container():
    containername = request.args.get('containername')
    imagename = request.args.get('imagename')
    # print(containername, imagename)
    # print(os.getcwd())
    k8s_connection.create_namespaced_deployment(containername,[{'image':imagename}],'default')
    return {
        "code":200
    }

@app.route('/api/net/list', methods=['get'])
def network_list():
    return {
        "code": 200,
        "data": ['network_2S','network_3S']
    }
@app.route('/api/net/topology', methods=['get'])
def network_topology():
    return {
        "code": 200,
        "data": 'links:\n  - endpoints: ["sw-1:eth0","sw-2:eth0","sw-3:eth0","usr-1:eth0","usr-2:eth0","usr-3:eth0","ctr-1:eth0"]\n    driver: bridge\n  - endpoints: ["sw-1:eth1", "usr-1:eth1"]\n  - endpoints: ["sw-2:eth1", "usr-2:eth1"]\n  - endpoints: ["sw-3:eth1", "usr-3:eth1"]\n  - endpoints: ["sw-1:eth2", "sw-2:eth2"]\n  - endpoints: ["sw-1:eth3", "sw-3:eth2"]\n  - endpoints: ["sw-1:eth4", "ctr-1:eth1"]\nVERSION: 2\ndriver: veth\nPREFIX: 1S\nCONF_DIR: ./config\nMY_IMAGE: "tovs:1.1.4"\nPUBLISH_BASE: 9005\nSUBNET: "10.31.100.0/24"\nGATEWAY: "10.31.100.254:\nAUX_ADDRESSES:["10.31.100.1", "10.31.100.2"]'
    }

@app.route('/api/net/info', methods=['get'])
def docker_list():
    phy = request.args.get('netName')
    userid = request.args.get('userid')
    types = request.args.get('type')
    sql1 = ""
    print(types)
    if types=="phy":
        sql1 = "select dockerid,dockerimage,dockername,dockercommand,dockercreatetime from infos where uid=%s and phy=%s"
    elif types=="net":
        sql1 = "select dockerid,dockerimage,dockername,dockercommand,dockercreatetime from infos where uid=%s and vlanid=%s"
    cursor = conn.cursor()
    cursor.execute(sql1,[userid,phy])
    results = (cursor.fetchall())
    print(results)
    alldocker = []
    if results:
        for i in range(len(results)):
            docker = {
            'id': str(results[i][0]),
            'image': str(results[i][1]),
            'name': str(results[i][2]),
            'command': str(results[i][3]),
            'created': str(results[i][4])
            }
            alldocker.append(docker)
    cursor.close()       
    return {
        "code": 200,
        "data": alldocker
    }


@app.route('/api/data_centers/info', methods=['get'])
def data_centers_info():
    uid = request.args.get("userid")
    #uid =1
    sql1 = "select dc from infos where uid=%s"%(uid)
    cursor = conn.cursor()
    cursor.execute(sql1)
    results = cursor.fetchall()
    if results:
        results = list(results)
        for i in range(len(results)):
            results[i] = str(results[i][0])
    cursor.close()
    result = []
    for v in results:
        if v not in result:
            result.append(v)
    return {
        "code": 200,
        "data": result
    }
# get details in one particular data center
@app.route('/api/data_centers/server_and_nets', methods=['get'])
def server_and_nets():
    DC = request.args.get('dataCenter')
    uid = 1
    sql1 = "select phy,vlanid from infos where uid=%s and dc=%s"
    cursor = conn.cursor()
    cursor.execute(sql1,[uid,DC])
    results = cursor.fetchall()
    servers = []
    subnets = []
    if results:
        results = list(results)
        for i in range(len(results)):
            servers.append(str(results[i][0]))
            subnets.append(str(results[i][1]))
    cursor.close()
    server = []
    subnet = []
    for v in servers:
        if v not in server:
            server.append(v)
    for v in subnets:
        if v not in subnet:
            subnet.append(v)
    return {
        "code": 200,
        "data": {
            "servers":server,
            "nets":subnet
        }
    }


@app.route('/api/net/device/info', methods=['get'])
def docker_device_info():
    print(request.args)
    device_info = {
            'Architecture': 'x86',
            'CPU op-mode(s)': '32 bit',
            'Byte Order': 'little endian',
            'CPU(s)': '20',
            'On-line CPU(s) list': 'd',
            'Thread(s) per core': '1',
            'Core(s) per socket': 10,
           'Socket(s)': 2,
            'NUMA node(s)': 2,
            'Vendor ID': 'dd',
            'CPU family': 6,
            'Model': 79,
            'Model name': 'inter(r) Xeon(R) CPU E5-2630 v4',
            'Stepping': 1,
            'CPU Mhz': 1200.232,
            'CPU max MHz': 2200.0,
            'CPU min MHz': 1200.0,
            'BogoMIPS': 4399.78,
            'Virtualiztion': 'VT-x',
            'L1d cache': '32k',
            'L1i cache': '32k',
            'L2 cache': '256k',
            'L3 cache': '25600k',
            'NUMA node0 CPU(s)': '0,2,4',
           'NUMA node1 CPU(s)': '1,3,5'
    }
    return {
        "code": 200,
        "data": device_info
    }
if __name__ == '__main__':
    # conn = init()
    k8s_connection.k8sInitial()
    app.run(debug=True,port=5000)
    # conn.close()
