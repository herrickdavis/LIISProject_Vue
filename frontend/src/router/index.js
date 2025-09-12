import { createRouter, createWebHistory } from "vue-router";
import Login from "../pages/Login.vue";
import Dashboard from "../pages/Dashboard.vue";
import EquipoList from "../pages/EquipoList.vue";
import GestionEquipos from "../pages/GestionEquipos.vue";

import EquipoAddEdit from "../pages/EquipoAddEdit.vue";
import EquipoView from "../pages/EquipoView.vue";
import Capturapeso from "../pages/CapturaDatos/Capturapeso.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/login",
      name: "login",
      component: Login,
    },
    {
      path: "/",
      name: "dashboard",
      component: Dashboard,
      meta: { requiresAuth: true },
    },
    {
      path: "/capturar-peso",
      name: "CapturaDePeso",
      component: Capturapeso,
      meta: { requiresAuth: true },
    },

    {
      path: "/liis/equipos",
      name: "GestionDeEquipos",
      component: GestionEquipos,
      meta: { requiresAuth: true },
    },
    {
      path: "/liis/agregar-equipo",
      name: "AgregarEquipo",
      component: EquipoAddEdit,
      meta: { requiresAuth: true },
    },
    {
      path: "/liis/editar-equipo/:id",
      name: "EditarEquipo",
      component: EquipoAddEdit,
      meta: { requiresAuth: true },
    },
    {
      path: "/liis/equipo/:id",
      name: "VerEquipo",
      component: EquipoView,
      meta: { requiresAuth: true },
    },
  ],
});

router.beforeEach((to, from, next) => {
  const publicPages = ["/login"];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = localStorage.getItem("token");

  if (authRequired && !loggedIn) {
    return next("/login");
  }

  next();
});

export default router;
