import Vue from 'vue';
import App from './App.vue';
import store from './store/index.js';
import router from './router/index.js';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import less from 'less';

Vue.use(ElementUI);
Vue.use(less);
//入口文件
new Vue({
    el: '#app',
    store: store,
    router: router,
    render: c => c(App)
});
