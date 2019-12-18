#!/bin/bash

# This example will run benchmarks for a series of commits in the past

# Get every 60th commit (as hash, date), then only test the most recent 50
# git log --format='"%H", "%aD"' | awk 'NR == 1 || NR % 60 == 0' | head -n 50

# Get those same commits in a runnable format
# git log --format='run_with_commit %H' | awk 'NR == 1 || NR % 60 == 0' | head -n 50

# Kill chef for 16 hours
# sudo stop_chef_temporarily -t 16 -r "benchmarking"

export DESTDIR=driazati.github.io/torchscript/data
export BENCHMARKS='benchmarks/basic/run.py'
# export BENCHMARKS='benchmarks/resnet/run.py'

shopt -s expand_aliases  # make aliases work
alias run_with_commit='python ./runner/main.py --skip-conda-check --benchmarks $BENCHMARKS --out $DESTDIR --hash'

run_with_commit 4d22c3ba01c67a809f7272e38f8ffa6e9e4f384c                                                                                          run_with_commit 6e1e09fd10e58857c72b6da475c17709b0ef13ff                                                                                          run_with_commit 5b03ff0a09d43d721067e39da10aa23edc6997cd                                                                                          run_with_commit 82268bf300e2c794010ed381844767ebc5794f62                                                                                          run_with_commit a7406516d1b0c35973461833fa665d4296a75038                                                                                          run_with_commit d6ca93b3536f157577076480a3948c1d42ad984c
run_with_commit 9c02b88791de00eb8f5c06483629d20f125bb38b
run_with_commit efe1859ad94a26f04d5f9a57b890d02d984c3707
run_with_commit 1cc321deed43ed246f0de6b393184507d0307b45
run_with_commit 1aa80471b80050fa59e0a781b51fde11cd338128
run_with_commit ec52d911bd16ccba498b93685c646e489b8172a9
run_with_commit 4f94aed8a3d9263e232744b4ef8f343b58a81a4a
run_with_commit c543034531d70e4bb21be76a73acf59056921500
run_with_commit dfa9c9e227b6989d342c61f8e0229c53c50c09a0
run_with_commit c3b2c2e353179bd591b6bbafa303d9affca9babb
run_with_commit 93b5c9d723dd4003ebd7439074a9e9722d58d33c
run_with_commit edcf659e423d24a5a15939e55310d4f84d7c0270
run_with_commit 4515edfe1596db609b1a4c4601026ce2befc089b
run_with_commit a5aeb37493831871aa9b48c06f4336784b7347cf
run_with_commit 70f3f23e3ad8f07c08609f4a7a0b9ca751264fe1
run_with_commit 9034762a7dd428ae0fcdefe868fda87ea55e75cb
run_with_commit 2526f97464a24244d07b312931bdb1c54d8295c2
run_with_commit 9f890a921805a06058819a02f4a3ebc006514f3b
run_with_commit bfbb3e0579d239713b70a47034938b69b751a204
run_with_commit e280f93e31c2c662cf746d2bf2dc91035587b0b4
run_with_commit 6301d62e0b205c53a445ffb87ce7be1ac52d9cb9
run_with_commit d083b443b4046942499b50e2951d644a215e2213
run_with_commit cbe5ab11093355e5e8d0d09878d10de094cdf22f
run_with_commit 19df7e7e84c1328a0661c267835e1c922a6d90f7
run_with_commit d8df8aa8421125ecb554d7f13e649c1e09d6c701
run_with_commit 6cf189512c4aed7742a7b77aed480e1ed89a5e9b
run_with_commit 7b3881f68cb01dd0b98fb3ff5ef9618ac286a5ef
run_with_commit 493c90081008b193fb865b96671067f801c3cdcb
run_with_commit 46539eee0363e25ce5eb408c85cefd808cd6f878
run_with_commit f8db764f6c3383141fd0d8b27898116162d19d94
run_with_commit 492660768f193f9dde5c697b0f1811dce060f0c3
run_with_commit 08425d8c01204810c62be259dbc5647b3fbf9a0e
run_with_commit 7516156a354ab81f6037792a28198b81499d88ed
run_with_commit c79d116a7d3375a5108d64fab4f18cfbaa6ca711
run_with_commit 916eee182c9dc8d335501f6672842c6d29f0af58
run_with_commit 921079c5c26e0cb7a02e2fcd9ba144b10b0ea6da
run_with_commit 958d6272883f5b053545e8bdbff8af5bb0259dcc
run_with_commit 3051e36e059600a5daf9ce091af6ab6f2722bf14
run_with_commit bdc656da708e7cf2f354b68517a5dcc3eb081587
run_with_commit fc93d1ae6bd00b10be5d1a092b2c80f568634b96
run_with_commit d7a1152ee9948e21f337264460c5f6d12e4ed67f
run_with_commit 50cb48643df2e82d4000dc9dd4a9ba0ec2435c6a
run_with_commit 832c72a2d63034049d3303679b6a2f3c7d6e6956
run_with_commit d2919353778071f7f06ca3b0f592d272fb176c28
run_with_commit f88f9e13319ef278933f8f8523fc1601cd330b53
