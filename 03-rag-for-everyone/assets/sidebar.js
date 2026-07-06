document.addEventListener('DOMContentLoaded', () => {
  const sidebar = document.getElementById('module-sidebar');
  if (!sidebar || !window.RAG_MODULES) return;
  const root = sidebar.dataset.root || '';
  const active = document.body.dataset.activeModule;
  const links = window.RAG_MODULES.map((module) => {
    const href = `${root}${module.path}`;
    const isActive = module.id === active ? 'active' : '';
    return `<a class="${isActive}" href="${href}">${module.icon} ${module.title}</a>`;
  }).join('');
  sidebar.innerHTML = `<div class="eyebrow">All modules</div>${links}`;
});
