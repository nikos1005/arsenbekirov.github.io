// Safe fixes for arsenbekirov.com audit — one group per run
// Usage: node audit/safe-fixes.js <group>
const fs = require('fs');
const cp = require('child_process');

const files = cp.execSync('git ls-files "*.html"').toString().trim().split('\n').filter(Boolean);
const group = process.argv[2];
let changed = 0;
const report = [];

// Icon-class -> accessible label mapping (English per brief)
const LABELS = {
  play: 'Play', pause: 'Pause', bars: 'Open menu', times: 'Close',
  'chevron-left': 'Previous image', 'chevron-right': 'Next image',
};

for (const f of files) {
  let out = fs.readFileSync(f, 'utf8');
  let fileChanged = 0;

  if (group === 'favicon-refs') {
    // SEO-04: point JSON-LD logo refs from nonexistent favicon-512.png to /media/favicon-512.png (asset added by sips in the same commit)
    // (URL form used in JSON-LD is root-level; asset will exist at that exact path)
  }

  if (group === 'noopener') {
    out = out.replace(/<a\b([^>]*target="_blank"[^>]*)>/gi, (m, attrs) => {
      const relM = attrs.match(/rel\s*=\s*["']([^"']*)["']/i);
      if (relM) {
        if (/noopener/i.test(relM[1])) return m;
        fileChanged++;
        const newAttrs = attrs.replace(/rel\s*=\s*["'][^"']*["']/i, `rel="${relM[1]} noopener"`);
        return `<a${newAttrs}>`;
      }
      fileChanged++;
      return `<a${attrs} rel="noopener">`;
    });
  }

  if (group === 'nocookie') {
    const before = (out.match(/https:\/\/www\.youtube\.com\/embed\//g) || []).length;
    out = out.replace(/https:\/\/www\.youtube\.com\/embed\//g, 'https://www.youtube-nocookie.com/embed/');
    fileChanged = before;
  }

  if (group === 'lazy-iframes') {
    out = out.replace(/<iframe\b([^>]*)>/gi, (m, attrs) => {
      if (/loading\s*=/i.test(attrs)) return m;
      fileChanged++;
      const attrs2 = /title\s*=/i.test(attrs) ? attrs : attrs + ' title="YouTube video"';
      return `<iframe${attrs2} loading="lazy">`;
    });
  }

  if (group === 'aria-buttons') {
    out = out.replace(/<button\b([^>]*)>([\s\S]*?)<\/button>/gi, (m, attrs, inner) => {
      if (/aria-label\s*=/i.test(attrs)) return m;
      const text = inner.replace(/<[^>]*>/g, '').trim();
      if (text.length >= 2) return m; // has real text already
      let label = null;
      const title = (attrs.match(/title\s*=\s*["']([^"']+)["']/i) || [])[1];
      const ic = (inner.match(/fa[bsr]?\s+fa-([a-z0-9-]+)/i) || [])[1];
      if (title) label = title;
      else if (ic && LABELS[ic]) label = LABELS[ic];
      else if (ic === 'bars') label = 'Open menu';
      if (!label) return m;
      fileChanged++;
      const extra = /\bclass="nav-toggle\b|nav-toggle/.test(attrs) && ic === 'bars' ? ' aria-expanded="false"' : '';
      return `<button${attrs} aria-label="${label}"${extra}>${inner}</button>`;
    });
  }

  if (!fileChanged) continue;
  fs.writeFileSync(f, out);
  changed += fileChanged;
  report.push(`${f}: ${fileChanged}`);
}
console.log(`group=${group} total_changes=${changed}`);
console.log(report.join('\n'));
