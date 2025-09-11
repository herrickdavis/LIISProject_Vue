<template>
  <nav>
    <router-link :to="{ name: 'Dashboard' }">
      <img class="nav-logo" src="/path/to/your/logo.png" alt="Logo de empresa">
    </router-link>
    <div class="nav-center">
      <div class="menu-item" @click="toggleMenu('balanzas')">
        Balanzas
        <ul v-if="activeMenu === 'balanzas'" class="submenu">
          <li><router-link :to="{ name: 'Dashboard' }">Capturar</router-link></li>
          <li><router-link :to="{ name: 'EquipoList' }">Gestión de Equipos</router-link></li>
        </ul>
      </div>
      </div>
    <div class='nav-right-section'>
      <ul>
        <li class="nav-item">{{ user.username }}</li>
        <li class="nav-item"><a href="#" @click.prevent="logout">Salir</a></li>
      </ul>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const activeMenu = ref(null);
const user = ref({ username: localStorage.getItem('username') || '' });

const toggleMenu = (menu) => {
    activeMenu.value = activeMenu.value === menu ? null : menu;
};

const logout = async () => {
    try {
        await axios.post('http://127.0.0.1:8000/api/users/logout/');
    } finally {
        localStorage.clear();
        router.push('/login');
    }
};
</script>