<template>
  <div class="filter-container mb-4">
    <div class="row g-3">
      <div class="col-md-3">
        <select v-model="filters.price_order" class="form-select" @change="applyFilters">
          <option value="">Сортировка по цене</option>
          <option value="asc">По возрастанию</option>
          <option value="desc">По убыванию</option>
        </select>
      </div>
      
      <div class="col-md-3">
        <select v-model="filters.size" class="form-select" @change="applyFilters">
          <option value="">Размер</option>
          <option v-for="size in sizes" :key="size" :value="size">{{ size }}</option>
        </select>
      </div>
      
      <div class="col-md-3">
        <select v-model="filters.brand" class="form-select" @change="applyFilters">
          <option value="">Бренд</option>
          <option v-for="brand in brands" :key="brand" :value="brand">{{ brand }}</option>
        </select>
      </div>
      
      <div class="col-md-3">
        <button class="btn btn-outline-secondary w-100" @click="resetFilters">
          Сбросить фильтры
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      filters: {
        price_order: '',
        size: '',
        brand: ''
      },
      sizes: ['S', 'M', 'L', 'XL', 'XXL'], // Можно загружать с бэкенда
      brands: ['Brand1', 'Brand2', 'Brand3'] // Можно загружать с бэкенда
    }
  },
  methods: {
    applyFilters() {
      this.$emit('filter', this.filters)
    },
    resetFilters() {
      this.filters = {
        price_order: '',
        size: '',
        brand: ''
      }
      this.applyFilters()
    }
  }
}
</script> 