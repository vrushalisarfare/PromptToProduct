/* app.js - orchestrates Fund Transfer UI using modular validation & confirmation */
import { validateForm } from './validation.js';
import { renderConfirmation } from './confirmation.js';

const form = document.getElementById('transfer-form');
const confirmSection = document.getElementById('confirmation');
const confirmDetails = document.getElementById('confirm-details');
const errorSummary = document.getElementById('error-summary');
const editBtn = document.getElementById('editBtn');
const finishBtn = document.getElementById('finishBtn');

// Default date initialization
const dateField = document.getElementById('transferDate');
if (dateField) {
  dateField.value = new Date().toISOString().substring(0,10);
}

function showErrors(errors) {
  errorSummary.hidden = errors.length === 0;
  if (errors.length) {
    errorSummary.innerHTML = '<strong>Please correct the following:</strong><ul>' + errors.map(e => '<li>' + e + '</li>').join('') + '</ul>';
  } else {
    errorSummary.innerHTML = '';
  }
}

function setFieldError(id, msg) {
  const el = document.getElementById('error-' + id);
  if (!el) return;
  if (msg) {
    el.textContent = msg;
    el.hidden = false;
  } else {
    el.textContent = '';
    el.hidden = true;
  }
}

form.addEventListener('submit', e => {
  e.preventDefault();
  // Clear previous field errors
  ['fromAccount','toAccount','amount','transferDate'].forEach(f => setFieldError(f));
  const result = validateForm(form);
  // Set inline errors
  Object.entries(result.fieldErrors).forEach(([field,msg]) => setFieldError(field, msg));
  showErrors(result.errors);
  if (!result.valid) return;

  // Update normalized amount value
  form.amount.value = result.data.amount;
  renderConfirmation(confirmDetails, result.data);
  form.hidden = true;
  confirmSection.hidden = false;
});

editBtn.addEventListener('click', () => {
  confirmSection.hidden = true;
  form.hidden = false;
  form.querySelector('#continueBtn').focus();
});

finishBtn.addEventListener('click', () => {
  alert('Prototype complete: In production, transfer would be submitted.');
});