# System requirements

## Supported platform

- Windows 10 64-bit
- Windows 11 64-bit

The v1.0.0 release target is Windows x64.

## GPU acceleration

FaceTrack Analytics uses ONNX Runtime execution providers.

- **NVIDIA CUDA-capable GPU available:** the application can use CUDA acceleration.
- **No compatible CUDA GPU:** the application automatically falls back to CPU execution and displays a warning that analysis may be slower.
- **AMD/Intel GPU in v1.0.0:** no dedicated AMD/Intel GPU execution backend is included; analysis uses CPU fallback.

A current compatible NVIDIA driver is required for CUDA acceleration. The portable build is designed to bundle the required CUDA/cuDNN runtime libraries, so users should not need to install CUDA Toolkit or cuDNN separately.

## Clean-machine validation

The release candidate was tested on a clean Windows 10 virtual machine configured without:

- Python,
- project virtual environment,
- CUDA Toolkit,
- cuDNN development installation.

The application launched successfully, entered CPU mode, completed photo/video analysis, generated outputs, supported language switching, and reopened successfully.

CUDA execution was separately validated on a physical NVIDIA GeForce RTX 3050 Ti Laptop GPU system.

## Portable package rule

The v1.0.0 build uses PyInstaller **ONEDIR** packaging. Keep the complete extracted folder together:

```text
FaceTrackAnalytics/
├── FaceTrackAnalytics.exe
├── _internal/
└── outputs/
```

Do not copy `FaceTrackAnalytics.exe` by itself and expect the application to retain its packaged dependencies.

## Performance expectations

CPU fallback may be substantially slower than CUDA. Runtime FPS also depends on source resolution, scene content, preset, and the number/quality of visible faces. For that reason, the project does not publish a single universal FPS claim.
