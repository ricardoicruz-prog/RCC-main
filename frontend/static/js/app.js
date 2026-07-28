let currentData = null;
let selectedIndustry = 'all';

// ── Industry chips ──────────────────────────────────────────
async function loadIndustries() {
  try {
    const resp = await fetch('/api/industries');
    const industries = await resp.json();
    const container = document.getElementById('industryChips');
    container.innerHTML = Object.entries(industries).map(([key, val]) => `
      <button
        class="industry-chip ${key === 'all' ? 'active' : ''}"
        data-key="${key}"
        onclick="selectIndustry('${key}', this)"
      >${val.emoji} ${val.label}</button>
    `).join('');
  } catch (e) {
    // silently fail — chips just won't show
  }
}

function selectIndustry(key, btn) {
  selectedIndustry = key;
  document.querySelectorAll('.industry-chip').forEach(c => c.classList.remove('active'));
  btn.classList.add('active');
}

// ── Scan ────────────────────────────────────────────────────
async function runScan(forceRefresh = false) {
  showLoading();

  const msgEl = document.getElementById('loadingMsg');
  const ind = document.querySelector('.industry-chip.active');
  const indLabel = ind ? ind.textContent.trim() : 'your niche';
  const msgs = [
    `Scanning Reddit for ${indLabel} discussions…`,
    'Fetching Hacker News discussions…',
    `Searching Bluesky for ${indLabel} conversations…`,
    'Pulling YouTube videos…',
    'Scraping industry sites…',
    'Scoring by engagement heat…',
    'Clustering topic themes…',
    'Almost done…',
  ];
  let msgIdx = 0;
  const msgInterval = setInterval(() => {
    msgIdx = (msgIdx + 1) % msgs.length;
    msgEl.textContent = msgs[msgIdx];
  }, 4000);

  try {
    const resp = await fetch('/api/scan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ force_refresh: forceRefresh, industry: selectedIndustry }),
    });

    clearInterval(msgInterval);

    if (!resp.ok) throw new Error(`Server error: ${resp.status}`);

    const json = await resp.json();
    currentData = json.data;
    renderResults(json.status);
  } catch (err) {
    clearInterval(msgInterval);
    showError(err.message);
  }
}

function showLoading() {
  document.getElementById('idleState').style.display = 'none';
  document.getElementById('loadingState').style.display = 'flex';
  document.getElementById('results').style.display = 'none';
  document.getElementById('exportBtn').style.display = 'none';
  document.getElementById('scanBtn').disabled = true;
  document.getElementById('refreshBtn').disabled = true;
}

function showError(msg) {
  document.getElementById('loadingState').style.display = 'none';
  document.getElementById('idleState').style.display = 'flex';
  document.getElementById('idleState').querySelector('p').textContent = `Error: ${msg}`;
  document.getElementById('scanBtn').disabled = false;
  document.getElementById('refreshBtn').disabled = false;
}

function renderResults(status) {
  document.getElementById('loadingState').style.display = 'none';
  document.getElementById('idleState').style.display = 'none';
  document.getElementById('results').style.display = 'block';
  document.getElementById('exportBtn').style.display = 'inline-block';
  document.getElementById('scanBtn').disabled = false;
  document.getElementById('refreshBtn').disabled = false;

  const d = currentData;
  const total = d.total_fetched || 0;
  const pc = d.platform_counts || {};
  const indLabel = d.industry_label ? ` · ${d.industry_label}` : '';
  const ytPart = pc.youtube ? `, YouTube: ${pc.youtube}` : '';
  const fcPart = pc.firecrawl ? `, Web: ${pc.firecrawl}` : '';
  document.getElementById('statsText').textContent =
    `${total} posts scanned${indLabel} — Reddit: ${pc.reddit || 0}, HN: ${pc.hackernews || 0}, Bluesky: ${pc.bluesky || 0}${ytPart}${fcPart}`;

  const badge = document.getElementById('cacheLabel');
  badge.textContent = status === 'cached' ? 'Cached' : 'Fresh';
  badge.className = 'cache-badge ' + (status === 'cached' ? 'cached' : 'fresh');

  renderEngageFeed(d.engage || []);
  renderTopics(d.topics || []);
}

