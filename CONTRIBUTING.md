# Contributing

Keep changes focused. Include a minimal synthetic input and expected result for analysis changes. Run `npm test`, then rebuild `standalone.html` with `python tools/build_standalone.py`. Do not hand-edit the generated bundle.

Preserve units and distinguish software tests from hardware validation. A bug fix or new parser adapter must never silently drop samples, guess units or turn correlation into causality. Do not upload private customer traces. Document upstream sources and licenses for imported code.

AI-assisted contributions are welcome when their use is disclosed and the changes are reviewed/tested. Avoid invented experience, fake bench results or backdated commits.
