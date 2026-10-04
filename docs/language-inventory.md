# Detected languages

Checked on 2026-10-05 against the existing Stats deployment. Successive queries
hid previously returned languages until the service returned an empty card.
This found 24 language labels within this service's dataset, not every repository
or programming skill.

| Current treatment | Languages | Count |
| --- | --- | --- |
| Visible on the main card | Python, C, MATLAB, Java, JavaScript, Verilog, C#, PHP, R, Rust, C++ | 11 |
| Hidden | HTML, CSS, Jupyter Notebook, PowerShell, Shell, Makefile, Tcl, Batchfile, Awk, TeX, ASP, M, Objective-C | 13 |

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

ASP, M, and Objective-C were subsequently hidden at the owner's request. C++ and
C# remain included. Percentages are recalculated over the retained languages.

## Verified public sources of the less familiar labels

| Label | Classified bytes | Public source |
| --- | ---: | --- |
| C++ | 7,312 | [Computer-Vision](https://github.com/diaoenmao/Computer-Vision), two MATLAB MEX `.cpp` files under `Final Project/Inverting_RANSAC/code/mex/`. |
| C# | 77,443 | [STF-Ivy-Dream-Works-MBTI-Test](https://github.com/diaoenmao/STF-Ivy-Dream-Works-MBTI-Test), the MVC .NET MBTI website's `.cs` files. |
| ASP | 12,008 | The same MBTI website's `.aspx` views. |
| M | 1,433 | Digital-Signal-Processing-Applications (1,125) and Computer-Vision (308). |
| Objective-C | 763 | Weighted-L2-Divergence (429) and Monophonic-Pitch-Tracking (334). |
| R | 24,318 | [MIREX-Audio-Melody-Extraction-Data-Analysis](https://github.com/diaoenmao/MIREX-Audio-Melody-Extraction-Data-Analysis), R analysis scripts. |

GitHub Linguist's `M` label means MUMPS; M, MATLAB, and Objective-C share the
`.m` extension. The M byte counts match the reviewed MATLAB files
[`genSignal.m`](https://github.com/diaoenmao/Digital-Signal-Processing-Applications/blob/master/Adaptive%20Equalization/genSignal.m),
[`gauss1d.m`](https://github.com/diaoenmao/Computer-Vision/blob/master/HW/assgn6/gauss1d.m), and
[`gauss2d.m`](https://github.com/diaoenmao/Computer-Vision/blob/master/HW/assgn6/gauss2d.m).
Weighted-L2-Divergence's Objective-C bytes also match the MATLAB file
[`mergeunpacked.m`](https://github.com/diaoenmao/Weighted-L2-Divergence/blob/master/src/mergeunpacked.m).
This is strong evidence of classification inconsistencies in small `.m` files.
Monophonic-Pitch-Tracking's aggregate Objective-C count was confirmed, but its
complete per-file allocation was not established. These labels do not establish
that the owner wrote MUMPS or Objective-C programs.
