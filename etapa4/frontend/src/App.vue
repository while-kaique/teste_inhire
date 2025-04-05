<template>
  <div id="app">
    <header>
      <p>Olá, você está no</p>
      <h1>Sistema de Operadoras de Saúde</h1>
    </header>
    <main>
      <SearchOperadoras />
    </main>
  </div>
</template>

<script>
import SearchOperadoras from './components/SearchOperadoras.vue'

export default {
  name: 'App',
  components: {
    SearchOperadoras
  }
}
</script>

<style>
#app {
  font-family: 'Poppins', sans-serif;
  font-size: 200;
  color: #b0d8ff;

  width: 100%;

  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

header {
  width: 78%;
  text-align: left;
  font-size: 1.6rem;
  color: #A6BBCC;
  font-weight: 900;
  margin-bottom: 40px;
}

header p{
  color: white;
  font-weight: 100;
  font-size: 1rem;
  padding-left: 3px;
}

main {
  min-width: 100%;
}
</style>