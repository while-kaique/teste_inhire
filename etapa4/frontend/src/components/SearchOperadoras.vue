<template>
    <div class="search-container">
      <!-- Campo de busca mantido igual -->
       <div class="barra_pesquisa">
        <input v-model="searchTerm" @input="handleSearch" placeholder="Buscar operadoras...">
        <button @click="handleSearch">Buscar Novamente</button>
       </div>
  
      <div class="while" v-if="loading">Carregando...</div>
    <div v-if="error" class="error">{{ error }}</div>
    
    <table v-if="results.data && results.data.length > 0">
      <thead>
        <tr>
          <th>Registro ANS</th>
          <th>Nome Fantasia</th>
          <th>Razão Social</th>
        </tr>
      </thead>
      <tbody>
        <!-- Correção aqui: results.data -->
        <tr v-for="item in results.data" :key="item.registro_ans">
          <td>{{ item.registro_ans }}</td>
          <td>{{ item.nome_fantasia }}</td>
          <td>{{ item.razao_social }}</td>
        </tr>
      </tbody>
    </table>

    <!-- Adicione esta mensagem para resultados vazios -->
    <div v-else-if="results.data && results.data.length === 0" class="while">
      Nenhum resultado encontrado para "{{ searchTerm }}"
    </div>

      
      <!-- Controles de paginação -->
      <div class="pagination" v-if="results.pagination">
        <button 
          @click="changePage(results.pagination.current_page - 1)"
          :disabled="!results.pagination.has_prev"
        >
          Anterior
        </button>
        
        <span>Página {{ results.pagination.current_page }} de {{ results.pagination.total_pages }}</span>
        
        <button 
          @click="changePage(results.pagination.current_page + 1)"
          :disabled="!results.pagination.has_next"
        >
          Próxima
        </button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        searchTerm: '',
        results: {},
        loading: false,
        error: null,
        currentPage: 1
      }
    },
    methods: {
      async handleSearch() {
        this.currentPage = 1 // Reset para a primeira página em novas buscas
        await this.fetchResults()
      },
      async changePage(page) {
        this.currentPage = page
        await this.fetchResults()
      },
      async fetchResults() {
        if (!this.searchTerm.trim()) {
          this.results = {}
          return
        }
        
        this.loading = true
        this.error = null
        
        try {
          const response = await fetch(
            `http://localhost:5000/api/operadoras?q=${encodeURIComponent(this.searchTerm)}&page=${this.currentPage}`
          )
          
          if (!response.ok) {
            throw new Error('Erro na busca')
          }
          
          this.results = await response.json()
        } catch (err) {
          this.error = err.message
          this.results = {}
        } finally {
          this.loading = false
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .search-container {
    margin: 0 auto;
    padding: 20px;
  }
  
  .search-box {
    display: flex;
    margin-bottom: 20px;
  }
  .barra_pesquisa {
    margin-bottom: 10px;
    display: flex;
    justify-content: center;
    width: 100%;
  }
  input {
    width: 60%;
    padding-left: 10px;
    height: 40px;
    font-size: 16px;
    border: none;
    border-top-left-radius: 4px;
    border-bottom-left-radius: 4px;
  }

  input:focus{
    outline: none;
    box-shadow: none;
  }
  
  button {
    width: 20%;
    height: 40px;
    background: #42b983;
    color: white;
    border: none;
    cursor: pointer;
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
  }
  button:hover{
    background-color: #3ca174;
  }

  .while {
    width: 100%;
    text-align: center;
  }
  
  table {
    width: 80%;
    margin:auto;
    border-collapse: collapse;
  }
  
  td{
    background-color: #ffff;
    color: black;
    border-right: 1px solid black;
  }

  th, td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #ddd;
    text-align: center;
  }
  
  th {
    color: black;
    background-color: #f2f2f2;
    border-right: 1px solid black;
  }
  
  .loading, .error {
    padding: 20px;
    text-align: center;
  }
  
  .error {
    color: red;
  }

  .pagination {
    display: flex;
    justify-content: space-between;
    padding-top: 15px;
    width: 80%;
    margin: auto;
  }
  .pagination button{
    border-radius: 4px;
  }
  </style>
