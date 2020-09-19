import axios from 'axios';
//some configs
const service = axios.create({
    timeout: 1500000
});

export default {
    //send the formatted file to the server
    sendYaml(data) {
        //console.log(data)
        //console.log(data['driver'])
        return service({
            url: 'http://192.168.1.60:20000/api/file/send_yaml',
            method: 'post',
            data: {
                keys: data
            }
        });
    }
};
