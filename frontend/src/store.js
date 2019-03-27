import Vue from 'vue';
import Vuex from 'vuex';
import ProfileController from './controllers/profile';
import RoutesController from './controllers/routes';

Vue.use(Vuex);

const store = new Vuex.Store({
    state: {
        profile: ProfileController,
        routes: RoutesController
    },
    mutations: {},
    actions: {}
});

export default store;
