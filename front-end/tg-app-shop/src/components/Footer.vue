<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="row">
        <div class="col-6">
          <div class="company-info"> <!-- Блок информации о компании -->
            <p>&copy; {{ year }} <br>  6 O'clock Shop</p>
          </div>
        </div>
        <div class="col-6" style="border-left: 2px solid grey;"> <!-- Добавлена синяя линия слева -->
          <div class=""> <!-- Блок ссылок -->
            <ul class="footer-links">
              <li><router-link to="/about" class="navbar-link">О нас</router-link></li>
              <li><router-link to="/help" class="navbar-link">Помощь</router-link></li>
              <li><router-link to="/concierge" class="navbar-link">Консьерж-сервис</router-link></li> 
              <li><router-link to="/privacy-policy" class="navbar-link">Политика конфиденциальности</router-link></li>
              <li><router-link to="/terms-of-service" class="navbar-link">Условия использования</router-link></li>
            </ul>
          </div>
        </div>
      </div>
      
    </div>
  </footer>
</template> 


<script>
export default {
  name: 'Footer',
  data() {
    return {
      year: new Date().getFullYear()
    }
  }
}
</script>   


<style scoped>
.footer {
  background-color: #f8f9fa; /* Цвет фона */
  padding: 20px; /* Отступы */
  position: absolute; /* Относительное положение */
  bottom: NONE; /* Прижимаем к нижнему краю страницы */
  left: 0; /* Выравнивание по левому краю */
  right: 0; /* Выравнивание по правому краю */
}

.footer-links {
  list-style-type: none; /* Убираем маркеры списка */
  padding: 0; /* Убираем отступы */
  margin: 0; /* Убираем внешние отступы */
  width: 100%;
}

.navbar-link {
  margin: 5px 0; /* Увеличиваем вертикальный отступ между ссылками */
  color: #6c757d; /* Меняем цвет на серый */
  text-decoration: none; /* Убираем подчеркивание */
  font-size: 14px; /* Уменьшаем шрифт */
}

.navbar-link:hover {
  text-decoration: underline; /* Подчеркивание при наведении */
}

.company-info {
  text-align: left; /* Выравнивание текста по левому краю */
}

.footer img {
  max-width: 100px;
  height: auto;
}
</style>    