// ── CSV Export ───────────────────────────────────────────────
function exportCSV() {
  if (!currentData) return;

  const ind = currentData.industry_label || 'All Industries';
  const date = new Date().toISOString().slice(0, 10);

  const rows = [
    ['Title', 'URL', 'Platform', 'Source', 'Heat Score', 'Age (hours)', 'Upvotes', 'Comments', 'Pain Signal', 'Industry'],
  ];

  (currentData.engage || []).forEach(item => {
    rows.push([
      item.title || '',
      item.url || '',
      item.platform || '',
      item.source || '',
      item.heat_score != null ? item.heat_score.toFixed(2) : '',
      item.age_hours || '',
      item.raw_score || 0,
      item.comment_count || 0,
      item.pain_signal || '',
      ind,
    ]);
  });

  const csv = rows.map(r =>
    r.map(v => `"${String(v).replace(/"/g, '""')}"`).join(',')
  ).join('\n');

  const blob = new Blob(['﻿' + csv], { type: 'text/csv;charset=utf-8;' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `rcc-${ind.toLowerCase().replace(/[^a-z0-9]+/g, '-')}-${date}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

// ── Render helpers ───────────────────────────────────────────
function heatBadge(score) {
  if (score >= 5) return '<span class="heat-badge heat-high">🔥 Hot</span>';
  if (score >= 2) return '<span class="heat-badge heat-mid">↑ Rising</span>';
  return '<span class="heat-badge heat-low">· Active</span>';
}

function painBadge(signal) {
  if (!signal) return '';
  return `<span class="pain-badge" title="${escHtml(signal)}">🚨 Pain Point</span>`;
}

function platformPill(platform) {
  const labels = { reddit: 'Reddit', hackernews: 'HN', bluesky: 'Bluesky', youtube: 'YouTube', firecrawl: 'Web' };
  const cls = { reddit: 'pill-reddit', hackernews: 'pill-hackernews', bluesky: 'pill-bluesky', youtube: 'pill-youtube', firecrawl: 'pill-firecrawl' };
  return `<span class="platform-pill ${cls[platform] || ''}">${labels[platform] || platform}</span>`;
}

function age(hours) {
  if (hours < 1) return 'just now';
  if (hours < 24) return `${Math.round(hours)}h ago`;
  return `${Math.round(hours / 24)}d ago`;
}

function renderEngageFeed(items) {
  const el = document.getElementById('engageList');
  if (!items.length) {
    el.innerHTML = '<p style="color:var(--text-muted);text-align:center;padding:40px">No recent posts found. Try a Fresh Scan or check back later.</p>';
    return;
  }

  el.innerHTML = items.map(item => {
    const snippet = item.text && item.text !== item.title
      ? `<p class="post-text">${escHtml(item.text.slice(0, 200))}${item.text.length > 200 ? '…' : ''}</p>`
      : '';
    return `
      <div class="post-card${item.pain_signal ? ' has-pain' : ''}">
        <div class="post-header">
          <a href="${escHtml(item.url)}" target="_blank" rel="noopener" class="post-title">${escHtml(item.title)}</a>
          <div class="post-badges">
            ${painBadge(item.pain_signal)}
            ${heatBadge(item.heat_score)}
          </div>
        </div>
        ${snippet}
        <div class="post-meta">
          ${platformPill(item.platform)}
          <span class="meta-chip">📌 ${escHtml(item.source)}</span>
          <span class="meta-chip">🕒 ${age(item.age_hours)}</span>
          ${item.raw_score ? `<span class="meta-chip">▲ ${item.raw_score}</span>` : ''}
          ${item.comment_count ? `<span class="meta-chip">💬 ${item.comment_count}</span>` : ''}
        </div>
      </div>
    `;
  }).join('');
}

function renderTopics(summaries) {
  const el = document.getElementById('topicsList');
  if (!summaries.length) {
    el.innerHTML = '<p style="color:var(--text-muted);text-align:center;padding:40px">No topics clustered yet.</p>';
    return;
  }

  el.innerHTML = summaries.map((s, i) => {
    const platformTags = s.platforms.map(p => platformPill(p)).join(' ');
    const postsHtml = s.top_items.map(item => `
      <div class="topic-post-row">
        ${platformPill(item.platform)}
        <a href="${escHtml(item.url)}" target="_blank" rel="noopener" class="topic-post-link">${escHtml(item.title)}</a>
        <span class="meta-chip" style="flex-shrink:0">${age(item.age_hours)}</span>
      </div>
    `).join('');

    return `
      <div class="topic-cluster">
        <div class="topic-header" onclick="toggleCluster(this)">
          <span class="topic-name">${escHtml(s.topic)}</span>
          <div class="topic-stats">
            ${platformTags}
            <span>${s.post_count} posts</span>
            <span style="color:var(--text);font-size:14px">${i === 0 ? '▾' : '▸'}</span>
          </div>
        </div>
        <div class="topic-posts" ${i > 0 ? 'style="display:none"' : ''}>
          ${postsHtml}
        </div>
      </div>
    `;
  }).join('');
}

function toggleCluster(header) {
  const posts = header.nextElementSibling;
  const arrow = header.querySelector('span:last-child');
  const open = posts.style.display !== 'none';
  posts.style.display = open ? 'none' : 'flex';
  arrow.textContent = open ? '▸' : '▾';
}

function showTab(name, btn) {
  document.getElementById('engageTab').style.display = name === 'engage' ? 'block' : 'none';
  document.getElementById('topicsTab').style.display = name === 'topics' ? 'block' : 'none';
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  btn.classList.add('active');
}

function escHtml(str) {
  return String(str || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// ── Init ─────────────────────────────────────────────────────
loadIndustries();
