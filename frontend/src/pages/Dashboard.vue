<template>
  <MainLayout>
    <form class="balanza" @submit.prevent="handleFormSubmit">
        <div class="c-barra-contain">
            <template v-if="balanza">
                <a @click.prevent="clearBalanza" title="Limpiar campo de codigo de barra"><i class="fa-solid fa-arrows-rotate"></i></a>
            </template>
            <div>
                <label for="codigo_balanza">Código de Equipo</label>
                <input type="text" name="codigo_balanza" v-model="codigo_balanza_input" :readonly="!!balanza" autofocus>
            </div>
            <div>
                <p v-if="cb_error" class="cb-error msg">{{ cb_error }}</p>
                <p v-if="balanza" class="cb-respuesta">{{ balanza.equipo }} {{ balanza.marca }} {{ balanza.modelo }}</p>
            </div>
        </div>

        <div style="display: flex; justify-content: space-between; height: 250px;">
            <div>
                <div class="c-muestra-contain">
                    <label for="codigo_muestra">Codigo de Muestra</label>
                    <input type="text" v-model="codigo_muestra_input" name="codigo_muestra" :readonly="!!codigo_muestra" :disabled="!balanza">
                </div>
                <div class="c-peso-contain">
                    <label for="">Medición ({{ balanza?.unidad || 'Unidad' }})</label>
                    <div>
                        <div style="display:flex;">
                            <button class="ear-contain" @click.prevent="listenBalanza" :disabled="!ensayo || !balanza"><i class="fa-solid fa-ear-listen"></i></button>
                            <input class="medicion" :style="medicionStyle" name="medicion" type="text" v-model="medicion" :disabled="!ensayo">
                        </div>
                        <p class="med_range">{{ rangoMedicion }}</p>
                    </div>
                </div>
            </div>
            <div style="width:45%; height: 220px;">
                <label class="list-medition-contain" for="">Mediciones Pendientes</label>
                <input class="fijo" v-model="fijo" readonly>
                <div class="ensayo-table">
                    <table class="met-table">
                        <tr v-for="(m, i) in metodos" :key="i" @click="extraerInformacion(m)" @dblclick="fijarInformacion(m)" :class="{ 'selected': m.idve === idve_selected }">
                            <td>{{ m.metodo }}</td>
                            <td>{{ m.NMVEMETODO }}</td>
                            <td>{{ m.min || '-' }}</td>
                            <td>{{ m.max || '-' }}</td>
                        </tr>
                    </table>
                </div>
            </div>
        </div>

        <div class="contain-boton-enviar">
            <button class="boton-guardar-peso" type="submit">{{ buttonText }}</button>
        </div>
    </form>
  </MainLayout>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import axios from 'axios';
import MainLayout from '../layouts/MainLayout.vue';

const codigo_balanza_input = ref('');
const codigo_muestra_input = ref('');
const balanza = ref(null);
const conectado = ref(false);
const error_conexion = ref('');
const cb_error = ref('');
const metodos = ref([]);
const medicion = ref('');
const ensayo = ref(null);
const fijo = ref('');
const idve_selected = ref(null);

const handleFormSubmit = async () => {
    if (!balanza.value) {
        await searchBalanza();
    } else if (!codigo_muestra_input.value) {
        await searchMetodos();
    } else if (medicion.value) {
        await saveMedicion();
    }
};

const searchBalanza = async () => {
    try {
        const response = await axios.post('http://127.0.0.1:8000/api/liis/capturar-peso/', {
            codigo_balanza: codigo_balanza_input.value,
            conectar: true
        });
        balanza.value = response.data.balanza;
        conectado.value = response.data.conectado;
        cb_error.value = '';
    } catch (err) {
        cb_error.value = err.response.data.cb_error;
    }
};

const searchMetodos = async () => {
    if (!codigo_muestra_input.value) return;
    try {
        const response = await axios.post('http://127.0.0.1:8000/api/liis/capturar-peso/', {
            codigo_balanza: balanza.value.codigo,
            codigo_muestra: codigo_muestra_input.value
        });
        metodos.value = response.data.metodos;
        cb_error.value = '';
    } catch (err) {
        cb_error.value = err.response.data.cb_error;
    }
};

const saveMedicion = async () => {
    try {
        const response = await axios.post('http://127.0.0.1:8000/api/liis/capturar-peso/', {
            codigo_balanza: balanza.value.codigo,
            codigo_muestra: codigo_muestra_input.value,
            medicion: medicion.value,
            ensayo: ensayo.value
        });
        // Lógica para mostrar mensaje de éxito y limpiar el formulario
    } catch (err) {
        // Lógica para manejar errores
    }
};

const listenBalanza = async () => {
    // Lógica para la conexión real con la balanza, que será más compleja y puede requerir un WebSocket
    // Por ahora, simularemos la lectura
    medicion.value = (Math.random() * 100).toFixed(4);
};

const clearBalanza = () => {
    balanza.value = null;
    conectado.value = false;
    codigo_balanza_input.value = '';
    // Limpiar todos los campos del formulario
};

const extraerInformacion = (m) => {
    ensayo.value = `${m.idve}-${m.min || ''}-${m.max || ''}`;
    idve_selected.value = m.idve;
};

const fijarInformacion = (m) => {
    fijo.value = m.metodo;
    extraerInformacion(m);
};

const buttonText = computed(() => {
    if (!balanza.value) return 'Buscar';
    if (!codigo_muestra_input.value) return 'Buscar Métodos';
    return 'Enviar';
});

const medicionStyle = computed(() => {
    // Lógica para cambiar el borde según el rango
    // Puedes adaptar tu código de JS original aquí
    return {};
});

watch(codigo_balanza_input, (newValue) => {
    if (!newValue) clearBalanza();
});
</script>