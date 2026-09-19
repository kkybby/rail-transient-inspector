# Data handling and security boundaries

The application has no analytics, remote CSV download, uploads, service worker, cookies or localStorage. Dependencies are vendored. The bundled build uses a hash-based Content Security Policy with `connect-src 'none'`; exported reports contain no executable scripts. Input file names and operator notes are escaped in HTML.

This does not control browser extensions, endpoint monitoring, your operating system, or a hosting provider's access logs. Reports deliberately include source filename/notes and may therefore be sensitive. Review before sharing. A SHA-256 is an input fingerprint, not proof of origin or authenticity.

The initial release limits CSV size to 10 MiB and samples to 200,000. Parsing is synchronous and can temporarily occupy the browser; very large or adversarial text may still affect responsiveness. Use trusted captures. Security/side-channel testing is not comprehensive.

Do not commit real customer/company captures, credentials, source designs or identifying information. File a public issue only with sanitized reproductions. If a report contains confidential information, remove it before submitting an issue.
