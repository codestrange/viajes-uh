<template>
    <div id="userView">
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
                this.$store.state.user.getUserData().then(user => this.user = user);
            },
        },
        mounted() {
            this.loadUserData();
        },
    }
</script>