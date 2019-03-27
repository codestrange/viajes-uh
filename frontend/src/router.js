import Vue from 'vue';
import Router from 'vue-router';
import Home from './components/Home';
import Login from './views/Login';
import Nav from './views/Nav';
import NotFound from './views/NotFound';
import Profile from './components/Profile';
import Register from './views/Register';
import Store from './store';


Vue.use(Router);

const checkforAuth = (to, from, next) => {
    if (to.matched.some(route => route.meta.requiresAuth)) {
        Store.state.profile.loadMinData();
        if (Store.state.profile.isLogued() === false) {
            next({name: 'loginPage'});
        }
    }
};

const router = new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        //Redirections
        {
            path: '/',
            redirect: {name: 'homePage'},
        },
        //Redirections
        {
            path: '/nav',
            name: 'navPage',
            component: Nav,
            meta: {
                requiresAuth: true
            },
            children: [
                {
                    path: '/home',
                    name: 'homePage',
                    component: Home,
                    meta: {
                        requiresAuth: true
                    }
                },
                {
                    path: '/profile',
                    name: 'profilePage',
                    component: Profile,
                    meta: {
                        requiresAuth: true
                    }
                }
            ]
        },
        {
            path: '/login',
            name: 'loginPage',
            component: Login,
            beforeEnter(to, from, next) {
                Store.state.profile.loadMinData();
                if (Store.state.profile.isLogued() === true) {
                    next({ name: Store.state.routes.getLast() });
                }
                next();
            }
        },
        {
            path: '/register',
            name: 'registerPage',
            component: Register
        },
        {
            path: '*',
            name: 'notFoundPage',
            component: NotFound
        }
    ]
});

router.beforeEach((to, from, next) => {
    checkforAuth(to, from, next);
    next();
});

router.afterEach((to, from) => {
   Store.state.routes.updateLast(from.name);
});

export default router;
