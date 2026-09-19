"""Restore the exact reviewed SPDX copy of CERN-OHL-S-2.0; refuse different bytes."""
from pathlib import Path
import urllib.request,hashlib
root=Path(__file__).resolve().parents[1]
p=root/'LICENSES/CERN-OHL-S-2.0.txt';p.parent.mkdir(exist_ok=True)
expected='114486fd9446c39da1b69101597e25e33877fca6'
data=p.read_bytes() if p.exists() else urllib.request.urlopen('https://raw.githubusercontent.com/spdx/license-list-data/main/text/CERN-OHL-S-2.0.txt',timeout=30).read()
actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
if actual!=expected:raise RuntimeError('License text differs from the reviewed SPDX blob; manual review required.')
p.write_bytes(data)
print('Complete CERN-OHL-S-2.0 licence matches reviewed blob '+actual)
