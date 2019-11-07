#!/bin/bash

# Usage:
#   ./builder.sh <git hash of commit>

# Checkout the relevant hash without cloning the whole repo
mkdir -p pytorch
cd pytorch
git init
git clean -xfd
git remote add origin https://github.com/pytorch/pytorch
git fetch origin $1
git reset --hard FETCH_HEAD

# Parallel submodule update
git submodule status | awk '{print $2}' | xargs -t -P 20 -n1 git submodule update --init --recursive
git submodule update --init --recursive

pip install -r requirements.txt

# Run the build
REL_WITH_DEB_INFO=1 \
USE_DISTRIBUTED=0 \
USE_MKLDNN=0 \
USE_CUDA=0 \
BUILD_TEST=0 \
USE_FBGEMM=0 \
USE_NNPACK=0 \
USE_QNNPACK=0 \
CC=gcc \
CXX=g++ \
python setup.py develop
