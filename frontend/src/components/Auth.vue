<template>
    <div id="auth">
        <b-input-group @keyup.enter="validateUser()" size="sm">
            <b-form-input placeholder="Usuario" v-model.trim="username" :state="!wrong_input">
            </b-form-input>
        </b-input-group>
        <b-input-group @keyup.enter="validateUser()" size="sm">
            <b-form-input placeholder="Contraseña" type="password" v-model="password" :state="!wrong_input">
            </b-form-input>
        </b-input-group>
    </div>
</template>

<script>
    import UserController from '@/controllers/user';

    export default {
        name: 'Auth',
        data() {
            return {
                username: '',
                password: '',
                wrong_input: false,
            }
        },
        methods: {
            validateUser() {
                this.getToken(this.username, this.password);
            },
            getToken(username, password) {
                UserController.getToken(username, password)
                    .then(json => {
                        if (json.token != null) {
                            this.$store.state.user.token = json.token;
                        }
                        else {
                            console.log(json.error + ':' + json.message);
                            this.wrong_input = true;
                            setTimeout(() => this.wrong_input = false, 1000);
                        }
                    });
            }
        },
    }
</script>
