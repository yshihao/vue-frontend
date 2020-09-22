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
    getDockerList(netName) {
        return service({
            url: 'api/net/info',
            method: 'get',
            params: {
                netName
            }
        });
    }
};
