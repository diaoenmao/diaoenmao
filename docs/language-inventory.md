# Detected languages

Checked on 2026-10-05 against the existing Stats deployment. Successive queries
hid previously returned languages until the service returned an empty card.
This found 24 language labels within this service's dataset, not every repository
or programming skill.

| Current treatment | Languages | Count |
| --- | --- | --- |
| Visible on the main card | Python, C, MATLAB, Java, JavaScript, Verilog, C#, PHP, R, Rust, ASP, C++, M, Objective-C | 14 |
| Hidden | HTML, CSS, Jupyter Notebook, PowerShell, Shell, Makefile, Tcl, Batchfile, Awk, TeX | 10 |

The previous deployment displayed only ten languages even when `langs_count=20`
was requested. It used commit
`ff2e02ba6841a263b6dc26807c0ea350fafac03b`; its
[renderer clamps the count to 1–10](https://github.com/diaoenmao/github-readme-stats/blob/ff2e02ba6841a263b6dc26807c0ea350fafac03b/src/cards/top-languages-card.js#L167)
before slicing the sorted language list. A fresh direct request with
`langs_count=14` returned ten labels with `Age: 0` and `X-Vercel-Cache: MISS`.
This is a rendering limit, not a minimum-percentage threshold or an old cached
image.

On 2026-10-05 the fork was synchronized and Vercel production updated to
`54a7985aeefda00d5eadb55b80c17c7f976c37d2`. The unchanged README URL now returns
all fourteen retained labels (HTTP 200). The newer renderer supports up to twenty.

Percentages on the secondary queries describe a different selection.
`M` is a label returned by the service and has not been verified against its files.
