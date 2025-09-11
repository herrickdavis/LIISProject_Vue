<template>
  <div class="d-flex align-items-center justify-content-center vh-100 bg-light">
    <div class="card p-4 shadow-lg" style="width: 25rem;">
      <div class="text-center">
        <img class="mb-4" src="/src/assets/logo.png" alt="Logo de empresa" style="width: 150px;">
        <h1 class="h3 mb-3 fw-normal">Iniciar Sesión</h1>
      </div>
      <form @submit.prevent="login">
        <p v-if="error" class="alert alert-danger">{{ error }}</p>
        <div class="form-floating mb-3">
          <input type="text" class="form-control" id="floatingInput" placeholder="Username" v-model="username" required>
          <label for="floatingInput">Username</label>
        </div>
        <div class="form-floating mb-3">
          <input type="password" class="form-control" id="floatingPassword" placeholder="********" v-model="password" required>
          <label for="floatingPassword">Contraseña</label>
        </div>
        <button class="w-100 btn btn-lg btn-primary" type="submit">Ingresar</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const username = ref('');
const password = ref('');
const error = ref('');
const router = useRouter();

const login = async () => {
    error.value = '';
    try {
        const response = await axios.post('http://127.0.0.1:8000/api/users/login/', {
            username: username.value,
            password: password.value,
        });
        localStorage.setItem('is_authenticated', 'true');
        localStorage.setItem('username', response.data.first_name || response.data.username);
        router.push('/');
    } catch (err) {
        if (err.response && err.response.data.error) {
            error.value = err.response.data.error;
        } else {
            error.value = 'Ha ocurrido un error inesperado. Inténtalo de nuevo.';
        }
    }
};
</script>