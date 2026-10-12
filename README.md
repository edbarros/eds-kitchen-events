# Ed's Kitchen events feed

Public, data-only feed for the Ed's Kitchen Suite app (iPhone, iPad, Mac). No secrets live here.

- `events.json` is the live market/event list. The app fetches
  `https://raw.githubusercontent.com/edbarros/eds-kitchen-events/main/events.json`
  on launch, when it returns to the foreground, and when you tap Refresh.
- `app/` holds the signed web-page update (`manifest.json` + `index.html`) written by
  `scripts/publish_ota.py` in the app repo. The app verifies an Ed25519 signature before using it.
- `AGENT.md` is the playbook for the scheduled events agent.
- `validate.py` checks `events.json` the same way the app does; GitHub Actions runs it (and `test_validate.py`) on every push. Run it before every push.

## events.json format

```
{ "schema": 1, "updated": "2026-10-12T13:00:00Z", "events": [ ... ] }
```

Each event (fields the app requires are marked *):

| field | meaning |
|---|---|
| `id`* | lowercase slug, unique, e.g. `mansfield-fcm` |
| `n`* / `s` | full name / short name |
| `city`*, `v` | city, venue |
| `t` | `weekly`, `once`, `multi`, ... |
| `d` / `p` / `r` | dates as `MM-DD` (event days / preview days / rain dates) |
| `tm` | hours text |
| `st`* | `open`, `check`, `closed`, `tba`, `next` |
| `ck` | cottage food allowed: `yes`, `no`, `check` |
| `mi`* | one-way miles from Ovilla (number) |
| `fee`, `fn` | fee text, fee as a number |
| `dl` | application deadline `MM-DD` |
| `ap` | https application link |
| `ct`, `nt`, `x` | contact, notes, extra |
| `rk` | optional score used for sorting (number) |

Invalid entries are skipped by the app, so one bad row never breaks the list.
