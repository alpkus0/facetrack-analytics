# Third-party notices

FaceTrack Analytics combines original application code with third-party libraries and pretrained model assets. Source-code licenses and pretrained-model terms are not necessarily the same.

This file is a release/redistribution notice, not legal advice. The exact license or permission applicable to a distributed build should be retained with the project records and reviewed before changing the distribution scope.

## BoxMOT 22.0.0

- Used for the application’s BoT-SORT short-term tracking integration.
- Audited dependency version: `boxmot==22.0.0`.
- The upstream BoxMOT project is distributed under AGPL terms. For FaceTrack Analytics' current non-commercial portfolio use, the BoxMOT maintainer confirmed in writing that this use is acceptable.
- This permission is limited to the current non-commercial scope; any future commercial use would require a separate licensing discussion.
- FaceTrack Analytics uses a separate SCRFD face detector rather than detector models supplied by BoxMOT.

Official references:

- https://pypi.org/project/boxmot/
- https://github.com/mikel-brostrom/boxmot

## InsightFace code and pretrained models

- The application uses the InsightFace Python package for face-analysis infrastructure and the `buffalo_m` model pack for SCRFD detection and face-recognition embeddings.
- InsightFace distinguishes the license of its source code from the terms that apply to supplied pretrained models.
- Any distributed model files remain subject to the applicable model-use and redistribution permission for the release.

Official reference:

- https://github.com/deepinsight/insightface

## PySide6 / Qt for Python

Qt for Python is available under community and commercial licensing options. A frozen application distribution should include the notices and license files required by the edition and terms used for the release.

Official reference:

- https://doc.qt.io/qtforpython-6/

## ONNX Runtime

ONNX Runtime is distributed under the MIT License.

Official reference:

- https://github.com/microsoft/onnxruntime/blob/main/LICENSE

## OpenCV, NumPy, PyInstaller, NVIDIA runtime packages, and other dependencies

These components retain their own licenses and redistribution terms. The final Windows release package should preserve any notices or license files required by the exact dependency versions bundled into the frozen build.

## Public portfolio boundary

This public repository intentionally excludes:

- the production TrackletGraph identity-resolution implementation,
- calibrated identity/decision thresholds,
- private diagnostics and assisted ground-truth tooling,
- internal evaluation media,
- pretrained ONNX model files,
- packaged executables and runtime DLLs,
- build output and local-machine paths.

The repository is a portfolio-oriented, source-visible presentation of the project rather than a complete production source release.
