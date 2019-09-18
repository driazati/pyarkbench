#!/bin/bash

# Checkout the relevant hash without cloning the whole repo
# mkdir -p pytorch
cd pytorch
# git init
# git remote add origin https://github.com/pytorch/pytorch
# git fetch origin $1
# git reset --hard FETCH_HEAD

# # Parallel submodule update
# git submodule status | awk '{print $2}' | xargs -t -P 20 -n1 git submodule update --init --recursive

pip install -r requirements.txt

REL_WITH_DEB_INFO=1 USE_DISTRIBUTED=0 USE_MKLDNN=0 USE_CUDA=0 BUILD_TEST=0 USE_FBGEMM=0 USE_NNPACK=0 USE_QNNPACK=0 python setup.py develop
