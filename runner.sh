#!/bin/fish

OUT_DIR=driazati.github.io/torchscript
# set OUT_DIR driazati.github.io/torchscript

# Cleanup
# conda activate benchmark
# pip uninstall numpy
# pip uninstall torchvision
# pip uninstall torch
# pip uninstall torch

# # Fresh nightly install
# pip install --pre torch torchvision -f https://download.pytorch.org/whl/nightly/cu92/torch_nightly.html

# Run tests
python test.py

# Move results to website folder
cp *.csv $OUT_DIR

cd $OUT_DIR

git add .
git c -m"Update benchmarks"
git push

