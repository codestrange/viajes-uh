<template>
    <div id="user">
        <b-input-group style="margin-bottom: 10px">
            <b-form-input id="username" v-model.trim="username" :state="state_input">
            </b-form-input>
        </b-input-group>
        <b-input-group style="margin-bottom: 10px">
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
        name: "User"
    }
</script>