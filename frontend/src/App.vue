<template>
<div id="app">
    <b-navbar toggleable="md" type="dark" variant="primary">
        <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
        <b-navbar-brand href="#">UH Travels</b-navbar-brand>
        <b-collapse is-nav id="nav_collapse">   
            <b-navbar-nav>
            <b-nav-item @click="changeTab('home')"><strong>Home</strong></b-nav-item>
            <b-nav-item @click="changeTab('travels')" v-if="isUserLogged()"><strong>Viajes</strong></b-nav-item>
            <b-nav-item-dropdown v-if="isUserLogged()">
                <template slot="button-content">
                    <strong>Administración</strong>
                </template>
                <b-dropdown-item @click="changeTab('admin-user')">Usuarios</b-dropdown-item>
            </b-nav-item-dropdown>
            </b-navbar-nav>
            <b-navbar-nav class="ml-auto">
                <b-nav-item-dropdown right v-if="isUserLogged()">
                    <template slot="button-content">
                    <strong>Mi Usuario</strong>
                    </template>
                    <b-dropdown-item @click="changeTab('user-view')">Perfil</b-dropdown-item>
                    <b-dropdown-item @click="logoutUser()">Cerrar Sesión</b-dropdown-item>
                </b-nav-item-dropdown>
                <b-nav-item-dropdown right v-else>
                    <template slot="button-content">
                    <strong>Iniciar Sesión</strong>
                    </template>
                    <auth/>
                </b-nav-item-dropdown>
            </b-navbar-nav>
        </b-collapse>
    </b-navbar>
    <div id="loader">
        <loading v-if="this.$store.state.loader.showing"></loading>
    </div>
    <div id="content" class="container-fluid">
        <component :is="activeView"></component>
    </div>
</div>
</template>

<script>
import Home from '@/views/Home.vue';
import Travels from '@/views/Travels.vue';
import AdminUser from '@/views/AdminUser.vue';
import UserView from '@/views/UserView.vue';
import Auth from '@/components/Auth.vue';
import Loading from '@/components/Loading.vue';

export default {
    name: 'app',
    components: {
        Home,
        Travels,
        AdminUser,
        Auth,
        UserView,
        Loading,
    },
    data() {
        return {
            activeView: 'home',
        };
    },
    methods: {
        changeTab(newTab) {
            this.activeView = newTab;
            localStorage.setItem('uh-travel-active_view', this.activeView);
        },
        isUserLogged() {
            //This should check if the user is logged with the controller
            //by asking if the token is valid
            return this.$store.state.user.isLogued();
        },
        logoutUser() {
            //This should logout the user and notify to the server
            this.$store.state.user.logOut();
            localStorage.setItem('uh-travel-user_data', this.$store.state.user.getMinData());
            this.changeTab('home');
        },
    },
    mounted() {
        if(localStorage.getItem('uh-travel-user_data') !== null) {
            this.$store.state.user.reloadMinData(JSON.parse(localStorage.getItem('uh-travel-user_data')));
        }
        if(localStorage.getItem('uh-travel-active_view')) {
            this.activeView = localStorage.getItem('uh-travel-active_view');
        }
    },
    updated() {
        localStorage.setItem('uh-travel-user_data', this.$store.state.user.getMinData());
        localStorage.setItem('uh-travel-active_view', this.activeView);
    },
}
</script>