import Vue from 'vue';
import VueRouter from 'vue-router';
import CreateNet from '../pages/old/CreateNet.vue';
import NotFound from '../pages/errors/NotFound';
import NetworkInfo from '../pages/old/NetworkInfo';
import NetList from '../components/old/network/NetList';
import Dock from '../components/old/network/Dock';
import Device from '../components/old/network/Device';
import DockerImages from '@/pages/old/DockerImages';
import DataCenters from '../pages/old/DataCenters';
import ServerAndNets from '../components/old/DataCenter/ServerAndNets';
import Login from '../pages/users/Login';
import Register from '../pages/users/Register';
import Home from '@/pages/Home';
import Deploy from '@/components/Deployment/Deploy';
import layout from '@/components/createDeploy/layout';
Vue.use(VueRouter);

const originalPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
    return originalPush.call(this, location).catch(err => err);
};

const routes = [
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/register',
        name: 'register',
        component: Register
    },
    {
        path: '/home',
        name: 'Home',
        component: Home,
        meta: {
            requireAuth: true
        },
        children: [
            {
                path: '/home/deploy',
                name: 'Deploy',
                component: Deploy,
                meta: {
                    requireAuth: true
                }
            },
            {
                path: '/home/createdeploy',
                name: 'createDeploy',
                component: layout,
                meta: {
                    requireAuth: true
                }
            }
        ]
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
        component: DataCenters
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
/*
router.beforeEach((to,from,next)=>{
    let flag = sessionStorage.getItem('Authorization')

    if(to.meta.requireAuth == true){ 
        if(!flag){                   
            next({
                path: '/login'
            })
        }else{                       
            return next();
        }
    }else{                          
        return next();
    }
})*/
export default router;
