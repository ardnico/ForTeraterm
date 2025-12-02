# Project Plans

Pragmatic expansions that deliver clear operator value without bloating the launcher:

1. **Profile portability (export/import with secrets stripping)**
   - Allow exporting profiles/command sets without credentials, plus selective import with conflict resolution. Saves time when sharing vetted settings across teams while avoiding secret leaks.

2. **Connection health checks and retry policy**
   - Add optional pre-flight ping/port checks and configurable retry intervals. Reduces failed runs from typos or transient network blips.

3. **Audit-friendly history view**
   - Extend history filtering with date ranges and CSV export. Makes it usable for audits and quick incident reviews rather than a basic log list.

4. **Credential usage guardrails**
   - Warn when using stale credentials, and allow per-profile “require password every time” toggles. Prevents silent reuse of outdated secrets.

5. **Quick-connect scratchpad**
   - Lightweight one-off connection launcher that never writes to the database. Avoids cluttering profiles when testing temporary hosts.
