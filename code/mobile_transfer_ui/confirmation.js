// confirmation.js - handles rendering of confirmation details
import { sanitize } from './validation.js';

export function renderConfirmation(container, data) {
  container.innerHTML = '';
  Object.entries(data).forEach(([k,v]) => {
    const dt = document.createElement('dt');
    dt.textContent = k.replace(/([A-Z])/g,' $1').replace(/^./,c=>c.toUpperCase());
    const dd = document.createElement('dd');
    dd.textContent = sanitize(v);
    container.appendChild(dt);
    container.appendChild(dd);
  });
}