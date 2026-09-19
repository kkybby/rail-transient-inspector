# Repository publication

Public target: `kkybby/rail-transient-inspector`. A separate public repository was created by the owner. The private work-experience archive remains unchanged.

The source commit contains the application, tests, build scripts, documentation, licenses and CI. The workflow restores the immutable Papa Parse file only if missing and verifies its SHA-256. It runs Node tests, builds the offline application and synthetic reports, then runs Chromium smoke checks. Actual demo screenshots, reports, the bundle and integrity manifest are committed by a separate least-privilege publication job after the checks pass.

The publication job runs only for pushes to the owner's main branch, never for pull requests. It commits a specific generated-file allowlist and never force-pushes. A concurrent change or insufficient permission causes a failure rather than overwriting another branch update. Check the Actions run before calling CI successful.

There is no Pages deployment, commercial checkout, external-contact form or analytics service configured. GitHub hosts the source and generated files; opening an HTML source view on GitHub does not run the app. Download the repository and open `standalone.html` locally.

The project contains no company/customer files. All supplied waveforms and reports are synthetic. The only imported runtime source is the unchanged MIT-licensed Papa Parse dependency listed in THIRD_PARTY_NOTICES.md.
