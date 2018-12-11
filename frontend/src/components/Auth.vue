<template>
    <div id="auth">
        <b-input-group @keyup.enter="validateUser()" size="sm" style="margin-bottom: 10px">
            <b-form-input id="username"  placeholder="Usuario" v-model.trim="username" :state="state_input">
            </b-form-input>
        </b-input-group>
        <b-input-group @keyup.enter="validateUser()" size="sm" style="margin-bottom: 10px">
            <b-form-input placeholder="Contraseña" type="password" v-model="password" :state="state_input">
            </b-form-input>
        </b-input-group>
        <b-input-group>
            <b-button type="submit" variant="primary" block @click="validateUser()">Iniciar</b-button>
        </b-input-group>
    </div>
</template>

<script>
    export default {
        name: 'Auth',
        data() {
            return {
                username: '',
                password: '',
                state_input: null,
            }
        },
        methods: {
            validateUser() {
                this.getToken(this.username, this.password);
            },
            getToken(username, password) {
                this.$store.state.user.authenticateUser(username, password)
                    .then(result => {
                        if(result === false) {
                            this.state_input = false;
                            setTimeout(() => this.state_input = null, 1000);
                        }
                    });
            }
        },
    }
</script>
<style>
    #auth {
        padding: 10px;
    }
</style>