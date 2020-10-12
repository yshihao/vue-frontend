import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../components/Home.vue';
import NotFound from '../components/errors/NotFound';
import NetworkInfo from '../components/NetworkInfo';
import NetList from '../components/network/NetList';
import Dock from '../components/network/Dock';
import Device from '../components/network/Device';

Vue.use(VueRouter);

const originalPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
    return originalPush.call(this, location).catch(err => err);
};

const routes = [
    {
        path: '/',
        redirect: '/create_net'
    },
    {
        path: '/create_net',
        name: 'CreateNet',
        component: Home
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
    // {
    //     path: '/DockInfo',
    //     name: 'DockInfo',
    //     component: Dock
    // },
    // {
    //     path: '/DeviceInfo',
    //     name: 'DeviceInfo',
    //     component: Device
    // },
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
