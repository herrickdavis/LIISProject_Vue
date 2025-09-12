<template>
  <MainLayout>
    <div class="container py-4">
      <!-- ALERTAS -->
      <div
        v-if="alert.message"
        :class="`alert alert-${alert.type}`"
        role="alert"
      >
        {{ alert.message }}
      </div>

      <!-- FORMULARIO AGREGAR / EDITAR -->
      <div class="card mb-4">
        <div class="card-header">
          {{ isEditing ? "Editar Equipo" : "Agregar Equipo" }}
        </div>
        <div class="card-body">
          <form @submit.prevent="saveEquipo" class="row g-3">
            <div class="col-md-4">
              <label class="form-label">Código de Barra</label>
              <input
                type="text"
                class="form-control"
                v-model="form.codigo"
                :readonly="isEditing"
                required
              />
            </div>
            <div class="col-md-4">
              <label class="form-label">Código Interno</label>
              <input
                type="text"
                class="form-control"
                v-model="form.codigo_interno"
              />
            </div>
            <div class="col-md-4">
              <label class="form-label">Equipo</label>
              <input
                type="text"
                class="form-control"
                v-model="form.equipo"
                required
              />
            </div>
            <div class="col-md-3">
              <label class="form-label">Marca</label>
              <input
                type="text"
                class="form-control"
                v-model="form.marca"
                required
              />
            </div>
            <div class="col-md-3">
              <label class="form-label">Modelo</label>
              <input
                type="text"
                class="form-control"
                v-model="form.modelo"
                required
              />
            </div>
            <div class="col-md-3">
              <label class="form-label">Valor Máximo</label>
              <input
                type="number"
                class="form-control"
                v-model="form.max_value"
                required
              />
            </div>
            <div class="col-md-3">
              <label class="form-label">Unidad</label>
              <input
                type="text"
                class="form-control"
                v-model="form.unidad"
                required
              />
            </div>
            <div class="col-md-3">
              <label class="form-label">Hostname</label>
              <input
                type="text"
                class="form-control"
                v-model="form.host"
                required
              />
            </div>
            <div class="col-md-3">
              <label class="form-label">Puerto TCP/IP</label>
              <input
                type="number"
                class="form-control"
                v-model="form.puerto"
                required
              />
            </div>
            <div class="col-md-3">
              <label class="form-label">Baudios</label>
              <input
                type="number"
                class="form-control"
                v-model="form.baudios"
                required
              />
            </div>
            <div class="col-md-3">
              <label class="form-label">Bytesize</label>
              <select class="form-select" v-model="form.bytesize" required>
                <option value="5">5</option>
                <option value="6">6</option>
                <option value="7">7</option>
                <option value="8">8</option>
              </select>
            </div>
            <div class="col-md-3">
              <label class="form-label">Parity</label>
              <select class="form-select" v-model="form.parity" required>
                <option value="None">None</option>
                <option value="EVEN">EVEN</option>
                <option value="ODD">ODD</option>
                <option value="MARK">MARK</option>
                <option value="SPACE">SPACE</option>
              </select>
            </div>
            <div class="col-md-3">
              <label class="form-label">Stopbits</label>
              <select class="form-select" v-model="form.stopbits" required>
                <option value="1">1</option>
                <option value="1.5">1.5</option>
                <option value="2">2</option>
              </select>
            </div>
            <div class="col-md-3">
              <label class="form-label">País</label>
              <input
                type="text"
                class="form-control"
                v-model="form.pais"
                required
              />
            </div>
            <div class="col-md-3">
              <label class="form-label">Sucursal</label>
              <input
                type="text"
                class="form-control"
                v-model="form.sede"
                required
              />
            </div>
            <div class="col-12 text-end">
              <button type="submit" class="btn btn-success me-2">
                {{ isEditing ? "Actualizar" : "Guardar" }}
              </button>
              <button
                type="button"
                class="btn btn-secondary"
                @click="resetForm"
              >
                Cancelar
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- TABLA DE EQUIPOS -->
      <table class="table table-striped table-hover">
        <thead class="table-dark">
          <tr>
            <th>Código</th>
            <th>Código Interno</th>
            <th>Descripción</th>
            <th>País</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="equipo in equipos" :key="equipo.id">
            <td>{{ equipo.codigo }}</td>
            <td>{{ equipo.codigo_interno || "-" }}</td>
            <td>{{ equipo.equipo }} {{ equipo.marca }} {{ equipo.modelo }}</td>
            <td>{{ equipo.pais }}</td>
            <td>
              <button
                class="btn btn-sm btn-warning me-1"
                @click="editEquipo(equipo)"
              >
                <i class="fa-solid fa-pen-to-square"></i>
              </button>
              <button
                class="btn btn-sm btn-danger"
                @click="deleteEquipo(equipo.id)"
              >
                <i class="fa-solid fa-trash"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- PAGINACIÓN -->
      <nav v-if="totalPages > 1">
        <ul class="pagination justify-content-center">
          <li class="page-item" :class="{ disabled: page === 1 }">
            <a class="page-link" href="#" @click.prevent="changePage(page - 1)"
              >Anterior</a
            >
          </li>
          <li
            class="page-item"
            v-for="p in totalPages"
            :key="p"
            :class="{ active: p === page }"
          >
            <a class="page-link" href="#" @click.prevent="changePage(p)">{{
              p
            }}</a>
          </li>
          <li class="page-item" :class="{ disabled: page === totalPages }">
            <a class="page-link" href="#" @click.prevent="changePage(page + 1)"
              >Siguiente</a
            >
          </li>
        </ul>
      </nav>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import MainLayout from "../layouts/MainLayout.vue";

