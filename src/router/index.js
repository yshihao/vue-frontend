import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../components/Home.vue';
import NotFound from '../components/errors/NotFound';
import NetworkInfo from '../components/NetworkInfo';
import NetList from '../components/network/NetList';

Vue.use(VueRouter);

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
        name: 'NetworkInfo',
        component: NetworkInfo,
        children: [{ path: '/', name: 'NetList', component: NetList }]
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
