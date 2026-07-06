(() => {
  function shouldUseViewer() {
    return window.location.protocol !== 'file:';
  }

  function isMarkdownHref(href) {
    return href && /\.md(?:[#?].*)?$/i.test(href);
  }

  function toViewerHref(anchor, baseRoot = '') {
    const rawHref = anchor.getAttribute('href');
    if (!isMarkdownHref(rawHref)) return rawHref;

    const targetUrl = new URL(rawHref, window.location.href);
    const viewerUrl = new URL(`${baseRoot}document.html`, window.location.href);
    viewerUrl.searchParams.set('file', `${targetUrl.pathname}${targetUrl.search}`);

    const label = (anchor.dataset.viewerTitle || anchor.textContent || '').trim();
    if (label) viewerUrl.searchParams.set('title', label);

    return viewerUrl.toString();
  }

  function enhanceDocumentLinks(scope = document, options = {}) {
    if (!shouldUseViewer()) return;
    const baseRoot = options.baseRoot ?? document.body.dataset.root ?? '';
    scope.querySelectorAll('a[href]').forEach((anchor) => {
      const rawHref = anchor.getAttribute('href');
      if (!isMarkdownHref(rawHref)) return;
      if (anchor.dataset.viewerLinked === 'true') return;
      anchor.setAttribute('href', toViewerHref(anchor, baseRoot));
      anchor.dataset.viewerLinked = 'true';
    });
  }

  window.RAGCourseDocs = {
    enhanceDocumentLinks,
    toViewerHref,
  };

  document.addEventListener('DOMContentLoaded', () => enhanceDocumentLinks());
})();
