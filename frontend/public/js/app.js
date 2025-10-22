const tbody = document.querySelector("#table tbody");
const form = document.querySelector("#form");
const cancelEditBtn = document.querySelector("#cancelEdit");

let editingId = null;

// ---- Modal controls ----
const modalEl = document.getElementById('propertyModal');
const openBtn = document.getElementById('openModal');
const modalTitle = document.getElementById('modalTitle');

function openModal(title = 'Novo Imóvel') {
  modalTitle.textContent = title;
  modalEl.classList.add('is-open');
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  modalEl.classList.remove('is-open');
  document.body.style.overflow = '';
}

document.querySelectorAll('[data-open-modal]').forEach(btn => {
  btn.addEventListener('click', () => {
    form?.reset();
    editingId = null;
    if (cancelEditBtn) cancelEditBtn.style.display = 'none';
    openModal('Novo Imóvel');
  });
});


modalEl?.addEventListener('click', (e) => {
  if (e.target.matches('[data-close], .modal__backdrop')) closeModal();
});


window.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && modalEl.classList.contains('is-open')) closeModal();
});
// ---- Fim Modal controls ----

async function api(path, opts = {}) {
  const res = await fetch(`/api${path}`, { headers: { 'Content-Type': 'application/json' }, ...opts });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'Erro');
  }
  return res.json();
}

async function refresh() {
  const items = await api('/properties');
  tbody.innerHTML = items.map(it => `
    <tr>
      <td>${it.id}</td>
      <td>${escapeHtml(it.title)}</td>
      <td>${escapeHtml(it.address)}</td>
      <td><span class="badge ${it.status}">${it.status}</span></td>
      <td class="actions">
        <button class="btn btn-edit" 
          data-id="${it.id}" 
          data-title="${attrEscape(it.title)}" 
          data-address="${attrEscape(it.address)}" 
          data-status="${attrEscape(it.status)}">Editar</button>
        <button class="btn" data-delete="${it.id}">Excluir</button>
      </td>
    </tr>
  `).join('');
}


function escapeHtml(s = '') {
  return String(s)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}


function attrEscape(s = '') {
  return String(s).replaceAll('"', '&quot;').replaceAll("'", '&#039;');
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(form).entries());

  if (editingId) {
    await api(`/properties/${editingId}`, { method: 'PUT', body: JSON.stringify(data) });
  } else {
    await api('/properties', { method: 'POST', body: JSON.stringify(data) });
  }

  form.reset();
  editingId = null;
  cancelEditBtn.style.display = 'none';
  closeModal();              
  await refresh();
});

cancelEditBtn.addEventListener('click', () => {
  editingId = null;
  form.reset();
  cancelEditBtn.style.display = 'none';
  closeModal();              
});


document.getElementById('table')?.addEventListener('click', async (e) => {
  const editBtn = e.target.closest('.btn-edit');
  const delBtn = e.target.closest('[data-delete]');

  if (editBtn) {
    const id = Number(editBtn.dataset.id);
    const title = editBtn.dataset.title;
    const address = editBtn.dataset.address;
    const status = editBtn.dataset.status;

    editingId = id;
    form.title.value = title;
    form.address.value = address;
    form.status.value = status;

    cancelEditBtn.style.display = 'inline-block';
    openModal('Editar Imóvel');
    return;
  }

  if (delBtn) {
    const id = Number(delBtn.dataset.delete);
    if (confirm('Excluir?')) {
      await api(`/properties/${id}`, { method: 'DELETE' });
      await refresh();
    }
    return;
  }
});

refresh();
