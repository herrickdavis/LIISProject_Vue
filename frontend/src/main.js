import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

// Importar Bootstrap CSS
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap'; // Importa el JavaScript de Bootstrap

const app = createApp(App);
app.use(router);
app.mount('#app');