<template>
  <MainLayout>
    <div class="div_main">
        <h1>{{ equipo?.equipo }} {{ equipo?.marca }} {{ equipo?.modelo }}
            <router-link :to="{ name: 'EquipoEdit', params: { id: equipo?.id } }" style="padding-left: 30px;" title="Editar equipo"><i class="fa-solid fa-pen-to-square"></i></router-link>
        </h1>
        <div style="font-size: 1.6rem;">
            <p>Código de Barra: {{ equipo?.codigo }}</p>
            </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import MainLayout from '../layouts/MainLayout.vue';

const route = useRoute();
const equipo = ref(null);

onMounted(async () => {
    try {
        const response = await axios.get(`http://127.0.0.1:8000/api/liis/equipos/${route.params.id}/`);
        equipo.value = response.data;
    } catch (error) {
        console.error('Error al obtener los detalles del equipo:', error);
    }
});
</script>