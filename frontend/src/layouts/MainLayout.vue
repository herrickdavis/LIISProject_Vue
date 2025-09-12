<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <router-link class="navbar-brand d-flex align-items-center" :to="{ name: 'dashboard' }">
        <img src="/src/assets/logo.png" alt="Logo" style="height: 40px;">
      </router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="capturaDePesoDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Captura de Peso
            </a>
            <ul class="dropdown-menu" aria-labelledby="capturaDePesoDropdown">
              <li><router-link class="dropdown-item" :to="{ name: 'CapturaDePeso' }">Captura de Peso</router-link></li>
              <li><router-link class="dropdown-item" :to="{ name: 'GestionDeEquipos' }">Gestión de Equipos</router-link></li>
            </ul>
          </li>
        </ul>
        <ul class="navbar-nav">
          <li class="nav-item">
            <span class="nav-link text-white">{{ user.username }}</span>
          </li>
          <li class="nav-item">
            <a class="nav-link text-white" href="#" @click.prevent="logout">Salir</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <main class="container mt-4">
    <slot></slot>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { Dropdown, Collapse } from 'bootstrap';

const router = useRouter();
const user = ref({ username: localStorage.getItem('username') || '' });

const logout = async () => {
  try {
    // Si tu backend tiene un endpoint de logout, úsalo.
    await axios.post('http://127.0.0.1:8000/api/users/logout/');
  } finally {
    localStorage.clear();
    router.push('/login');
  }
};

onMounted(() => {
  user.value.username = localStorage.getItem('username') || '';

  const dropdownElement = document.getElementById('capturaDePesoDropdown');
  if (dropdownElement) {
    new Dropdown(dropdownElement);
  }

  const navbarToggler = document.querySelector('.navbar-toggler');
  const navbarCollapse = document.getElementById('navbarNav');
  if (navbarToggler && navbarCollapse) {
    new Collapse(navbarCollapse, {
      toggle: false
    });
  }
});
</script>