import Vue from 'vue';
import Vuex from 'vuex';
import App from './App.vue';
import BootstrapVue from 'bootstrap-vue';
import UserController from './controllers/user';
import Loader from './store/loading';
import Notify from './store/notification';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

Vue.use(Vuex);
Vue.use(BootstrapVue);
Vue.config.productionTip = false;

const store = new Vuex.Store({
    state: {
        user: UserController,
        loader: Loader,
        notify: Notify,
    }
})

new Vue({
    store,
    render: h => h(App),
}).$mount('#app');