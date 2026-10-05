#!/usr/bin/env bash
# Fetch the external baselines at the commits used in the paper.
#   mccepy  https://github.com/NorskRegnesentral/mccepy   @63e4fa3 (+ pandas-2 patch)
#   CARE    https://github.com/peymanrasouli/CARE          @811ff09 (GPL-3.0; not redistributed here)
# NICE is installed from PyPI (NICEx==0.2.3, in requirements.txt).
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p external
if [ ! -d external/mccepy ]; then
  git clone https://github.com/NorskRegnesentral/mccepy external/mccepy
  git -C external/mccepy checkout 63e4fa38b3fe2506710104b96d2a2f34c665e70e
  git -C external/mccepy apply "$PWD/patches/mccepy-pandas2.patch"
fi
if [ ! -d external/CARE ]; then
  git clone https://github.com/peymanrasouli/CARE external/CARE
  git -C external/CARE checkout 811ff096b1f65168307813a0e28a9dff64823ffd
fi
echo "External baselines ready in external/ (external_baselines.py finds them there)."
