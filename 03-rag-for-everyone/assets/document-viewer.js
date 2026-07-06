(() => {
  const sourcePath = document.getElementById('source-path');
  const sourceLink = document.getElementById('source-link');
  const viewerTitle = document.getElementById('viewer-title');
  const viewerSubtitle = document.getElementById('viewer-subtitle');
  const viewerContent = document.getElementById('viewer-content');
  const viewerToc = document.getElementById('viewer-toc');
  let currentSourceUrl = null;

  function escapeHtml(value) {
    return value
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function slugify(value) {
    return value
      .toLowerCase()
      .replace(/[^a-z0-9\s-]/g, '')
      .trim()
      .replace(/\s+/g, '-');
  }

  function toViewerHref(url, label) {
    const viewerUrl = new URL('document.html', window.location.href);
    viewerUrl.searchParams.set('file', `${url.pathname}${url.search}`);
    if (label) viewerUrl.searchParams.set('title', label);
    return viewerUrl.toString();
  }

  function sanitizeLinkUrl(rawUrl, label = '') {
    try {
      const base = currentSourceUrl || new URL(window.location.href);
      const resolved = new URL(rawUrl, base);
      if (resolved.protocol === 'mailto:') return resolved.toString();
      if (!['http:', 'https:'].includes(resolved.protocol)) return null;
      if (/\.md$/i.test(resolved.pathname) && resolved.origin === window.location.origin) {
        return toViewerHref(resolved, label);
      }
      return resolved.toString();
    } catch (error) {
      return null;
    }
  }

  function renderInline(text) {
    const escaped = escapeHtml(text);
    return escaped
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/\*([^*]+)\*/g, '<em>$1</em>')
      .replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_, label, url) => {
        const safeUrl = sanitizeLinkUrl(url, label);
        return safeUrl ? `<a href="${safeUrl}">${label}</a>` : label;
      });
  }

  function normalizeMarkdown(markdown) {
    return markdown
      .replace(/^\uFEFF/, '')
      .replace(/\r/g, '')
      .split('\n')
      .map((line) => line.replace(/^ {4}(?=\S)/, ''))
      .join('\n');
  }

  function isTableSeparator(line) {
    return /^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?$/.test(line.trim());
  }

  function isBlockStart(line, nextLine) {
    return !line ||
      /^```/.test(line) ||
      /^#{1,6}\s+/.test(line) ||
      /^[-*]\s+/.test(line) ||
      /^\d+\.\s+/.test(line) ||
      /^>\s?/.test(line) ||
      /^\|/.test(line) ||
      (/^\|/.test(line) && isTableSeparator(nextLine || '')) ||
      /^---+$/.test(line.trim());
  }

  function parseTable(lines, startIndex) {
    const header = lines[startIndex].split('|').slice(1, -1).map((cell) => cell.trim());
    const rows = [];
    let index = startIndex + 2;

    while (index < lines.length && /^\|/.test(lines[index])) {
      rows.push(lines[index].split('|').slice(1, -1).map((cell) => cell.trim()));
      index += 1;
    }

    const html = `
      <table>
        <thead><tr>${header.map((cell) => `<th>${renderInline(cell)}</th>`).join('')}</tr></thead>
        <tbody>${rows.map((cells) => `<tr>${cells.map((cell) => `<td>${renderInline(cell)}</td>`).join('')}</tr>`).join('')}</tbody>
      </table>
    `;

    return { html, nextIndex: index };
  }

  function parseMarkdown(markdown) {
    const lines = normalizeMarkdown(markdown).split('\n');
    const html = [];
    const toc = [];
    let index = 0;

    while (index < lines.length) {
      const line = lines[index];
      const trimmed = line.trim();

      if (!trimmed) {
        index += 1;
        continue;
      }

      if (/^```/.test(trimmed)) {
        const codeLines = [];
        index += 1;
        while (index < lines.length && !/^```/.test(lines[index].trim())) {
          codeLines.push(lines[index]);
          index += 1;
        }
        if (index < lines.length) index += 1;
        html.push(`<pre><code>${escapeHtml(codeLines.join('\n'))}</code></pre>`);
        continue;
      }

      if (/^#{1,6}\s+/.test(trimmed)) {
        const level = trimmed.match(/^#+/)[0].length;
        const text = trimmed.replace(/^#{1,6}\s+/, '').trim();
        const id = slugify(text) || `section-${toc.length + 1}`;
        toc.push({ level, text, id });
        html.push(`<h${level} id="${id}">${renderInline(text)}</h${level}>`);
        index += 1;
        continue;
      }

      if (/^\|/.test(trimmed) && isTableSeparator(lines[index + 1] || '')) {
        const table = parseTable(lines, index);
        html.push(table.html);
        index = table.nextIndex;
        continue;
      }

      if (/^[-*]\s+/.test(trimmed)) {
        const items = [];
        while (index < lines.length && /^[-*]\s+/.test(lines[index].trim())) {
          items.push(lines[index].trim().replace(/^[-*]\s+/, ''));
          index += 1;
        }
        html.push(`<ul>${items.map((item) => `<li>${renderInline(item)}</li>`).join('')}</ul>`);
        continue;
      }

      if (/^\d+\.\s+/.test(trimmed)) {
        const items = [];
        while (index < lines.length && /^\d+\.\s+/.test(lines[index].trim())) {
          items.push(lines[index].trim().replace(/^\d+\.\s+/, ''));
          index += 1;
        }
        html.push(`<ol>${items.map((item) => `<li>${renderInline(item)}</li>`).join('')}</ol>`);
        continue;
      }

      if (/^>\s?/.test(trimmed)) {
        const blocks = [];
        while (index < lines.length && /^>\s?/.test(lines[index].trim())) {
          blocks.push(lines[index].trim().replace(/^>\s?/, ''));
          index += 1;
        }
        html.push(`<blockquote><p>${renderInline(blocks.join(' '))}</p></blockquote>`);
        continue;
      }

      if (/^---+$/.test(trimmed)) {
        html.push('<hr>');
        index += 1;
        continue;
      }

      const paragraph = [trimmed];
      index += 1;
      while (index < lines.length && lines[index].trim() && !isBlockStart(lines[index].trim(), lines[index + 1])) {
        paragraph.push(lines[index].trim());
        index += 1;
      }
      html.push(`<p>${renderInline(paragraph.join(' '))}</p>`);
    }

    return { html: html.join('\n'), toc };
  }

  function renderToc(items) {
    if (items.length <= 1) {
      viewerToc.innerHTML = '<div class="viewer-empty"><p>No section list needed for this document.</p></div>';
      return;
    }

    viewerToc.innerHTML = `
      <div class="eyebrow">On this page</div>
      <div class="page-toc">
        ${items.map((item) => `<a href="#${item.id}">${item.text}</a>`).join('')}
      </div>
    `;
  }

  function resolveSourceUrl(file) {
    try {
      const base = window.location.href;
      const resolved = new URL(file, base);
      if (window.location.protocol !== 'file:' && resolved.origin !== window.location.origin) return null;
      if (!['http:', 'https:', 'file:'].includes(resolved.protocol)) return null;
      if (!/\.md$/i.test(resolved.pathname)) return null;
      return resolved;
    } catch (error) {
      return null;
    }
  }

  async function load() {
    const params = new URLSearchParams(window.location.search);
    const file = params.get('file');
    const title = params.get('title') || 'Document';

    viewerTitle.textContent = title;

    if (!file) {
      viewerSubtitle.textContent = 'No source file was provided.';
      viewerContent.innerHTML = '<div class="viewer-empty"><p>Add a <code>file</code> query parameter to render a document.</p></div>';
      renderToc([]);
      return;
    }

    const sourceUrl = resolveSourceUrl(file);
    if (!sourceUrl) {
      viewerSubtitle.textContent = 'This document link is not allowed.';
      viewerContent.innerHTML = '<div class="viewer-empty"><p>Only same-origin markdown files can be rendered in this viewer.</p></div>';
      renderToc([]);
      return;
    }

    currentSourceUrl = sourceUrl;
    sourcePath.textContent = `${sourceUrl.pathname}${sourceUrl.search}`;
    sourceLink.href = sourceUrl.toString();
    viewerSubtitle.textContent = 'Rendered from source so notes, slide outlines, and README files open as readable pages instead of raw markdown.';
    document.title = `${title} — RAG for Everyone`;

    try {
      const response = await fetch(sourceUrl.toString(), { cache: 'no-store' });
      if (!response.ok) throw new Error(`Unable to load ${sourceUrl.pathname}`);
      const markdown = await response.text();
      const rendered = parseMarkdown(markdown);
      viewerContent.innerHTML = `<article class="viewer-prose">${rendered.html}</article>`;
      renderToc(rendered.toc);
    } catch (error) {
      viewerContent.innerHTML = `
        <div class="viewer-empty">
          <p>We could not render this file from the current environment.</p>
          <p>If you are opening the site directly from the filesystem, use the source-file link above or serve the course over HTTP so the viewer can fetch the markdown file.</p>
        </div>
      `;
      renderToc([]);
    }
  }

  document.addEventListener('DOMContentLoaded', load);
})();
