# Project notes for Claude

## Visualizing prediction results

When asked to visualize/inspect the output of a `boltz predict` run (a
`boltz_results_<name>/` folder), build an HTML report — 3D structure viewer
(color by pLDDT confidence band and by chain), a per-residue pLDDT chart, and
a PAE heatmap — sourced from that folder's `predictions/<name>/*.cif` and
`*.npz` files.

**Always save the finished report into that same experiment's results
folder**, as `boltz_results_<name>/report.html`, in addition to publishing it
as an Artifact. This keeps each experiment's visualization alongside its raw
outputs so it survives independently of the chat session. If a report already
exists there, overwrite it after checking what's already in the folder.
