# Security and private data

The application is a local CLI. It is not a web service. The preparation workflow does not call models or cloud integrations.

Keep these out of commits, issues, logs, and screenshots:

- API keys, database passwords, filesystem tokens, memory-space keys, and authentication headers.
- Personal notes, derived personal context, private source metadata, and raw third-party archives.
- Generated context packets and reports, which can contain private source excerpts.
- Global agent configuration and local authentication stores.

The runtime constrains file paths to its selected root, checks source hashes, bounds context size, treats retrieved text as untrusted data, and redacts configuration status. HTML import stores data without executing scripts or fetching linked resources. These protections do not make source instructions trustworthy or protect against an already-compromised local account.

Report a vulnerability privately through a maintainer-approved channel. Do not open a public issue containing credentials, personal source text, or an exploit against someone else's workspace. A private reporting address has not been configured yet.

If a secret reaches a commit or remote service, revoke or rotate it first. Adding an ignore rule afterward does not remove it from history. Review access and history before sharing again.
