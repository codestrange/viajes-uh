<template>
    <div id="auth">
        <strong>Usuario:</strong>
        <input type="text" id="usernameInput" v-model="username" @keyup.enter="validateUser()"/>
        <strong>Contraseña:</strong>
        <input type="password" id="passwordInput" v-model="password" @keyup.enter="validateUser()"/>
    </div>   
</template>

<script>
export default {
    name:'Auth',
    data() {
        return {
            username:'',
            password:'',
        }
    },
    methods: {
        validateUser() {
            console.log('Username:' + this.username + ' Password:' + this.password);
            //Now we should connect to the server and try to get the validation
            //For now we would use a mock response
            let user_token = this.getToken(this.username, this.password);
            //Storing the token in the app state
            this.$store.state.user.token = 'mock_token';
        },
        getToken(username, password) {
            return 'mock_token';
        },

    },
}
</script>