const equipos = ref([]);
const form = ref({});
const isEditing = ref(false);
const alert = ref({ message: "", type: "success" });
const page = ref(1);
const pageSize = 10;
const totalPages = ref(1);

const API_BASE = "http://127.0.0.1:8000/api/liis/equipos/";

// Traer equipos paginados
const fetchEquipos = async () => {
  const token = localStorage.getItem("token");
  try {
    const res = await axios.get(`${API_BASE}?page=${page.value}`, {
      headers: { Authorization: `Token ${token}` },
    });
    equipos.value = res.data.results;
    totalPages.value = Math.ceil(res.data.count / pageSize);
  } catch (err) {
    showAlert("Error al cargar equipos", "danger");
  }
};

// Guardar / actualizar equipo
const saveEquipo = async () => {
  const token = localStorage.getItem("token");
  try {
    if (isEditing.value) {
      await axios.put(`${API_BASE}${form.value.id}/`, form.value, {
        headers: { Authorization: `Token ${token}` },
      });
      showAlert("Equipo actualizado", "success");
    } else {
      await axios.post(API_BASE, form.value, {
        headers: { Authorization: `Token ${token}` },
      });
      showAlert("Equipo agregado", "success");
    }
    resetForm();
    fetchEquipos();
  } catch (err) {
    console.log(err.response?.data);
    showAlert("Error al guardar equipo", "danger");
  }
};


// Editar equipo
const editEquipo = (equipo) => {
  form.value = { ...equipo };
  isEditing.value = true;
  window.scrollTo({ top: 0, behavior: "smooth" });
};

// Eliminar equipo
const deleteEquipo = async (id) => {
  if (!confirm("¿Seguro de eliminar?")) return;
  const token = localStorage.getItem("token");
  try {
    await axios.delete(`${API_BASE}${id}/`, {
      headers: { Authorization: `Token ${token}` },
    });
    showAlert("Equipo eliminado", "success");
    fetchEquipos();
  } catch (err) {
    showAlert("Error al eliminar", "danger");
  }
};

// Cambiar página
const changePage = (p) => {
  if (p < 1 || p > totalPages.value) return;
  page.value = p;
  fetchEquipos();
};

// Reset form
const resetForm = () => {
  form.value = {};
  isEditing.value = false;
};

// Mostrar alertas
const showAlert = (msg, type = "success") => {
  alert.value = { message: msg, type };
  setTimeout(() => (alert.value.message = ""), 4000);
};

onMounted(fetchEquipos);
</script>

<style scoped>
.table th,
.table td {
  vertical-align: middle;
}
.card {
  border-radius: 0.5rem;
}
.alert {
  transition: all 0.3s;
}
</style>
