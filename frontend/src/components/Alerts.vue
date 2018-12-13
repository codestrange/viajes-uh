<template>
    <div id="alerts-shower">
        <b-alert show v-bind:variant="this.type" style="text-align: center;">{{this.text}}</b-alert>
    </div>
</template>

<script>
    export default {
        name: "Alerts",
        props: {
            text: String,
            type: String,
        },
    }
</script>
