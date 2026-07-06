document.addEventListener('DOMContentLoaded', () => {
  const sidebar = document.getElementById('module-sidebar');
  if (!sidebar || !window.RAG_MODULES) return;
  const useViewer = window.location.protocol !== 'file:';
  const root = sidebar.dataset.root || '';
  const active = document.body.dataset.activeModule;
  const activePage = document.body.dataset.activePage || 'lesson';
  const currentModule = window.RAG_MODULES.find((module) => module.id === active);
  const links = window.RAG_MODULES.map((module) => {
    const href = `${root}${module.path}`;
    const isActive = module.id === active ? 'active' : '';
    return `<a class="${isActive}" href="${href}">${module.icon} ${module.title}</a>`;
  }).join('');

  const toViewerHref = (href, label) => {
    const targetUrl = new URL(href, window.location.href);
    const viewerUrl = new URL(`${root}document.html`, window.location.href);
    viewerUrl.searchParams.set('file', `${targetUrl.pathname}${targetUrl.search}`);
    if (label) viewerUrl.searchParams.set('title', label);
    return viewerUrl.toString();
  };

  const renderHref = (item, href) => (useViewer && item.path.endsWith('.md')) ? toViewerHref(href, item.label) : href;
  const sections = [];

  if (currentModule) {
    const basePath = `${root}${currentModule.path.replace(/lesson\.html$/, '')}`;
    const learnerLinks = [
      { id: 'lesson', label: 'Lesson', path: 'lesson.html' },
      { id: 'quiz', label: 'Quiz', path: 'quiz.html' },
      { id: 'interview', label: 'Interview prep', path: 'interview-questions.html' },
      { id: 'practice', label: 'Practice bank', path: 'practice/index.html' },
      { id: 'lab', label: 'Hands-on lab', path: 'hands-on-lab/index.html' },
      { id: 'exercises', label: 'Exercises', path: 'exercises/index.html' },
      { id: 'project', label: 'Project', path: 'project/index.html' },
      { id: 'flashcards', label: 'Flashcards', path: 'flashcards/index.html' },
      { id: 'notebook', label: 'Notebook', path: 'notebook/index.html' },
    ];
    const assetLinks = [
      { id: 'master-chapter', label: 'Master chapter', path: 'content/master-chapter.md' },
      { id: 'speaker-notes', label: 'Speaker notes', path: 'content/speaker-notes.md' },
      { id: 'blog-post', label: 'Blog post', path: 'content/blog-post.md' },
      { id: 'newsletter', label: 'Newsletter', path: 'content/newsletter.md' },
      { id: 'cheat-sheet', label: 'Cheat sheet', path: 'content/cheat-sheet.md' },
      { id: 'slides', label: 'Slide outline', path: 'content/slides.md' },
      { id: 'youtube-script', label: 'YouTube script', path: 'content/youtube-script.md' },
      { id: 'linkedin-carousel', label: 'LinkedIn carousel', path: 'content/linkedin-carousel.md' },
      { id: 'workshop-material', label: 'Workshop material', path: 'content/workshop-material.md' },
      { id: 'architecture', label: 'Architecture diagram', path: 'diagrams/architecture.svg' },
    ];

    const renderSectionLinks = (items) => items.map((item) => {
      const href = `${basePath}${item.path}`;
      const isActive = item.id === activePage ? 'active' : '';
      return `<a class="${isActive}" href="${renderHref(item, href)}">${item.label}</a>`;
    }).join('');

    sections.push(`<div class="sidebar-section"><div class="eyebrow">This module</div>${renderSectionLinks(learnerLinks)}<p class="sidebar-note">Move through lesson → quiz → practice → build without leaving the module shell.</p></div>`);
    sections.push(`<div class="sidebar-section"><div class="eyebrow">Content assets</div>${renderSectionLinks(assetLinks)}</div>`);
  }

  sections.push(`<div class="sidebar-section"><div class="eyebrow">All modules</div>${links}</div>`);
  sidebar.innerHTML = sections.join('');

  sidebar.closest('body').querySelectorAll('a[href]').forEach((anchor) => {
    if (!useViewer) return;
    const href = anchor.getAttribute('href');
    if (!href || !/\.md(?:[#?].*)?$/i.test(href) || anchor.dataset.viewerLinked === 'true') return;
    anchor.href = toViewerHref(href, anchor.textContent.trim());
    anchor.dataset.viewerLinked = 'true';
  });
});
