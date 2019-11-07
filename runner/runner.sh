#!/bin/fish

# OUT_DIR=driazati.github.io/torchscript
set OUT_DIR driazati.github.io/torchscript

# Cleanup
conda activate benchmark
conda info
# yes | pip uninstall numpy
# yes | pip uninstall torchvision
# yes | pip uninstall torch
# yes | pip uninstall torch

python -c 'import torch'
if [ $? -eq 0 ]
# if [ $status -eq 0 ]
    echo "PyTorch was not uninstalled correctly"
    exit 1
end

# Fresh nightly install
pip install --pre torch torchvision -f https://download.pytorch.org/whl/nightly/cu92/torch_nightly.html

# Run tests
python test.py $OUT_DIR

# Move results to website folder
cd $OUT_DIR

git add .
git c -m"Update benchmarks"
git push
