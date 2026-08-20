# Validation methodology

FaceTrack Analytics was validated against manually verified ground-truth counts. The target metric is the number of distinct visible people represented in each test item, not identity-by-name recognition.

The public repository does not include private evaluation media or assisted ground-truth tooling.

## Video development set

Ten labeled development videos were evaluated across all three presets, producing 30 runs.

| Metric | Result |
| --- | ---: |
| Runs | 30 |
| Exact count | 27 / 30 |
| Within ±1 | 30 / 30 |
| Mean absolute error | 0.100 |
| Worst absolute error | 1 |

Preset exact-count results on the development set:

| Preset | Exact |
| --- | ---: |
| Balanced | 9 / 10 |
| Accuracy | 10 / 10 |
| Fast | 8 / 10 |

## Video holdout/regression set

Six additional labeled videos were evaluated across all three presets, producing 18 runs.

| Metric | Result |
| --- | ---: |
| Runs | 18 |
| Exact count | 15 / 18 |
| Within ±1 | 18 / 18 |
| Mean absolute error | 0.167 |
| Worst absolute error | 1 |

Each preset produced 5 / 6 exact counts in this set.

## Video stress validation

Stress variants were used to probe degradation under controlled transformations rather than to tune the production thresholds.

| Metric | Result |
| --- | ---: |
| Runs | 36 |
| Exact count | 28 / 36 |
| Within ±1 | 34 / 36 |
| Mean absolute error | 0.278 |
| Worst absolute error | 2 |

The stress suite included cases where information loss or temporal degradation produced larger errors. Those cases are retained as documented limitations rather than hidden by retuning to the stress set.

## Photo validation

Photo-mode confidence admission was calibrated on a labeled development set and then frozen before a fresh holdout evaluation.

### Fresh photo holdout

Six photos were evaluated across all three presets, producing 18 runs.

| Metric | Result |
| --- | ---: |
| Runs | 18 |
| Exact count | 14 / 18 |
| Within ±1 | 18 / 18 |
| Mean absolute error | 0.222 |
| Worst absolute error | 1 |

Preset exact-count results:

| Preset | Exact |
| --- | ---: |
| Balanced | 5 / 6 |
| Accuracy | 5 / 6 |
| Fast | 4 / 6 |

## Interpretation

These figures are **project-specific validation results**, not a universal accuracy claim. Performance can vary with camera quality, motion blur, face size, occlusion, pose, illumination, scene density, compression, and hardware/runtime configuration.

Video and photo metrics should not be compared as if the modes were identical: video mode uses temporal tracking and identity evidence, while photo mode is a single-frame detector/counting workflow.
