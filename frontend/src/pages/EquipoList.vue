<template>
  <MainLayout>
    <div class="div_main">
      <div>
        <h1>
          Listado de Equipos<router-link
            :to="{ name: 'AgregarEquipo' }"
            style="padding-left: 30px"
            title="Agregar equipo"
            ><i class="fa-solid fa-plus"></i
          ></router-link>
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
              <td style="width: 5%">Acciones</td>
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
              <td>
                <router-link
                  :to="{ name: 'VerEquipo', params: { id: equipo.id } }"
                  ><i class="fa-solid fa-eye"></i
                ></router-link>
                <router-link
                  :to="{ name: 'EditarEquipo', params: { id: equipo.id } }"
                  ><i class="fa-solid fa-pen-to-square"></i
                ></router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <p v-else>Sin información almacenada en la base de datos.</p>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import MainLayout from "../layouts/MainLayout.vue";

const equipos = ref([]);

onMounted(async () => {
  const token = localStorage.getItem("token");
  if (!token) return;

  try {
    const response = await axios.get(
      "http://127.0.0.1:8000/api/liis/equipos/", 
      {
        headers: { Authorization: `Token ${token}` }
      }
    );
    equipos.value = response.data;
  } catch (error) {
    console.error("Error al obtener los equipos:", error.response?.data || error.message);
  }
});

</script>
