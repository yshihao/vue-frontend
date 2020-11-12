import axios from 'axios';
import Config from '@/config/index'
//some configs
const service = axios.create({
    timeout: 1500000,
    baseURL: Config.baseUrl
});

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
