// validation.js - encapsulates form validation logic for Fund Transfer UI
export function sanitize(str) {
  return String(str).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;','\'':'&#39;'}[c]));
}

export function validateForm(form) {
  const errors = [];
  const fromAccount = form.fromAccount.value.trim();
  const toAccount = form.toAccount.value.trim();
  const amountRaw = form.amount.value.trim();
  const dateVal = form.transferDate.value.trim();
  const description = form.description.value;

  // clear previous inline errors (caller responsible for DOM removal)
  const fieldErrors = {};

  if (!fromAccount) {
    errors.push('Select a source account');
    fieldErrors.fromAccount = 'Required';
  }

  if (!toAccount) {
    errors.push('Enter beneficiary account');
    fieldErrors.toAccount = 'Required';
  } else if (!/^[A-Za-z0-9]{10,14}$/.test(toAccount)) {
    errors.push('Beneficiary account must be 10–14 letters/digits');
    fieldErrors.toAccount = 'Pattern mismatch';
  }

  let amount = parseFloat(amountRaw);
  if (!amountRaw) {
    errors.push('Enter transfer amount');
    fieldErrors.amount = 'Required';
  } else if (isNaN(amount)) {
    errors.push('Amount must be numeric');
    fieldErrors.amount = 'Invalid number';
  } else {
    if (amount <= 0) { errors.push('Amount must be > 0'); fieldErrors.amount = 'Must be > 0'; }
    if (amount > 10000) { errors.push('Amount exceeds limit 10,000.00'); fieldErrors.amount = 'Exceeds limit'; }
  }

  if (!dateVal) {
    errors.push('Transfer date required');
    fieldErrors.transferDate = 'Required';
  }

  const normalizedAmount = !isNaN(amount) && amount > 0 && amount <= 10000 ? amount.toFixed(2) : amountRaw;

  return {
    valid: errors.length === 0,
    errors,
    fieldErrors,
    data: { fromAccount, toAccount, amount: normalizedAmount, transferDate: dateVal, description }
  };
}
