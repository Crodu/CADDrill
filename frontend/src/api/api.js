import axios from 'axios';

const api = axios.create({
  baseURL: 'http://driller.local:8000/'
});

export default api;