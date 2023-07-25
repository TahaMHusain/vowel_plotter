#!/bin/bash --login
# The --login ensures the bash configuration is loaded,
# enabling Conda.

# Enable strict mode.
set -euo pipefail
# ... Run whatever commands ...

# Temporarily disable strict mode and activate conda:
set +euo pipefail
conda activate vowel_plotter

# Re-enable strict mode:
set -euo pipefail

# exec the final command
exec pip install praat-parselmouth
exec python vowel_plotter.py data/sample_vowels.wav