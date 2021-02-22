import Vue from 'vue';
import Vuex from 'vuex';
import windowState from './windowState';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        Authorization: localStorage.getItem('Authorization')
            ? localStorage.getItem('Authorization')
            : ''
    },
    mutations: {
        changeLogin(state, user) {
            state.Authorization = user.Authorization;
            localStorage.setItem('Authorization', user.Authorization);
        },
        del_token(state) {
            state.Authorization = '';
            localStorage.removeItem('Authorization');
        }
    },
    actions: {},
    modules: {
        windowState
    }
});
