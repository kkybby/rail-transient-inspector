(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.RailReport = factory();
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  function escape(s) { return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
  function fmt(n, digits = 3) { return n === null || n === undefined ? 'n/a' : Number(n).toFixed(digits); }
  function pathIndices(samples, start, end, step) {
    const ids = [];
    for (let i = start; i < end; i += step) {
      const stop = Math.min(end, i + step); let min = i, max = i;
      for (let j = i + 1; j < stop; j++) { if (samples[j].v < samples[min].v) min = j; if (samples[j].v > samples[max].v) max = j; }
      ids.push(...[...new Set([i, min, max, stop - 1])].sort((a,b) => a-b));
    }
    return ids;
  }
  function chart(samples, r) {
    const W = 1080, H = 340, left = 62, right = 26, top = 32, bottom = 42;
    const c = r.configuration, low = Math.min(r.capture.minimum_v, c.trip_v) - 0.10;
    const high = Math.max(r.capture.maximum_v, c.nominal_v) + 0.13;
    const x = t => left + (t-r.capture.start_s) / r.capture.span_s * (W-left-right);
    const y = v => top + (high-v) / (high-low) * (H-top-bottom);
    let svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" role="img" aria-label="Rail voltage against time, with analysis thresholds, event windows and trigger markers"><rect width="1080" height="340" fill="#ffffff"/>`;
    for (let i = 0; i <= 5; i++) {
      const value = low+(high-low)*i/5, yy = y(value);
      svg += `<path d="M${left} ${yy}H${W-right}" stroke="#e5eaf0"/><text x="${left-10}" y="${yy+4}" text-anchor="end" font-family="monospace" font-size="12" fill="#596a7c">${fmt(value,2)}</text>`;
    }
    for (let i = 0; i <= 5; i++) {
      const t = r.capture.start_s+r.capture.span_s*i/5, xx=x(t);
      svg += `<path d="M${xx} ${top}V${H-bottom}" stroke="#edf0f4"/><text x="${xx}" y="${H-20}" text-anchor="middle" font-family="monospace" font-size="12" fill="#596a7c">${fmt(t*1000,2)}</text>`;
    }
    for (const g of r.gaps.slice(0,2000)) svg += `<rect x="${x(g.start_s)}" y="${top}" width="${Math.max(1,x(g.end_s)-x(g.start_s))}" height="${H-top-bottom}" fill="#e8eaed"/>`;
    for (const ev of r.events.slice(0,2000)) svg += `<rect x="${x(ev.start_s)}" y="${top}" width="${Math.max(1,x(ev.end_s)-x(ev.start_s))}" height="${H-top-bottom}" fill="#ffb454" opacity="0.15"/>`;
    const lines = [[c.nominal_v,'#95a2af','3 5','nominal'],[c.trip_v,'#bc5522','8 5','trip'],[c.recover_v,'#128477','2 4','recovery']];
    for (const [v,col,dash,label] of lines) svg += `<path d="M${left} ${y(v)}H${W-right}" stroke="${col}" stroke-dasharray="${dash}"/><text x="${W-right-3}" y="${y(v)-6}" text-anchor="end" font-family="monospace" font-size="11" fill="${col}">${label} ${fmt(v,2)} V</text>`;
    for (const t of r.triggers.slice(0,1000)) svg += `<path d="M${x(t.time_s)} ${top}V${H-bottom}" stroke="#9a720e" stroke-dasharray="2 6"/><path d="M${x(t.time_s)-4} ${top-8}h8l-4 7z" fill="#9a720e"/>`;
    const bounds=[0,...r.gaps.map(g=>g.before_index),samples.length];
    const step=Math.max(1,Math.ceil(samples.length/1200));
    for(let s=0;s<bounds.length-1;s++) {
      const ids=pathIndices(samples,bounds[s],bounds[s+1],step);
      const d=ids.map((id,k)=>(k?'L':'M')+fmt(x(samples[id].t),2)+' '+fmt(y(samples[id].v),2)).join(' ');
      svg+=`<path d="${d}" fill="none" stroke="#173c57" stroke-width="2" stroke-linejoin="round"/>`;
    }
    svg += `<circle cx="${x(r.capture.minimum_at_s)}" cy="${y(r.capture.minimum_v)}" r="4" fill="#ffffff" stroke="#173c57" stroke-width="2"/><text x="${left}" y="16" font-family="monospace" font-size="11" fill="#596a7c">RAIL / V</text><text x="${W-right}" y="${H-2}" text-anchor="end" font-family="monospace" font-size="11" fill="#596a7c">TIME / ms</text></svg>`;
    return svg;
  }
  function eventTable(r) {
    const rows=r.events.slice(0,200).map(ev=>`<tr><td>EV${String(ev.id).padStart(2,'0')}</td><td>${fmt(ev.start_s*1000)}</td><td>${fmt(ev.minimum_v)}</td><td>${ev.complete?'':'≥ '}${fmt(ev.duration_s*1e6,1)}</td><td>${fmt(ev.trigger_lag_s===null?null:ev.trigger_lag_s*1e6,1)}</td><td>${ev.complete?'Complete':'Boundary / gap'}</td></tr>`).join('');
    return `<table><thead><tr><th>Event</th><th>Onset / ms</th><th>Minimum / V</th><th>Duration / µs</th><th>Trigger lag / µs</th><th>Observation</th></tr></thead><tbody>${rows||'<tr><td colspan="6">No retained events at these analysis settings.</td></tr>'}</tbody></table>`;
  }
  function html(samples,r) {
    const source=r.source||{name:'unspecified',origin:'unspecified / provenance unverified'};
    return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; img-src data:; base-uri 'none'; form-action 'none'"><title>Rail Transient Inspector | Report</title><style>body{font:15px/1.65 system-ui,sans-serif;color:#183144;max-width:1100px;margin:48px auto;padding:0 24px}h1{font-size:36px;margin-bottom:8px}h2{margin-top:30px}small,.muted{color:#596a7c}.status{padding:16px;border-left:4px solid #d6922d;background:#fff7e8}table{width:100%;border-collapse:collapse;font-size:13px}td,th{padding:12px 8px;border-bottom:1px solid #dce4eb;text-align:left}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px}svg{width:100%;height:auto}.grid{display:flex;gap:28px;flex-wrap:wrap}.grid strong{display:block;font:28px monospace}footer{border-top:1px solid #dce4eb;margin-top:40px;padding-top:18px}@media print{body{margin:0}details{display:block}}</style></head><body><small>ENGINEERING TOOL • v${escape(r.version)}</small><h1>Rail transient report</h1><p>${escape(source.name)}</p><p class="status"><strong>Data origin: ${escape(source.origin)}</strong><br>Automated waveform analysis only. Hardware, instrument accuracy and MCU reset behavior have not been independently validated.</p><div class="grid"><p>Capture minimum<strong>${fmt(r.capture.minimum_v)} V</strong></p><p>Drop from nominal<strong>${fmt(r.capture.drop_from_nominal_v*1000,1)} mV</strong></p><p>Retained / raw events<strong>${r.event_counts.kept} / ${r.event_counts.raw}</strong></p><p>Median sample interval<strong>${fmt(r.capture.median_sample_interval_s*1e6,3)} µs</strong></p></div>${chart(samples,r)}<p class="muted">Solid: rail voltage. Dashed: trip. Dotted: recovery and trigger markers. Event duration runs from trip entry to recovery, including the hysteresis band. Visualization is downsampled with extrema retained; metrics use all samples. Up to 2,000 event/gap overlays, 1,000 triggers and 200 table rows are displayed; JSON contains every result.</p><h2>Event log</h2>${eventTable(r)}<h2>Analysis settings</h2><p>Nominal ${fmt(r.configuration.nominal_v)} V; trip ${fmt(r.configuration.trip_v)} V; recovery ${fmt(r.configuration.recover_v)} V; minimum event ${fmt(r.configuration.min_duration_s*1e6,1)} µs; gap factor ${r.configuration.gap_factor}. Trigger: ${escape(r.configuration.trigger_edge)} at ${fmt(r.configuration.trigger_level_v)} V within ${fmt(r.configuration.trigger_window_s*1000,2)} ms.</p><h2>Limitations and data quality</h2><ul>${r.warnings.map(w=>'<li>'+escape(w)+'</li>').join('')}</ul><h2>Capture notes</h2><p>${escape(source.note||'No operator notes supplied.')}</p><p>Input SHA-256: <code>${escape(source.sha256||'Unavailable')}</code></p><details><summary>Complete structured result, including excluded events</summary><pre>${escape(JSON.stringify(r,null,2))}</pre></details><footer>Rail Transient Inspector • AI-assisted implementation • CSV parsing: Papa Parse 5.5.3 (MIT, Matthew Holt). No claim of original CSV-parser authorship or certified hardware validation.</footer></body></html>`;
  }
  return Object.freeze({escape,fmt,chart,eventTable,html});
});
