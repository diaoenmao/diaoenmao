# Profile service checks and changes

Checked on 2026-10-05 (Asia/Shanghai) using a direct HTTP client and the GitHub
profile rendered in the browser. These checks do not establish global uptime or
performance in every region.

| Original endpoint | Observation |
| --- | --- |
| `github.com/diaoenmao` | Unauthenticated HTTP 200; approximately 0.82 s in the direct check. |
| `komarev.com/ghpvc/` | Direct connection timed out; the badge initially failed through GitHub's proxy, then recovered and showed 6,651. Availability was intermittent. |
| `github-readme-stats-five-alpha-58.vercel.app/api` | Valid stats SVG; repeated direct check approximately 0.47 s. |
| `github-readme-streak-stats-rouge-delta.vercel.app/` | Valid streak SVG; repeated direct check approximately 0.82 s. |
| `github-profile-trophy-dusky-psi.vercel.app/` | Valid trophy SVG; repeated direct check approximately 0.91 s. |

The account owns forks of all three stats projects. Response headers identified
Vercel's `iad1` function region and `sin1` ingress. They showed cache misses in
the checks. This can add network distance and generation time, but it does not
prove a cold-start problem. Keep any database near the selected function region.

The final Stats, Languages, and Streak URLs also returned valid SVGs through
GitHub Camo (HTTP 200), with direct proxy checks around 0.54 s, 2.28 s, and
0.65 s respectively. The local preview initially showed broken images, then
the proxy checks succeeded. A successful origin request alone does not guarantee
that every first browser load succeeds.

## README changes

- Store all 54 tool icons locally in `assets/tools/`, preserving their order and
  official links. Independent icons wrap to the available README width. This
  replaces the earlier fixed grid in the combined `assets/tools.svg`.
