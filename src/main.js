import Vue from 'vue';
import App from './App.vue';
import axios from 'axios';
import store from './store/index.js';
import router from './router/index.js';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import less from 'less';
import service from '@/api/api'
Vue.use(ElementUI);
Vue.use(less);

router.beforeEach((to,from,next)=>{
    console.log("yes applied")
    if(to.meta.requireAuth==true){
        let token = localStorage.getItem('Authorization');
        console.log(token);
        if(token){
            next()
        }else{
            next({path:'/login'})
        }
    }else{
        next()
    }
}),
//入口文件
new Vue({
    el: '#app',
    store: store,
    router: router,
    render: c => c(App)
});
