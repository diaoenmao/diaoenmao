# Profile Views on Vercel

The selected project is [Komarev](https://github.com/antonkomarev/github-profile-views-counter).
Its fork is [diaoenmao/github-profile-views-counter](https://github.com/diaoenmao/github-profile-views-counter).

The user chose the free approach without creating a new database. The fork's
`vercel/` directory provides a Vercel relay; Komarev continues to store and
serve the existing count. This is not a self-hosted PHP counter. It requires no
Redis credentials, environment variables, or migration offset.

The verified migration baseline was **6,651** on 2026-10-05. No estimate for losses from
an older migration is added. The upstream username remains `diaoenmao`, so the
existing history continues. Do not add `base=6651`: that would count it twice.

Import the fork into Vercel, select **Other** and use the repository root as Root Directory.
The public badge endpoint is `/api/views`, with `/ghpvc/` as an alias.
The verified production endpoint is
<https://github-profile-views-counter-roan.vercel.app/api/views>.
It returned HTTP 200 and the original total 6,651 after deployment; the README
now uses it. The project is
<https://vercel.com/diaoenmaos-projects/github-profile-views-counter>.
After a GitHub Camo request the total increased to 6,652. Rebuilding the same
relay on 2026-10-05 preserved 6,652 (HTTP 200); no offset or reset was applied.

GitHub Camo's user agent is forwarded to Komarev for image requests. Ordinary
local previews use a read-only user agent according to the current upstream
implementation. HEAD uses the upstream HEAD method without a Camo user agent.
The relay disables caching and returns an unavailable SVG (`--`, HTTP 503) if
Komarev fails. It never invents a total or writes/reset counts.

The relay still depends on Komarev's availability. A future fully self-hosted
version needs durable storage: Vercel's function memory and local files are
not persistent. That option has not been deployed.

Local profile preview: `python scripts/preview-profile.py`, then open
<http://127.0.0.1:8766/>. Refresh after editing README.md.
