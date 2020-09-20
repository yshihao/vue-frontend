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


if __name__ == '__main__':
    app.run(debug=True,port=5000)
