/* UI only: no fetch, network parsing, telemetry, or localStorage. */
(function () {
  'use strict';
  const C=window.RailInspector, R=window.RailReport, $=id=>document.getElementById(id);
  const state={raw:'',bytes:null,name:'',origin:'',table:null,samples:null,result:null,generation:0};
  function message(text) { $('message').textContent=text; $('message').hidden=!text; }
  function invalidate() {
    state.generation++; state.result=null; $('result-body').hidden=true; $('empty').hidden=false;
    $('html-report').disabled=true; $('json-report').disabled=true;
  }
  function field(id) {
    if ($(id).value.trim()==='') throw new Error('Fill in '+id.replaceAll('-',' ')+'.');
    const v=Number($(id).value); if (!Number.isFinite(v)) throw new Error('Invalid number in '+id+'.'); return v;
  }
  function parseOptions() { return {skip_lines:field('skip'),delimiter:$('delimiter').value==='tab'?'\t':$('delimiter').value}; }
  function options(id,headers,selected,none) {
    const select=$(id); select.replaceChildren();
    if(none) select.add(new Option('None',''));
    for(const h of headers) select.add(new Option(h,h));
    select.value=headers.includes(selected)?selected:(none?'':headers[0]);
  }
  function mapColumns(reset) {
    state.table=C.parseTable(state.raw,parseOptions());
    const h=state.table.headers;
    options('time-column',h,reset?h[0]:$('time-column').value,false);
    options('voltage-column',h,reset?h[1]:$('voltage-column').value,false);
    options('trigger-column',h,reset?'':$('trigger-column').value,true);
    if(reset) for(const id of ['time-unit','voltage-unit','trigger-unit']) $(id).value='';
    $('source-name').textContent=state.name;
    $('sample-summary').textContent=state.table.records.length.toLocaleString()+' samples ready';
  }
  function setOrigin(demo) {
    const b=$('origin').querySelector('.badge');
    b.textContent=demo?'SYNTHETIC DEMO':'USER-PROVIDED CSV';
    $('origin').lastElementChild.textContent=demo?'Generated signal, not a bench measurement.':'Origin and instrument accuracy are unverified. Review your capture notes.';
  }
  async function hash(bytes) {
    if(!window.crypto?.subtle) return null;
    const d=await window.crypto.subtle.digest('SHA-256',bytes);
    return Array.from(new Uint8Array(d),x=>x.toString(16).padStart(2,'0')).join('');
  }
  function mapping() {
    return {time_column:$('time-column').value,voltage_column:$('voltage-column').value,
      trigger_column:$('trigger-column').value,time_unit:$('time-unit').value,
      voltage_unit:$('voltage-unit').value,trigger_unit:$('trigger-unit').value,decimal:$('decimal').value};
  }
  function config() {
    return {nominal_v:field('nominal'),trip_v:field('trip'),recover_v:field('recover'),
      min_duration_s:field('min-duration')*1e-6,gap_factor:field('gap-factor'),
      trigger_level_v:field('trigger-level'),trigger_edge:$('edge').value,
      trigger_window_s:field('trigger-window')*1e-3};
  }
  function metric(id,value,unit) {
    $(id).replaceChildren(document.createTextNode(value)); const el=document.createElement('small');el.textContent=unit;$(id).append(el);
  }
  function render(r,samples) {
    metric('metric-min',R.fmt(r.capture.minimum_v),'V');
    metric('metric-drop',R.fmt(r.capture.drop_from_nominal_v*1000,1),'mV');
    metric('metric-count',String(r.event_counts.kept),'');
    $('metric-count-note').textContent=r.event_counts.raw+' raw · '+r.event_counts.excluded_short_complete+' filtered · '+r.event_counts.incomplete+' incomplete';
    const longest=r.events.reduce((max,e)=>!max||e.duration_s>max.duration_s?e:max,null);
    metric('metric-longest',longest?(longest.complete?'':'≥ ')+R.fmt(longest.duration_s*1000,3):'0.000','ms');
    $('sample-summary').textContent=r.capture.sample_count.toLocaleString()+' samples · '+R.fmt(r.capture.span_s*1000,2)+' ms span';
    $('chart').innerHTML=R.chart(samples,r); // SVG contains numeric values only.
    $('event-table').innerHTML=R.eventTable(r); // Table contains numeric and fixed labels only.
    $('complete-count').textContent=r.event_counts.kept-r.event_counts.incomplete+' complete';
    $('quality').textContent='Median Δt '+R.fmt(r.capture.median_sample_interval_s*1e6,2)+' µs · '+r.gaps.length+' gaps · extrema-preserving display';
    $('warnings').replaceChildren(...r.warnings.map(w=>{const li=document.createElement('li');li.textContent=w;return li;}));
    if(r.events.length>200||r.triggers.length>1000||r.gaps.length>2000){const li=document.createElement('li');li.textContent='Display limits: 200 table rows, 2,000 event/gap overlays, 1,000 trigger markers. Full results are in JSON.';$('warnings').append(li);}
    $('result-body').hidden=false;$('empty').hidden=true;$('html-report').disabled=false;$('json-report').disabled=false;
  }
  async function analyze() {
    invalidate(); const generation=state.generation;
    try {
      if(!state.raw) throw new Error('Choose a CSV or load the synthetic demo.');
      const table=C.parseTable(state.raw,parseOptions()), m=mapping(), cfg=config();
      const samples=C.toSamples(table,m), r=C.analyze(samples,cfg);
      const fingerprint=await hash(state.bytes);
      if(generation!==state.generation) return;
      r.source={name:state.name,origin:state.origin,sha256:fingerprint,note:$('note').value.slice(0,2000),
        mapping:m,preamble_lines_skipped:table.preamble_lines_skipped,blank_rows_skipped:table.blank_rows_skipped,
        delimiter:table.delimiter,generated_at:new Date().toISOString(),hardware_validation:'not performed by this tool'};
      state.table=table;state.samples=samples;state.result=r;message('');render(r,samples);
    } catch(err){message(err.message);}
  }
  function download(content,type,name) {
    const url=URL.createObjectURL(new Blob([content],{type})),a=document.createElement('a');
    a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
  }
  async function loadDemo() {
    invalidate();state.raw=C.demoCsv();state.bytes=new TextEncoder().encode(state.raw);
    state.name='synthetic-demo.csv';state.origin='SYNTHETIC DEMO: generated mathematically; not acquired from hardware';
    for(const [id,val] of Object.entries({skip:0,delimiter:'',decimal:'.',nominal:3.3,trip:3,recover:3.08,
      'min-duration':20,'gap-factor':3,'trigger-level':1.65,'trigger-window':2,edge:'rising',note:''})) $(id).value=val;
    $('file').value=''; mapColumns(true);$('time-unit').value='s';$('voltage-unit').value='V';$('trigger-unit').value='V';
    $('trigger-column').value='trigger_v';setOrigin(true);await analyze();
  }
  $('analysis-form').addEventListener('submit',e=>{e.preventDefault();analyze();});
  $('analysis-form').addEventListener('input',()=>{invalidate();message('Settings changed. Apply Analyze capture to produce a fresh report.');});
  $('file').addEventListener('change',async()=>{
    invalidate();const generation=state.generation,file=$('file').files[0];if(!file)return;
    try{
      if(file.size>C.MAX_BYTES)throw new Error('File exceeds the 10 MiB limit.');
      const bytes=await file.arrayBuffer();if(generation!==state.generation)return;
      state.raw=new TextDecoder('utf-8',{fatal:true}).decode(bytes);state.bytes=bytes;state.name=file.name;
      state.origin='USER-PROVIDED CSV: measurement provenance not independently verified';
      $('note').value='';setOrigin(false);mapColumns(true);message('CSV loaded. Confirm the units, channels and analysis thresholds.');
    }catch(err){message('Import stopped: '+err.message);}
  });
  $('remap').addEventListener('click',()=>{invalidate();try{mapColumns(false);message('Header re-read. Verify column mapping, then analyze.');}catch(err){message(err.message);}});
  $('demo').addEventListener('click',loadDemo);
  $('sample-download').addEventListener('click',()=>download(C.demoCsv(),'text/csv','synthetic-demo.csv'));
  $('html-report').addEventListener('click',()=>{if(state.result)download(R.html(state.samples,state.result),'text/html','rail-transient-report.html');});
  $('json-report').addEventListener('click',()=>{if(state.result)download(JSON.stringify(state.result,null,2)+'\n','application/json','rail-transient-report.json');});
  loadDemo();
})();
