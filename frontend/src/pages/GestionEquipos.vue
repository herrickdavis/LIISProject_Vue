<template>
  <MainLayout>
    <div class="div_main">
      <!-- LISTADO -->
      <div v-if="currentView === 'list'">
        <div>
          <h1>
            Listado de Equipos
            <a
              href="#"
              @click.prevent="setView('add')"
              style="padding-left: 30px"
              title="Agregar equipo"
            >
              <i class="fa-solid fa-plus"></i>
            </a>
          </h1>
        </div>
        <div v-if="equipos.length">
          <table style="font-size: 1.6rem; width: 100%">
            <thead>
              <tr style="font-weight: bold">
                <td style="width: 20%; height: 35px; text-align: center">
                  Codigo de Barra
                </td>
                <td style="width: 20%; text-align: center">Codigo Interno</td>
                <td style="width: 40%">Descripción</td>
                <td style="width: 20%">País</td>
                <td style="width: 20%; text-align: center">Acciones</td>
              </tr>
            </thead>
            <tbody>
              <tr v-for="equipo in equipos" :key="equipo.id" class="item_list">
                <td style="height: 25px; text-align: center">
                  {{ equipo.codigo }}
                </td>
                <td style="text-align: center">
                  {{ equipo.codigo_interno || "-" }}
                </td>
                <td>
                  {{ equipo.equipo }} {{ equipo.marca }} {{ equipo.modelo }}
                </td>
                <td>{{ equipo.pais }}</td>
                <td style="text-align: center">
                  <a href="#" @click.prevent="setView('view', equipo.id)">
                    <i class="fa-solid fa-eye"></i>
                  </a>
                  <a href="#" @click.prevent="setView('edit', equipo.id)">
                    <i class="fa-solid fa-pen-to-square"></i>
                  </a>
                  <a href="#" @click.prevent="deleteEquipo(equipo.id)">
                    <i class="fa-solid fa-trash"></i>
                  </a>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-else>Sin información almacenada en la base de datos.</p>
      </div>

      <!-- FORMULARIO -->
      <div v-else-if="currentView === 'add' || currentView === 'edit'">
        <h1>{{ isEditing ? "Editar" : "Agregar" }} Equipo</h1>
        <form @submit.prevent="saveEquipo">
          <div class="item_form">
            <label for="codigo">Codigo de Barra</label>
            <input
              name="codigo"
              type="text"
              required
              v-model="form.codigo"
              :readonly="isEditing"
            />
          </div>
          <div class="item_form">
            <label for="codigo_interno">Codigo Interno</label>
            <input
              name="codigo_interno"
              type="text"
              v-model="form.codigo_interno"
            />
          </div>
          <div class="item_form">
            <label for="equipo">Equipo</label>
            <input type="text" name="equipo" required v-model="form.equipo" />
          </div>
          <div class="item_form">
            <label for="marca">Marca</label>
            <input type="text" name="marca" required v-model="form.marca" />
          </div>
          <div class="item_form">
            <label for="modelo">Modelo</label>
            <input type="text" name="modelo" required v-model="form.modelo" />
          </div>
          <div class="item_form">
            <label for="max_value">Valor máximo</label>
            <input
              type="text"
              name="max_value"
              required
              v-model="form.max_value"
            />
          </div>
          <div class="item_form">
            <label for="unidad">Unidad</label>
            <input type="text" name="unidad" required v-model="form.unidad" />
          </div>
          <div class="item_form">
            <label for="host">Hostname</label>
            <input type="text" name="host" required v-model="form.host" />
          </div>
          <div class="item_form">
            <label for="puerto">Puerto TCP/IP</label>
            <input type="text" name="puerto" required v-model="form.puerto" />
          </div>
          <div class="item_form">
            <label for="baudios">Baudios</label>
            <input type="text" name="baudios" required v-model="form.baudios" />
          </div>
          <div class="item_form">
            <label for="bytesize">bytesize</label>
            <select name="bytesize" required v-model="form.bytesize">
              <option value="5">5</option>
              <option value="6">6</option>
              <option value="7">7</option>
              <option value="8">8</option>
            </select>
          </div>
          <div class="item_form">
            <label for="parity">Parity</label>
            <select name="parity" required v-model="form.parity">
              <option value="None">None</option>
              <option value="EVEN">EVEN</option>
              <option value="ODD">ODD</option>
              <option value="MARK">MARK</option>
              <option value="SPACE">SPACE</option>
            </select>
          </div>
          <div class="item_form">
            <label for="stopbits">stopbits</label>
            <select name="stopbits" required v-model="form.stopbits">
              <option value="1">1</option>
              <option value="1.5">1.5</option>
              <option value="2">2</option>
            </select>
          </div>
          <div class="item_form">
            <label for="pais">País</label>
            <input type="text" name="pais" required v-model="form.pais" />
          </div>
          <div class="item_form">
            <label for="sede">Sucursal</label>
            <input type="text" name="sede" required v-model="form.sede" />
          </div>
          <div class="contain-boton-enviar">
            <button type="submit">Guardar</button>
            <a href="#" @click.prevent="setView('list')" class="btn-cancelar"
              >Cancelar</a
            >
          </div>
        </form>
      </div>

      <!-- DETALLES -->
      <div v-else-if="currentView === 'view' && equipo">
        <h1>
          {{ equipo.equipo }} {{ equipo.marca }} {{ equipo.modelo }}
          <a
            href="#"
            @click.prevent="setView('edit', equipo.id)"
            style="padding-left: 30px"
            title="Editar equipo"
          >
            <i class="fa-solid fa-pen-to-square"></i>
          </a>
        </h1>
        <div style="font-size: 1.6rem">
          <div style="display: flex; margin-bottom: 20px">
            <p style="width: 50%">Código de Barra: {{ equipo.codigo }}</p>
            <p style="width: 50%">
              Código Interno: {{ equipo.codigo_interno || "Sin información" }}
            </p>
          </div>
          <div style="display: flex; margin-bottom: 20px">
            <p style="width: 50%">
              Valor máximo: {{ equipo.max_value || "Sin información" }}
            </p>
            <p style="width: 50%">Unidad: {{ equipo.unidad }}</p>
          </div>
          <div style="display: flex; margin-bottom: 20px">
            <p style="width: 50%">Hostname: {{ equipo.host }}</p>
            <p style="width: 50%">TCP/IP: {{ equipo.puerto }}</p>
          </div>
          <div style="display: flex; margin-bottom: 20px">
            <p style="width: 50%">Baudios: {{ equipo.baudios }}</p>
            <p style="width: 50%">bytesize: {{ equipo.bytesize }}</p>
          </div>
          <div style="display: flex; margin-bottom: 20px">
            <p style="width: 50%">Parity: {{ equipo.parity }}</p>
            <p style="width: 50%">stopbits: {{ equipo.stopbits }}</p>
          </div>
          <div style="display: flex; margin-bottom: 20px">
            <p style="width: 50%">País: {{ equipo.pais }}</p>
            <p style="width: 50%">
              Sucursal: {{ equipo.sede || "Sin información" }}
            </p>
          </div>
        </div>
        <div class="contain-boton-enviar">
          <a href="#" @click.prevent="setView('list')" class="btn-cancelar"
            >Volver al Listado</a
          >
        </div>
      </div>
      <div v-else-if="currentView === 'view' && !equipo">
        <p>Cargando los detalles del equipo...</p>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import MainLayout from "../layouts/MainLayout.vue";
