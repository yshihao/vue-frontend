import axios from 'axios';
//some configs
const service = axios.create({
    timeout: 1500000,
    baseURL: 'http://localhost:5000'
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
    getDockerList(netName) {
        return service({
            url: 'api/net/info',
            method: 'get',
            params: {
                netName
            }
        });
    },
    getDockerDevice(dockName) {
        return service({
            url: 'api/net/device/info',
            method: 'get',
            params: {
                dockName
            }
        });
    },
    //get data centers list
    getDataCenters() {
        return service({
            url: 'api/data_centers/info',
            method: 'get'
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
