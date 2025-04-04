<template>
    <div>
        <h1>ola, meu nome é {{ nome }}</h1>
    </div>
</template>

<script>
    export default {
        name: 'LifeCycle',
        data() {
            return {
                nome: 'ainda não sei'
            }
        },
        created() {
            this.nome = 'Kaique'
        }
    }
</script>