import { useRoute } from "vue-router";

const route = useRoute();
const currentView = ref("list");
const equipos = ref([]);
const equipo = ref(null);
const form = ref({});
const isEditing = ref(false);

const API_BASE = "http://127.0.0.1:8000/api/liis/equipos/";

const fetchEquipos = async () => {
  const token = localStorage.getItem("token");
  if (!token) return console.error("No se encontró el token de autenticación.");
  try {
    const response = await axios.get(API_BASE, {
      headers: { Authorization: `Token ${token}` },
    });
    equipos.value = response.data;
  } catch (error) {
    console.error(
      "Error al obtener los equipos:",
      error.response?.data || error.message
    );
  }
};

const fetchEquipo = async (id) => {
  const token = localStorage.getItem("token");
  try {
    const response = await axios.get(`${API_BASE}${id}/`, {
      headers: { Authorization: `Token ${token}` },
    });
    equipo.value = response.data;
    form.value = { ...response.data };
  } catch (error) {
    console.error(
      "Error al obtener el equipo:",
      error.response?.data || error.message
    );
  }
};

const saveEquipo = async () => {
  const token = localStorage.getItem("token");
  try {
    if (isEditing.value) {
      await axios.put(`${API_BASE}${form.value.id}/`, form.value, {
        headers: { Authorization: `Token ${token}` },
      });
      alert("Equipo actualizado con éxito.");
    } else {
      await axios.post(API_BASE, form.value, {
        headers: { Authorization: `Token ${token}` },
      });
      alert("Equipo agregado con éxito.");
    }
    setView("list");
  } catch (error) {
    console.error(
      "Error al guardar el equipo:",
      error.response?.data || error.message
    );
    alert("Hubo un error al guardar el equipo.");
  }
};

const deleteEquipo = async (id) => {
  const token = localStorage.getItem("token");
  try {
    await axios.delete(`${API_BASE}${id}/`, {
      headers: { Authorization: `Token ${token}` },
    });
    alert("Equipo eliminado con éxito.");
    fetchEquipos();
  } catch (error) {
    console.error(
      "Error al eliminar el equipo:",
      error.response?.data || error.message
    );
    alert("Hubo un error al eliminar el equipo.");
  }
};

const setView = (view, id = null) => {
  currentView.value = view;
  if (view === "edit") {
    isEditing.value = true;
    fetchEquipo(id);
  } else if (view === "view") {
    isEditing.value = false;
    fetchEquipo(id);
  } else if (view === "add") {
    isEditing.value = false;
    form.value = {};
  } else if (view === "list") {
    equipo.value = null;
    fetchEquipos();
  }
};

onMounted(() => {
  fetchEquipos();
});
</script>
