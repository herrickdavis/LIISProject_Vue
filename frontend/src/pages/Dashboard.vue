<template>
  <MainLayout>
    <div class="card shadow-sm p-4">
      <form class="balanza" @submit.prevent="handleFormSubmit">
        <div class="row">
          <div class="col-md-6 mb-4">
            <div class="d-flex align-items-center mb-3">
              <h2 class="h5 mb-0 me-3">Código de Equipo</h2>
              <template v-if="balanza">
                <a @click.prevent="clearBalanza" title="Limpiar campo de codigo de barra" class="text-secondary"><i class="fas fa-sync-alt"></i></a>
              </template>
              <span class="ms-3">
                <i v-if="conectado" class="fas fa-circle text-success" title="Equipo con prueba de conexión satisfactoria"></i>
                <i v-else class="fas fa-circle text-danger" title="Sin conexión de equipo"></i>
              </span>
            </div>
            <div class="input-group">
              <input type="text" class="form-control" name="codigo_balanza" v-model="codigo_balanza_input" :readonly="!!balanza" :autofocus="!balanza" placeholder="Ingrese código de equipo">
            </div>
            <div class="mt-2">
              <p v-if="cb_error" class="text-danger">{{ cb_error }}</p>
              <p v-if="balanza" class="text-muted">{{ balanza.equipo }} {{ balanza.marca }} {{ balanza.modelo }}</p>
            </div>
          </div>
        </div>

        <div class="row">
          <div class="col-md-6 mb-4">
            <div class="d-flex align-items-center mb-3">
              <h2 class="h5 mb-0">Código de Muestra</h2>
            </div>
            <input type="text" class="form-control" name="codigo_muestra" v-model="codigo_muestra_input" :readonly="!!codigo_muestra" placeholder="Ingrese código de muestra">
            <!--:disabled="!balanza" -->
          </div>
          <div class="col-md-6 mb-4">
            <div class="d-flex align-items-center mb-3">
              <h2 class="h5 mb-0">Medición ({{ balanza?.unidad || 'Unidad' }})</h2>
            </div>
            <div class="input-group">
              <button class="btn btn-outline-secondary" type="button" @click.prevent="listenBalanza" :disabled="!ensayo || !balanza"><i class="fas fa-volume-up"></i></button>
              <input type="text" class="form-control" :class="medicionClass" name="medicion" v-model="medicion" :disabled="!ensayo" placeholder="Valor de la medición">
            </div>
            <p class="mt-2" :class="rangoClass">{{ rangoMedicion }}</p>
          </div>
        </div>

        <div class="row">
          <div class="col-12 mb-4">
            <h2 class="h5">Mediciones Pendientes</h2>
            <div class="table-responsive">
              <table class="table table-striped table-hover mt-2">
                <thead>
                  <tr>
                    <th>MÉTODO</th>
                    <th>NMVEMETODO</th>
                    <th>MIN</th>
                    <th>MAX</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(m, i) in metodos" :key="i" @click="extraerInformacion(m)" @dblclick="fijarInformacion(m)" :class="{ 'table-primary': m.idve === idve_selected }">
                    <td>{{ m.metodo }}</td>
                    <td>{{ m.NMVEMETODO }}</td>
                    <td>{{ m.min || '-' }}</td>
                    <td>{{ m.max || '-' }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
        
        <input type="hidden" name="ensayo" v-model="ensayo">
        <input type="hidden" name="fijo" v-model="fijo">
        <input type="hidden" name="idve_selected" v-model="idve_selected">

        <div class="d-grid mt-4">
          <button class="btn btn-primary btn-lg" type="submit" :disabled="!canSubmit">{{ buttonText }}</button>
        </div>
      </form>
    </div>
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
    codigo_muestra_input.value = '';
    metodos.value = [];
  } catch (err) {
    cb_error.value = err.response?.data?.cb_error || 'Error de conexión con la balanza.';
    balanza.value = null;
    conectado.value = false;
  }
};

const searchMetodos = async () => {
  if (!codigo_muestra_input.value) {
    cb_error.value = 'Debe ingresar un código de muestra.';
    return;
  }
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/liis/capturar-peso/', {
      codigo_balanza: balanza.value.codigo,
      codigo_muestra: codigo_muestra_input.value
    });
    metodos.value = response.data.metodos;
    cb_error.value = '';
  } catch (err) {
    cb_error.value = err.response?.data?.cb_error || 'Error al buscar métodos.';
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
    alert(response.data.message);
    clearForm();
  } catch (err) {
    alert(err.response?.data?.message || 'Error al guardar la medición.');
  }
};

const listenBalanza = async () => {
  // En un entorno real, aquí se haría una petición a la API de Django
  // para iniciar la conexión serial y recibir datos.
  // Por ahora, simulamos una lectura.
  medicion.value = (Math.random() * 100).toFixed(4);
};

const clearBalanza = () => {
  balanza.value = null;
  conectado.value = false;
  codigo_balanza_input.value = '';
  clearForm();
};

const clearForm = () => {
  codigo_muestra_input.value = '';
  metodos.value = [];
  medicion.value = '';
  ensayo.value = null;
  fijo.value = '';
  idve_selected.value = null;
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
  if (!balanza.value) return 'Conectar';
  if (!codigo_muestra_input.value) return 'Buscar Métodos';
  return 'Enviar';
});

const canSubmit = computed(() => {
  if (!balanza.value) return !!codigo_balanza_input.value;
  if (!codigo_muestra_input.value) return true;
  return !!medicion.value;
});

const medicionClass = computed(() => {
  if (!medicion.value) return '';
  const val = parseFloat(medicion.value);
  const min = parseFloat(ensayo.value?.split('-')[1]);
  const max = parseFloat(ensayo.value?.split('-')[2]);

  if (isNaN(min) || isNaN(max)) return 'is-valid';
  return val >= min && val <= max ? 'is-valid' : 'is-invalid';
});

const rangoMedicion = computed(() => {
  if (!ensayo.value) return '';
  const min = ensayo.value.split('-')[1] || '-';
  const max = ensayo.value.split('-')[2] || '-';
  return `Rango: ${min} - ${max}`;
});

watch(codigo_balanza_input, (newValue) => {
  if (!newValue) clearBalanza();
});

watch(codigo_muestra_input, (newValue) => {
  if (!newValue) clearForm();
});
</script>