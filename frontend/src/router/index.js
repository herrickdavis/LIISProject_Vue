import { createRouter, createWebHistory } from 'vue-router'
import Login from '../pages/Login.vue'
import Dashboard from '../pages/Dashboard.vue'
import EquipoList from '../pages/EquipoList.vue'
import EquipoAddEdit from '../pages/EquipoAddEdit.vue'
import EquipoView from '../pages/EquipoView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/',
      name: 'CapturaDePeso',
      component: Dashboard,
      meta: { requiresAuth: true }
    },
    {
      path: '/liis/equipos',
      name: 'GestionDeEquipos',
      component: EquipoList,
      meta: { requiresAuth: true }
    },
    {
      path: '/liis/agregar-equipo',
      name: 'AgregarEquipo',
      component: EquipoAddEdit,
      meta: { requiresAuth: true }
    },
    {
      path: '/liis/editar-equipo/:id',
      name: 'EditarEquipo',
      component: EquipoAddEdit,
      meta: { requiresAuth: true }
    },
    {
      path: '/liis/equipo/:id',
      name: 'VerEquipo',
      component: EquipoView,
      meta: { requiresAuth: true }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('is_authenticated') === 'true';
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'login' });
  } else {
    next();
  }
});

export default router