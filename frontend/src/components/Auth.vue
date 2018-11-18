<template>
    <div id="auth">
        <b-input-group @keyup.enter="validateUser()" size="sm">
            <b-form-input placeholder="Usuario" v-model="username" ></b-form-input>
        </b-input-group>
        <b-input-group @keyup.enter="validateUser()" size="sm">
            <b-form-input placeholder="Contraseña" type="password" v-model="password" ></b-form-input>
        </b-input-group>
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
            this.$store.state.user.token = this.getToken(this.username, this.password);
        },
        getToken(username, password) {
            return 'mock_token';
        },

    },
}
</script>
