<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark" style="background-color: #005DA8;">
      <div class="container-fluid">
        <router-link class="navbar-brand d-flex align-items-center" :to="{ name: 'dashboard' }">
          <img src="/src/assets/logo.png" alt="Logo" class="navbar-logo">
        </router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
          <ul class="navbar-nav mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'dashboard' }">Inicio</router-link>
            </li>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" id="capturaDePesoDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                Captura de Peso
              </a>
              <ul class="dropdown-menu dropdown-menu-dark" aria-labelledby="capturaDePesoDropdown">
                <li><router-link class="dropdown-item" :to="{ name: 'CapturaDePeso' }">Captura de Peso</router-link></li>
                <li><router-link class="dropdown-item" :to="{ name: 'GestionDeEquipos' }">Gestión de Equipos</router-link></li>
              </ul>
            </li>
          </ul>
          <ul class="navbar-nav">
            <li class="nav-item d-flex align-items-center me-2">
              <span class="nav-link text-white">Bienvenido, {{ user.first_name }}</span>
            </li>
            <li class="nav-item">
              <a class="btn btn-outline-light" href="#" @click.prevent="logout">Salir</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <main class="container mt-4">
      <slot></slot>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { Dropdown, Collapse } from 'bootstrap';

const router = useRouter();
const user = ref({ 
  username: localStorage.getItem('username') || '',
  first_name: localStorage.getItem('first_name') || ''
});

const logout = async () => {
  try {
    await axios.post('http://127.0.0.1:8000/api/users/logout/', null, {
        headers: { Authorization: `Token ${localStorage.getItem('token')}` }
    });
  } catch (error) {
    console.error('Error al cerrar sesión:', error);
  } finally {
    localStorage.clear();
    router.push('/login');
  }
};

onMounted(() => {
  user.value.username = localStorage.getItem('username') || '';
  user.value.first_name = localStorage.getItem('first_name') || '';

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

<style scoped>
.navbar {
  background-color: #005DA8;
}

.navbar-logo {
  height: 40px;
  filter: brightness(100%); /* Mantener el logo brillante */
  transition: transform 0.3s ease-in-out;
}

.navbar-logo:hover {
  transform: scale(1.05);
}

.nav-link {
  color: #e0f2ff !important;
  transition: color 0.3s ease-in-out;
}

.nav-link:hover {
  color: white !important;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 5px;
}

.dropdown-menu {
  background-color: #004a88;
  border: none;
}

.dropdown-item {
  color: #e0f2ff !important;
  transition: background-color 0.3s;
}

.dropdown-item:hover {
  background-color: #003a6b;
  color: white !important;
}

.btn-outline-light {
  color: white;
  border-color: white;
  transition: background-color 0.3s, color 0.3s;
}

.btn-outline-light:hover {
  background-color: white;
  color: #005DA8;
}
</style>