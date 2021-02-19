import axios from 'axios';
import Config from '@/config/index'
import store from '../store';
import router from '@/router/index.js';
//some configs

const service = axios.create({
    timeout: 1500000,
    baseURL: Config.baseUrl
});
service.interceptors.request.use(function (config) {
    let token = localStorage.getItem('Authorization');
    if (token) {
         config.headers['accessToken'] = token;
    }
    return config;
}, function (error) {
    // Do something with request error
    return Promise.reject(error);
});
service.interceptors.response.use(function(response){
    let status = response.status;
    return response;
},function(error){
    if(error.response){
        switch(error.response.status){
            case 401:
                store.commit('del_token')
                alert("登陆过期，重新登陆")
                router.push('/login')
            break;
        }
    }
})
export default {
    //send the formatted file to the server
    sendYaml(data) {
        //console.log(data)
        //console.log(data['driver'])
        return service({
            url: '/api/file/send_yaml',
            method: 'post',
            data: {
                keys: data
            }
        });
    },
    addDeployment(deploy_infos,containers) {
        return service({
            url:'/api/addDeploymentTest',
            method:'post',
            data:{
                deploy_infos:deploy_infos,
                containers:containers
            }
        })
    },
    addDeploymentTest(form) {
        return service({
            url:'/api/addDeploymentTest',
            method:'post',
            data:{
                type:'test',
                form:form
            }
        })
    },
    requestLogin(username,password) {
        return service({
            url:'/login',
            method:'post',
            data:{
                username:username,
                password:password,
            }

        })
    },
    getusername() {
        return service({
            url:'/get/username',
            method:'get'
        })
    },
    registerUser(username,password){
        return service({
            url:'/register',
            method:'post',
            data:{
                username:username,
                password:password,
            }

        })
    },
    getDeploymentList() {
        return service({
            url:'api/deployment/list',
            method:'get'
        });
    },
    addContainer(containername,imagename) {
        return service({
            url:'/api/addcontainer',
            methods:'post',
            params:{
                containername,
                imagename
            }
        })
    },
    //get network info from the server
    getNetworkInfo() {
        return service({
            url: '/api/net/list',
            method: 'get'
        });
    },
    getNetTopo(netName) {
        return service({
            url: '/api/net/topology',
            method: 'get',
            params: {
                netName
            }
        });
    },
    getDockerList(netName,userid,type) {
        return service({
            url: 'api/net/info',
            method: 'get',
            params: {
                netName,
                userid,
                type
            }
        });
    },
    getDockerDevice(dockName) {
        return service({
            url: 'api/net/device/info',
            method: 'get',
            params: {
                dockName,
            }
        });
    },
    //get data centers list
    getDataCenters(userid) {
        return service({
            url: 'api/data_centers/info',
            method: 'get',
            params:{
                userid
            }
        });
    },
    //get details in one particular data center
    getServerAndNets(dataCenter) {
        return service({
            url: 'api/data_centers/server_and_nets',
            method: 'get',
            params: {
                dataCenter
            }
        });
    }
};