- Add **Most Used Languages** using the existing Stats deployment. The reference
  [damingerdai README](https://github.com/damingerdai/damingerdai) uses the same
  `/api/top-langs` endpoint with `layout=compact`.
- Request up to 20 remaining languages for review, with compact layout, the existing default theme, and an 880 px
  SVG rendered across the README width. The fork fits the compact legend columns
  to the generation width and label lengths, instead of always using two columns.
  Stats and language cards request one-day caching. Actual caching
  still depends on the fork, Vercel, and GitHub's Camo image proxy.
- Disable card animations and preserve the original trophy layout parameters.
  Vercel remains the source of all four dynamic stats cards.
- Keep the cards' original default palette: white backgrounds, blue Stats and
  Languages accents, and orange-gold Streak accents. Preserve the language
  identification colors and trophy layout.
- Connect the existing Komarev count through a free Vercel relay in
  [the selected project's fork](https://github.com/diaoenmao/github-profile-views-counter).
  See [deployment and history preservation](profile-views.md). This relay creates
  no new database; the original count remains with Komarev.

Language percentages are based on code bytes in the owner's non-forked
repositories by default. They do not measure time spent coding or skill.
Notebook files, generated HTML, and large vendored files can dominate the result.
The card excludes HTML, CSS, Jupyter Notebook, auxiliary scripting languages
(Shell, PowerShell, Batchfile, Makefile, Tcl, and Awk), and TeX using
`hide=html,css,jupyter%20notebook,shell,powershell,batchfile,makefile,tcl,awk,tex`. Python and JavaScript
remain included as primary project languages. The displayed percentages are recalculated
over the remaining languages. If needed, adjust `size_weight` and
`count_weight`, exclude a specific repository, or configure GitHub Linguist in
the affected source repository. Private coverage depends on the deployment's
token and configuration; the query string alone cannot grant access.

The current fork source requests at most 100 owned non-fork repositories, and the
ten largest languages in each repository. The old deployment clamped the card
count to ten despite `langs_count=20`. After updating the production Stats
deployment to `54a7985aeefda00d5eadb55b80c17c7f976c37d2`, the unchanged README URL
returns all fourteen retained labels: Python, C, MATLAB, Java, JavaScript,
Verilog, C#, PHP, R, Rust, ASP, C++, M, and Objective-C. See
[the verified limit and update](language-inventory.md). These checks cannot
establish every language the owner has used or knows. ASP, M, and Objective-C
were subsequently hidden at the owner's request, leaving eleven visible labels;
C++ and C# remain included.

## Local preview

Run `python scripts/preview-profile.py` from this repository, then open
<http://127.0.0.1:8766/>. The script renders the latest README on every refresh;
after editing, refresh the browser to see the changes. It needs Python and the
`markdown` package (already installed on the current computer). Install that
package with `python -m pip install Markdown` on a different machine if needed.

The preview uses a GitHub-like layout and serves only the rendered README and
local assets. Stats images continue to load from their live Vercel endpoints;
this does not run the Vercel view-counter relay locally.

## Future service upgrades

The original [GitHub Readme Stats](https://github.com/anuraghazra/github-readme-stats)
now marks itself unmaintained and recommends
[GitHub Stats Extended](https://github.com/stats-organization/github-stats-extended).
For a future Vercel provider upgrade, migrate the existing Stats fork to that
successor and retain the current token access and configuration. That upgrade
is separate from this README change; the existing deployment is still in use.

[Metrics](https://github.com/lowlighter/metrics) and
[Profile Summary Cards](https://github.com/vn7n24fzkq/github-profile-summary-cards)
are alternatives for richer dashboards. GitHub Actions can generate static
cards if the desired hosting approach changes later.

## Free Vercel profile-view relay

The deployed endpoint is https://github-profile-views-counter-roan.vercel.app/api/views.
It returned a valid SVG (HTTP 200) in about 1.26 s in a direct check, retaining
the existing Komarev total of 6,651. A GitHub Camo check also returned HTTP 200
in about 1.56 s. The local browser verified all six profile images loaded.
No new database was created; Komarev retains the counter storage.
These timings are individual checks, not a global performance guarantee.

## Vercel updates on 2026-10-05

Only the four Profile projects were updated; the personal website was excluded.

| Project | Production source | Verification |
| --- | --- | --- |
| Stats and Languages | `54a7985aeefda00d5eadb55b80c17c7f976c37d2` | Valid Stats SVG and all 14 retained language labels, HTTP 200. |
| Trophy | `3616d79386790f5844321502b1ac9a5b56278636` | Valid 880 × 220 SVG with the original eight-column layout, HTTP 200. |
| Streak | `018477b504835412426ae67273a2d4709d7c0a4b` on `vercel` | Valid 495 × 195 SVG with current streak 10 and longest streak 89, HTTP 200. |
| Views | `af00d4c3911e6840477cca3ba2653c5cb272ab9d`, rebuilt | Valid SVG retaining 6,652 views, HTTP 200. |

Stats, Trophy, and Streak were synchronized with their upstream repositories.
Trophy required one compatibility fix: its Vercel Deno adapter does not resolve
the `deno.json` import map, so `api/index.ts` now imports the pinned dotenv module
using its direct URL. Streak production branch tracking was corrected from
`main` to `vercel`, and the new version rebuilt in the production environment.

The newer Stats code also changes its ranking calculation. The verified card
shows A- rather than the older deployment's A++; the README does not override it.
The four card URLs include `v=20261005` to avoid reusing old browser and GitHub
Camo images after this service upgrade. This does not change their layouts.

## Language layout follow-up

Stats fork commit `cbf4d77e9125f81162f76d48a7da3f8252a67c70` removes the hardcoded
two-column compact legend. The renderer measures label widths, fits as many
columns as the supplied card width permits, and adjusts the height for the rows.
The [production deployment](https://vercel.com/diaoenmaos-projects/github-readme-stats/DnmpRVar4BgvhPrUSFx8eZTHzSDo)
is Ready. A direct request returned HTTP 200 and an 880 × 165 SVG containing all
eleven retained languages, with five legend items on each complete row.
The language image uses `width="100%"` in the README. As a server-generated SVG,
its columns are determined by `card_width`; changing the browser width scales the
finished image rather than regenerating its layout. The separate tool icons do
wrap with the browser width. The existing 34 renderer tests and one added wide
card regression test passed, together with formatting and lint checks.

## What the Stats grade means

The current [`calculateRank.js`](https://github.com/diaoenmao/github-readme-stats/blob/54a7985aeefda00d5eadb55b80c17c7f976c37d2/src/calculateRank.js)
uses six normalized metrics. Commits, PRs, issues, and reviews use
`E(n, m) = 1 - 2 ** (-n / m)`. Stars and followers use `L(n, m) = n / (n + m)`.
The total score is `100 * sum(weight * normalized_metric) / 12`.

| Metric | Value used in this check | Normalization baseline | Weight | Score contribution |
| --- | ---: | ---: | ---: | ---: |
| All commits | 6,090 | 1,000 | 2 | 16.42 |
| PRs | 76 | 50 | 3 | 16.28 |
| Issues | 9 | 25 | 1 | 1.84 |
| Reviews in the past year | 0 | 2 | 1 | 0.00 |
| Stars | 531 | 50 | 4 | 30.46 |
| Followers | 93 | 10 | 1 | 7.52 |
| Total | | | 12 | 72.53 |

With `include_all_commits=true`, the commit baseline is 1,000; otherwise it is
250. Repository count and the card's "Contributed to" value do not enter the
new grade. The algorithm's modeled percentile is `100 - score`, or 27.47 here.
It does not fetch a real-time global distribution of GitHub accounts.

The new thresholds are S at 99+, A+ at 87.5+, A at 75+, A- at 62.5+, B+ at
50+, B at 37.5+, B- at 25+, C+ at 12.5+, and C below 12.5. There is no A++ grade.
The former deployment used a different linear weighted count plus normal-CDF
formula, so its A++ is not directly comparable to the new A-. The source change
does not mean contributions were lost. Keeping the other values constant, two
counted reviews would produce a score of 76.70 and grade A. This calculation is
illustrative; future cards also reflect changing counts and cached responses.
