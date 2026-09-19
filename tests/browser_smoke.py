"""Optional Playwright/Chromium smoke suite; loads the offline bundle without navigation."""
from playwright.sync_api import sync_playwright
from pathlib import Path
import json
import os
import shutil
import tempfile
root=Path(__file__).resolve().parents[1]
artifacts=Path(os.environ.get('RTI_ARTIFACT_DIR') or tempfile.mkdtemp(prefix='rti-browser-'))
artifacts.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=os.environ.get('BROWSER_EXECUTABLE') or shutil.which('chromium'),headless=True,args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1500,'height':1250},device_scale_factor=1)
 errors=[]; requests=[]
 page.on('pageerror',lambda err: errors.append(str(err)))
 page.on('request',lambda req: requests.append(req.url))
 page.set_content((root/'standalone.html').read_text(), wait_until='load')
 page.wait_for_function("document.getElementById('metric-count').textContent.trim() === '2'")
 page.screenshot(path=str(artifacts/'app-screenshot.png'),full_page=True)
 print('demo count', page.locator('#metric-count').inner_text())
 print('errors',errors)
 print('requests',requests)
 page.locator('#trip').fill('2.5');page.locator('#recover').fill('2.6')
 assert page.locator('#json-report').is_disabled()
 page.locator('#analyze').click();page.wait_for_function("document.getElementById('metric-count').textContent.trim() === '0'")
 page.locator('#demo').click();page.wait_for_function("document.getElementById('metric-count').textContent.trim() === '2'")
 with page.expect_download() as dl: page.locator('#json-report').click()
 out=dl.value;out.save_as(str(artifacts/'report.json'))
 rr=json.loads((artifacts/'report.json').read_text());assert rr['event_counts']['kept']==2
 assert rr['source']['sha256'] is None or len(rr['source']['sha256'])==64
 page.locator('#file').set_input_files({'name':'trial.csv','mimeType':'text/csv','buffer':b't,v\n0,3.3\n1,2.7\n2,3.3\n'})
 page.wait_for_function("document.getElementById('source-name').textContent==='trial.csv'")
 assert page.locator('#time-unit').input_value()==''
 page.locator('#analyze').click();assert 'Confirm' in page.locator('#message').inner_text()
 page.locator('#time-unit').select_option('ms');page.locator('#voltage-unit').select_option('V');page.locator('#analyze').click()
 page.wait_for_function("document.getElementById('metric-count').textContent.trim() === '1'")
 page.locator('#file').set_input_files({'name':'bad.csv','mimeType':'text/csv','buffer':b't,v\n0,3.3\n1,missing\n2,3.3\n'})
 page.wait_for_function("document.getElementById('source-name').textContent==='bad.csv'")
 page.locator('#time-unit').select_option('ms');page.locator('#voltage-unit').select_option('V');page.locator('#analyze').click()
 assert 'invalid' in page.locator('#message').inner_text();assert page.locator('#json-report').is_disabled()
 page.locator('#demo').click();page.wait_for_function("document.getElementById('metric-count').textContent.trim() === '2'")
 page.set_viewport_size({'width':390,'height':844});page.screenshot(path=str(artifacts/'mobile-screenshot.png'),full_page=True)
 assert page.evaluate('document.documentElement.scrollWidth')<=390
 assert errors == [], errors
 assert requests == [], requests
 print('BROWSER CHECKS PASSED')
 print('Temporary screenshots/reports:', artifacts)
 print('external', [u for u in requests if u.startswith(('http://','https://')) and not u.startswith('http://127.0.0.1:')])
 print('console errors',errors)
 b.close()
