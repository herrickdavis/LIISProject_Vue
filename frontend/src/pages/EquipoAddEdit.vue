<template>
  <MainLayout>
    <div class="div_main">
        <h1>{{ equipo?.codigo ? 'Editar' : 'Agregar' }} Equipo</h1>
        <form @submit.prevent="submitForm">
            <div class="item_form">
                <label for="codigo">Codigo de Barra</label>
                <input name="codigo" type="text" required v-model="form.codigo">
            </div>
            <div class="contain-boton-enviar">
                <button type="submit">Guardar</button>
            </div>
        </form>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import MainLayout from '../layouts/MainLayout.vue';

const route = useRoute();
const router = useRouter();
const equipo = ref(null);
const form = ref({
    codigo: '',
    // ... (todos los demás campos del modelo Equipo)
});

onMounted(async () => {
    const equipoId = route.params.id;
    if (equipoId) {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/api/liis/equipos/${equipoId}/`);
            equipo.value = response.data;
            form.value = { ...response.data };
        } catch (error) {
            console.error('Error al obtener el equipo:', error);
        }
    }
});

const submitForm = async () => {
    try {
        if (equipo.value) {
            // Lógica para editar
            await axios.put(`http://127.0.0.1:8000/api/liis/equipos/${equipo.value.id}/`, form.value);
        } else {
            // Lógica para agregar
            await axios.post('http://127.0.0.1:8000/api/liis/equipos/', form.value);
        }
        router.push({ name: 'EquipoList' });
    } catch (error) {
        console.error('Error al guardar el equipo:', error);
    }
};
</script>