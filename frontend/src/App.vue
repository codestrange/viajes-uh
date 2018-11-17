<template>
<div id="app">
    <b-navbar toggleable="md" type="dark" variant="primary">
        <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
        <b-navbar-brand href="#">UH Travels</b-navbar-brand>
        <b-collapse is-nav id="nav_collapse">   
            <b-navbar-nav>
            <b-nav-item @click="changeTab('home')">Home</b-nav-item>
            <b-nav-item @click="changeTab('travels')">Viajes</b-nav-item>
            <b-nav-item @click="changeTab('admin')">Administración</b-nav-item>
            </b-navbar-nav>
            <b-navbar-nav class="ml-auto">
                <b-nav-item-dropdown right v-if="user_token != ''">
                    <template slot="button-content">
                    <strong>Mi Usuario</strong>
                    </template>
                    <b-dropdown-item>Perfil</b-dropdown-item>
                    <b-dropdown-item>Cerrar Sesión</b-dropdown-item>
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
    <div id="content" class="container-fluid">
        <home v-if="activeTab == 'home'"/>
        <travels v-else-if="activeTab == 'travels'"/>
        <admin v-else-if="activeTab == 'admin'"/>
    </div>
   
</div>
</template>

<script>
import Home from '@/views/Home.vue';
import Travels from '@/views/Travels.vue';
import Admin from '@/views/Admin.vue';
import Auth from '@/components/Auth.vue';
import { authBus } from '@/main.js';

export default {
    name: 'app',
    components: {
        Home,
        Travels,
        Admin,
        Auth,
    },
    data() {
        return {
            activeTab: 'home',
            user_token: '',
        }
    },
    methods: {
        changeTab(newTab) {
            this.activeTab = newTab;
        }
    },
    created() {
        authBus.$on('user_authenticated', (data) => {
            console.log(data.token);
            this.user_token = data.token;
        })
    },
}
</script>

<style>
#content {
    margin: 10pt;
}
</style>
