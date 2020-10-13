#coding=utf-8
from flask import Flask, make_response, request
from flask_cors import CORS
import json
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
    print(request.args)
    docker = {
            'id': 'dockerid',
            'image': 'dockerimage',
            'name': 'docker1',
            'command': '/bin/bash',
            'created': 'createdtime'
    }
    alldocker = [docker,docker]
    return {
        "code": 200,
        "data": alldocker
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
# get data centers
@app.route('/api/data_centers/info', methods=['get'])
def data_centers_info():
    return {
        "code": 200,
        "data": ['Center1','Center2','Center3']
    }
# get details in one particular data center
@app.route('/api/data_centers/server_and_nets', methods=['get'])
def server_and_nets():
    print(request.args)
    return {
        "code": 200,
        "data": {
            "servers": ["server1","server2"],
            "nets": ["net-2S","net-3S"]
        }
    }

if __name__ == '__main__':
    app.run(debug=True,port=5000)
