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
      name: 'CapturarPeso',
      component: Dashboard,
      meta: { requiresAuth: true }
    },
    {
      path: '/liis/equipos',
      name: 'EquipoList',
      component: EquipoList,
      meta: { requiresAuth: true }
    },
    {
      path: '/liis/agregar-equipo',
      name: 'EquipoAdd',
      component: EquipoAddEdit,
      meta: { requiresAuth: true }
    },
    {
      path: '/liis/editar-equipo/:id',
      name: 'EquipoEdit',
      component: EquipoAddEdit,
      meta: { requiresAuth: true }
    },
    {
      path: '/liis/equipo/:id',
      name: 'EquipoView',
      component: EquipoView,
      meta: { requiresAuth: true }
    },
    {
      path: '/liis/ejecutable/:nombre',
      name: 'Ejecutable',
      component: null, // O un componente que maneje la descarga
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