<template>
  <div class="about-us">
    <!-- Декоративные линии -->
    <div class="diagonal-lines"></div>
    
    <div class="container position-relative">
      <!-- Заголовок с анимацией -->
      <div class="header-section text-center mb-5">
        <h1 class="display-4 fw-bold">6 O'clock Shop</h1>
        <p class="lead text-muted">Ваш проводник в мире люксовой моды</p>
        <div class="accent-line"></div>
      </div>

      <!-- О нас секция -->
      <div class="content-section mb-5">
        <div class="row align-items-center">
          <div class="col-md-6">
            <div class="about-card">
              <h2 class="section-title">О нас</h2>
              <p class="section-text">
                Мы занимаемся поиском и подбором лучших модных предметов гардероба от ведущих люксовых брендов. 
                Наши байеры подбирают стильные и эксклюзивные вещи со всего мира и доставляют их прямо к вам домой.
              </p>
              <div class="highlight-box">
                <i class="bi bi-clock"></i>
                <p>Каждый новый дроп — ежедневно в 6:00 вечера</p>
              </div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="image-grid">
              <div class="grid-item"></div>
              <div class="grid-item"></div>
           
            </div>
          </div>
        </div>
      </div>

      <!-- Контакты секция -->
      <div class="contact-section">
        <h2 class="section-title text-center mb-4">Свяжитесь с нами</h2>
        <div class="row">
          <div class="col-md-6 mb-4">
            <div class="contact-card">
              <h3 class="card-title">Мессенджеры</h3>
              <div class="contact-links">
                <a href="https://wa.me/your-number" class="contact-link">
                  <i class="bi bi-whatsapp"></i>
                  <span>WhatsApp</span>
                  <small class="text-muted">+7 (911) 111-11-11</small>
                </a>
                <a href="https://t.me/your-telegram" class="contact-link">
                  <i class="bi bi-telegram"></i>
                  <span>Telegram</span>
                  <small class="text-muted">@sixoclockdrop</small>
                </a>
                <a href="mailto:six.oclock.drop@yandex.ru" class="contact-link">
                  <i class="bi bi-envelope"></i>
                  <span>Email</span>
                  <small class="text-muted">six.oclock.drop@yandex.ru</small>
                </a>
              </div>
            </div>
          </div>
          
          <!-- Форма обратной связи -->
          <div class="col-md-6">
            <div class="feedback-form">
              <h3 class="card-title">Обратная связь</h3>
              <form @submit.prevent="submitForm">
                <div class="form-floating mb-3">
                  <input type="text" class="form-control" id="name" v-model="form.name" required>
                  <label for="name">Ваше имя</label>
                </div>
                
                <div class="form-floating mb-3">
                  <input type="text" class="form-control" id="contact" v-model="form.contact" required>
                  <label for="contact">Контакт для связи</label>
                </div>
                
                <div class="form-floating mb-3">
                  <select class="form-select" id="type" v-model="form.type">
                    <option value="question">Вопрос</option>
                    <option value="thank">Благодарность</option>
                    <option value="complaint">Жалоба</option>
                  </select>
                  <label for="type">Тип обращения</label>
                </div>
                
                <div class="form-floating mb-3">
                  <textarea class="form-control" id="message" v-model="form.message" style="height: 100px"></textarea>
                  <label for="message">Ваше сообщение</label>
                </div>
                
                <button type="submit" class="btn btn-primary w-100">
                  Отправить сообщение
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const form = ref({
  name: '',
  contact: '',
  type: 'question',
  message: ''
});

const submitForm = () => {
  // Здесь будет логика отправки формы
  console.log('Form submitted:', form.value);
};
</script>

<style scoped>
.about-us {
  position: relative;
  padding: 4rem 0;
  overflow: hidden;
  background-color: #fff;
}

.diagonal-lines {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, transparent 49.5%, #f0f4f8 49.5%, #f0f4f8 50.5%, transparent 50.5%);
  background-size: 30px 30px;
  opacity: 0.3;
  pointer-events: none;
}

.header-section {
  position: relative;
  z-index: 1;
}

.accent-line {
  width: 80px;
  height: 4px;
  background: linear-gradient(90deg, #3498db, #2ecc71);
  margin: 2rem auto;
  border-radius: 2px;
}

.about-card {
  padding: 2rem;
  background: #fff;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  transform: translateY(0);
  transition: transform 0.3s ease;
}

.about-card:hover {
  transform: translateY(-5px);
}

.section-title {
  color: #2c3e50;
  font-weight: 600;
  margin-bottom: 1.5rem;
  position: relative;
  display: inline-block;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 40px;
  height: 3px;
  background: #3498db;
  border-radius: 2px;
}

.highlight-box {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  margin-top: 1.5rem;
}

.highlight-box i {
  font-size: 1.5rem;
  color: #3498db;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  padding: 1rem;
}

.grid-item {
  aspect-ratio: 1;
  background: #f0f4f8;
  border-radius: 10px;
  transition: transform 0.3s ease;
}

.grid-item:hover {
  transform: scale(1.05);
}

.contact-card, .feedback-form {
  background: #fff;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
}

.contact-links {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.contact-link {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  text-decoration: none;
  color: inherit;
  transition: transform 0.2s ease;
}

.contact-link:hover {
  transform: translateX(5px);
  background: #f0f4f8;
}

.contact-link i {
  font-size: 1.5rem;
  color: #3498db;
}

.contact-link span {
  font-weight: 500;
}

.form-floating > .form-control,
.form-floating > .form-select {
  border-radius: 8px;
  border: 2px solid #e2e8f0;
}

.form-floating > .form-control:focus,
.form-floating > .form-select:focus {
  border-color: #3498db;
  box-shadow: none;
}

.btn-primary {
  background: linear-gradient(90deg, #3498db, #2ecc71);
  border: none;
  padding: 1rem;
  border-radius: 8px;
  font-weight: 500;
  transition: transform 0.2s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .about-us {
    padding: 2rem 0;
  }
  
  .image-grid {
    grid-template-columns: 1fr;
  }
  
  .contact-section .row {
    flex-direction: column-reverse;
  }
}
</style>
