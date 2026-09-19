#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),crypto=require('node:crypto');
const C=require('../src/core.js'),R=require('../src/report.js');
const HELP=`Rail Transient Inspector v${C.VERSION}
Offline usage (all channels share one time column):
  node tools/analyze.cjs --demo --out result.json --html result.html
  node tools/analyze.cjs --file capture.csv --time-column t --voltage-column CH1 --time-unit ms --voltage-unit V --nominal 3.3 --trip 3.0 --recover 3.08 --min-us 20 --out result.json
Optional: --trigger-column CH2 --trigger-unit V --trigger-level 1.65 --edge rising --window-ms 2 --gap-factor 3 --skip-lines 0 --delimiter comma|semicolon|tab|pipe|auto --decimal .|, --note "capture notes" --html report.html
Output defaults to JSON on stdout. Existing output files are not overwritten.
Thresholds are analysis limits, not device specifications. Only --demo labels data as synthetic.
`;
function run(argv){
  const allowed=new Set(['demo','help','file','time-column','voltage-column','time-unit','voltage-unit','trigger-column','trigger-unit','nominal','trip','recover','min-us','trigger-level','edge','window-ms','gap-factor','skip-lines','delimiter','decimal','note','out','html']);
  const a={};for(let i=0;i<argv.length;i++){
    const key=argv[i].replace(/^--/,'');if(!argv[i].startsWith('--')||!allowed.has(key))throw new Error('Unknown option: '+argv[i]);
    if(Object.hasOwn(a,key))throw new Error('Duplicate option: '+key);
    if(key==='help'||key==='demo')a[key]=true;
    else{if(i+1>=argv.length||argv[i+1].startsWith('--'))throw new Error('Missing value for '+key);a[key]=argv[++i];}
  }
  if(a.help){console.log(HELP);return;}
  if(!!a.demo===!!a.file)throw new Error('Choose exactly one of --demo or --file.');
  if(a.demo&&['nominal','trip','recover','time-column','voltage-column','time-unit','voltage-unit','trigger-column','trigger-unit','min-us','skip-lines','delimiter','decimal'].some(k=>Object.hasOwn(a,k)))throw new Error('Use --file samples/synthetic-demo.csv to customize demo analysis; --demo uses the reference configuration.');
  if(a.demo)Object.assign(a,{'time-column':'time_s','voltage-column':'rail_v','trigger-column':'trigger_v','time-unit':'s','voltage-unit':'V','trigger-unit':'V',nominal:'3.3',trip:'3.0',recover:'3.08','min-us':'20'});
  for(const k of ['time-column','voltage-column','time-unit','voltage-unit','nominal','trip','recover'])if(!Object.hasOwn(a,k))throw new Error('Required: --'+k);
  function num(k,def){if(a[k]!==undefined&&String(a[k]).trim()==='')throw new Error('Empty '+k);const v=Number(a[k]??def);if(!Number.isFinite(v))throw new Error('Invalid '+k);return v;}
  const delims={auto:'',comma:',',semicolon:';',tab:'\t',pipe:'|'};
  if(!Object.hasOwn(delims,a.delimiter||'auto'))throw new Error('Invalid delimiter.');
  if(a.file&&fs.statSync(a.file).size>C.MAX_BYTES)throw new Error('File exceeds the 10 MiB limit.');
  const bytes=a.demo?Buffer.from(C.demoCsv()):fs.readFileSync(a.file);
  const text=new TextDecoder('utf-8',{fatal:true}).decode(bytes);
  const table=C.parseTable(text,{skip_lines:num('skip-lines',0),delimiter:delims[a.delimiter||'auto']});
  const mapping={time_column:a['time-column'],voltage_column:a['voltage-column'],trigger_column:a['trigger-column']||'',time_unit:a['time-unit'],voltage_unit:a['voltage-unit'],trigger_unit:a['trigger-unit'],decimal:a.decimal||'.'};
  const samples=C.toSamples(table,mapping),r=C.analyze(samples,{nominal_v:num('nominal'),trip_v:num('trip'),recover_v:num('recover'),min_duration_s:num('min-us',0)*1e-6,gap_factor:num('gap-factor',3),trigger_level_v:num('trigger-level',1.65),trigger_edge:a.edge||'rising',trigger_window_s:num('window-ms',2)*1e-3});
  r.source={name:a.demo?'synthetic-demo.csv':require('node:path').basename(a.file),origin:a.demo?'SYNTHETIC DEMO: no hardware measured':'USER-PROVIDED CSV: provenance unverified',sha256:crypto.createHash('sha256').update(bytes).digest('hex'),mapping,note:a.note||'',delimiter:table.delimiter,preamble_lines_skipped:table.preamble_lines_skipped,blank_rows_skipped:table.blank_rows_skipped,hardware_validation:'not performed by this tool'};
  for(const k of ['out','html'])if(a[k]&&fs.existsSync(a[k]))throw new Error('Output exists; choose a new path: '+a[k]);
  if(a.out&&a.html&&require('node:path').resolve(a.out)===require('node:path').resolve(a.html))throw new Error('JSON and HTML output paths must differ.');
  const json=JSON.stringify(r,null,2)+'\n';if(a.out)fs.writeFileSync(a.out,json,{flag:'wx'});else process.stdout.write(json);
  if(a.html)fs.writeFileSync(a.html,R.html(samples,r),{flag:'wx'});
}
try{run(process.argv.slice(2));}catch(err){console.error('Analysis stopped: '+err.message+'\nRun with --help for usage.');process.exitCode=1;}
