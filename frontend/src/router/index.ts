import { createRouter, createWebHistory } from '@ionic/vue-router';
import { RouteRecordRaw } from 'vue-router';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: {
      title: 'Login - ReViews'
    }
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: {
      title: 'ReViews - Reseñas',
      requiresAuth: true
    }
  },
  {
    path: '/auth/callback',
    name: 'AuthCallback',
    component: () => import('@/views/AuthCallback.vue'),
    meta: {
      title: 'Autenticando...'
    }
  },
  {
    path: '/resena/:id',
    name: 'DetalleResena',
    component: () => import('@/views/DetalleResena.vue'),
    meta: {
      title: 'Detalle de Reseña - ReViews',
      requiresAuth: true
    }
  },
  {
    path: '/crear-resena',
    name: 'CrearResena',
    component: () => import('@/views/FormularioResena.vue'),
    meta: {
      title: 'Crear Reseña - ReViews',
      requiresAuth: true
    }
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

// Navigation guard para rutas protegidas
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('auth_token');
  const isPublicRoute = to.path === '/login' || to.path === '/auth/callback';
  
  // Si no hay token y no es una ruta pública, redirigir a login
  if (!token && !isPublicRoute) {
    next('/login');
  } 
  // Si hay token y trata de ir a login, redirigir a home
  else if (to.path === '/login' && token) {
    next('/');
  } 
  // En cualquier otro caso, permitir la navegación
  else {
    next();
  }
});

export default router;