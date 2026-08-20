# Changelog

All notable public-facing changes to FaceTrack Analytics are documented here.

The project uses semantic versioning for public releases.

## [1.0.0] - 2026-08-20

### Added

- Windows desktop interface for recorded-video and still-image face analysis.
- Video pipeline combining SCRFD face detection, BoT-SORT short-term tracking, selective Face ReID, and session-level unique-person estimation.
- Photo-specific single-frame analysis with confidence statistics and histogram visualization.
- Balanced, Accuracy, and Fast user presets.
- ONNX Runtime CUDA acceleration with automatic CPU fallback.
- Runtime dashboard for current faces, estimated unique people, confidence, FPS, detection time, tracking time, and ReID time.
- English and Türkçe interface localization.
- CSV export for video timelines and photo detections.
- Localized HTML analysis reports.
- User-facing `UNIQUE_PERSON_SUMMARY.jpg` output for naturally completed video sessions.
- Fullscreen media viewer and keyboard shortcuts.
- Windows ONEDIR packaging with bundled runtime dependencies for portable execution.

### Validation

- Verified CUDA execution on an NVIDIA GeForce RTX 3050 Ti Laptop GPU test system.
- Verified CPU fallback on a clean Windows 10 virtual machine without Python or CUDA Toolkit installed.
- Completed labeled development, holdout, and stress validation for video counting and a fresh holdout for photo counting.

### Release note

This public repository is a portfolio-oriented surface rather than the full production source tree. The production identity-resolution implementation, calibrated decision rules, private diagnostics, and evaluation tooling are intentionally not included.
