import axios from 'axios';

//some configs
const service = axios.create({
    timeout: 1500000
});

export default {
    //send the formatted file to the server
    sendYaml(data) {
        return service({
            url: 'api/file/send_yaml',
            method: 'post',
            data: data
        });
    }
};
