document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-module-id]').forEach((card) => {
    const key = `quiz-${card.dataset.moduleId}`;
    if (localStorage.getItem(key) === 'completed') {
      const badge = document.createElement('span');
      badge.className = 'badge';
      badge.textContent = '✓ Quiz completed';
      card.appendChild(badge);
    }
  });
});
