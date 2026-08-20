# Selected public code samples

This directory contains **real, non-core UI code derived from the production FaceTrack Analytics application** so reviewers can inspect engineering style without exposing the production identity-resolution implementation.

Included:

- native Qt line/count chart rendering,
- antialiased custom media control rendering,
- responsive scroll-area geometry management.

Intentionally excluded:

- TrackletGraph identity-resolution implementation,
- calibrated tracking/ReID thresholds,
- model configuration and identity decision rules,
- private diagnostics and evaluation tooling,
- packaging secrets or local machine paths.

The public samples are not a runnable copy of the full application.
