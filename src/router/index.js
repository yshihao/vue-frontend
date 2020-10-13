import Vue from 'vue';
import VueRouter from 'vue-router';
import CreateNet from '../pages/CreateNet.vue';
import NotFound from '../pages/errors/NotFound';
import NetworkInfo from '../pages/NetworkInfo';
import NetList from '../components/network/NetList';
import Dock from '../components/network/Dock';
import Device from '../components/network/Device';
import DockerImages from '../pages/DockerImages';
import DataCenters from '../pages/DataCenters';
import ServerAndNets from '../components/DataCenter/ServerAndNets';

Vue.use(VueRouter);

const originalPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
    return originalPush.call(this, location).catch(err => err);
};

const routes = [
    {
        path: '/',
        redirect: '/docker_images'
    },
    {
        path: '/create_net',
        name: 'CreateNet',
        component: CreateNet
    },
    {
        path: '/docker_images',
        name: 'DockerImages',
        component: DockerImages
    },
    {
        path: '/data_centers',
        name: 'DataCenters',
        component: DataCenters,
        children: [
            {
                path: ':datacenter',
                name: 'ServerAndNets',
                component: ServerAndNets
            }
        ]
    },
    {
        path: '/network_info',
        // name: 'NetworkInfo',
        component: NetworkInfo,
        children: [
            { path: '/', name: 'NetList', component: NetList },
            {
                path: ':netName/docker_list',
                name: 'DockerList',
                component: Dock
            },
            {
                path: ':netName/docker_list/device/:deviceName',
                name: 'DeviceInfo',
                component: Device
            }
        ]
    },
    {
        path: '*',
        name: '404',
        component: NotFound
    }
];

const router = new VueRouter({
    mode: 'history',
    routes
});

export default router;
