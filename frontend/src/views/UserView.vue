<template>
    <div id="userView" v-if="!this.$store.state.loader.showing">
        <h2>Nombre de Usuario:</h2>
        {{user.username}}
        <h2>Nombre Completo:</h2>
        {{user.fullname}}
        <h2>Correo Electronico:</h2>
        {{user.email}}
    </div>
</template>

<script>
    export default {
        name: "UserView",
        data() {
            return {
                user: {
                    username: 'Fallo',
                    fullname: 'Fallo',
                    email: 'Fallo',
                },
            };
        },
        methods: {
            loadUserData() {
                return this.$store.state.user.getUserData().then(user => {
                    this.user = user;
                });
            },
        },
        mounted() {
            this.$store.state.loader.showLoading();
            this.loadUserData().then( () => this.$store.state.loader.stopShowing() );
        },
    }
</script>