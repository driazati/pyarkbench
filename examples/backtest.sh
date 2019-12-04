#!/bin/bash

# Get every 60th commit (as hash, date), then only test the most recent 50
# git log --format='"%H", "%aD"' | awk 'NR == 1 || NR % 60 == 0' | head -n 50

# These are some commits to perf test
# example: python runn2er.py --out driazati.github.io/torchscript --hash a6fb6e1fb39f1f4a509dec04e4719ff9e2d04c83
python ./runner/main.py --out driazati.github.io/torchscript --skip-checkout

# python ./runner/main.py --out driazati.github.io/torchscript --hash ea3697db69e6ccb8235c3d20384d9a5b12463813
# python ./runner/main.py --out driazati.github.io/torchscript --hash 53785771a7aa557f6b397762f7e3b3b9f263f4fc
# python ./runner/main.py --out driazati.github.io/torchscript --hash 25f4ba7c1b72e2ce49322e841883de172264b768
# python ./runner/main.py --out driazati.github.io/torchscript --hash 29887f813a8224ec415facd8e77c16bfbd10e231
# python ./runner/main.py --out driazati.github.io/torchscript --hash c2b7b2cbf8d4a7e0c82496147b4ae68d4c6a0216
# python ./runner/main.py --out driazati.github.io/torchscript --hash 20b73e18053a972c84b6766bc0d13c308d328cd7
# python ./runner/main.py --out driazati.github.io/torchscript --hash 189b24ebe96b9ab9a45c98a699b0fbf965ca1b90
# python ./runner/main.py --out driazati.github.io/torchscript --hash 92a512b5832e91f64d9bca98b8a93897460b3cb8
# python ./runner/main.py --out driazati.github.io/torchscript --hash ed788ec7804cac24db42069f41a7109c65cc57f1
# python ./runner/main.py --out driazati.github.io/torchscript --hash f111f1b1a77702d632f2d5c9cea750064bc1d82a
# python ./runner/main.py --out driazati.github.io/torchscript --hash bb119d957e331a1dbca91fbdf00f298088218e5b
# python ./runner/main.py --out driazati.github.io/torchscript --hash 63675b1969d5437384851e0e543b2fe9785334ce
# python ./runner/main.py --out driazati.github.io/torchscript --hash a5d356cb39d521c25786c9ef14981f02ca3459be
# python ./runner/main.py --out driazati.github.io/torchscript --hash 21d11e0b644bcfff747c944849c9418fe42c32d8
# python ./runner/main.py --out driazati.github.io/torchscript --hash 1e904049cac8a5df5af8e2067711c5addefc35d9
# python ./runner/main.py --out driazati.github.io/torchscript --hash a844809a2c01d130be14701be51d04684dc595c1
# python ./runner/main.py --out driazati.github.io/torchscript --hash cbc234bcebe3a155a1cbe7e02282d64c52ffd0d4
# python ./runner/main.py --out driazati.github.io/torchscript --hash 4230132baf259bf10336b27755a1e0d6ae6927e7
# python ./runner/main.py --out driazati.github.io/torchscript --hash da6b8a905a2f37b5d927c380f2495628f4f091d9
# python ./runner/main.py --out driazati.github.io/torchscript --hash 9705d60a2f7dabe0adcc13598b0e5268678f9d00
# python ./runner/main.py --out driazati.github.io/torchscript --hash c813503f057db361eb44740e7a6932ddf3fb450d
# python ./runner/main.py --out driazati.github.io/torchscript --hash cbb4c87d434350d380ba8eb8ff2f0c60e17de58e
# python ./runner/main.py --out driazati.github.io/torchscript --hash ef8bcfe2c7a4842e54520a6d9c783e6be2443e56
# python ./runner/main.py --out driazati.github.io/torchscript --hash 341262754f5e7247e136504fcd06bf6fcab0dcc9
# python ./runner/main.py --out driazati.github.io/torchscript --hash f3df6b8ede4057453486964100e6cba284d9fa36
# python ./runner/main.py --out driazati.github.io/torchscript --hash 31a6ff46c1c6efaf9db24ce2c4b2cd89771380e7
# python ./runner/main.py --out driazati.github.io/torchscript --hash 646e214706fd940ae36c51cdc8d66789962203ff
# python ./runner/main.py --out driazati.github.io/torchscript --hash fc249c79245af10eeb564ab0f1d42b025a8e07f4
# python ./runner/main.py --out driazati.github.io/torchscript --hash 1d4d6b6f0fe590f44b469d1ee49a967b28ccf81a
# python ./runner/main.py --out driazati.github.io/torchscript --hash 3a18e2e7686d01e4222b5f3fafdbe0b6c9154797
# python ./runner/main.py --out driazati.github.io/torchscript --hash 8d5c2aa71c6c2bef6304c80ffb1a20ac398e4823
# python ./runner/main.py --out driazati.github.io/torchscript --hash 03007b3dda7c4b5bc339106bbf0dd9f7a409c7c9
# python ./runner/main.py --out driazati.github.io/torchscript --hash 3f72bcfcaacadfbbfb40e1cc32fc15fdec26bca5
# python ./runner/main.py --out driazati.github.io/torchscript --hash 567a1981a701f3682ab3c71b68ec45e965c8f279
# python ./runner/main.py --out driazati.github.io/torchscript --hash 67035871560b8b943488a9ff5b6aa677a0540364
# python ./runner/main.py --out driazati.github.io/torchscript --hash fb28014af0c3cc095917087da25dbb9147486500
# python ./runner/main.py --out driazati.github.io/torchscript --hash 2ce8c83f677fbd144c45d0b500a62c392b01c8fe
# python ./runner/main.py --out driazati.github.io/torchscript --hash 8c46061e2c178d2771ef5a1a54e6bac842c6ae62
# python ./runner/main.py --out driazati.github.io/torchscript --hash d4757afbe5f38cf16004cf2e7a14aa0ba70d9d34
# python ./runner/main.py --out driazati.github.io/torchscript --hash a14e88454690645d57e056f45829331df7eef611
# python ./runner/main.py --out driazati.github.io/torchscript --hash 75cac0fe6968dce6ff7068e58bc5ed51b7a09183
# python ./runner/main.py --out driazati.github.io/torchscript --hash 2e1a5cb80e7084d17ffe19f0f4c75d9232b14308
# python ./runner/main.py --out driazati.github.io/torchscript --hash c36b77fcdad3d54227cf0fd51693eb57035002c0
# python ./runner/main.py --out driazati.github.io/torchscript --hash 3805be62c1bb10b8bf4e645aac30d89efd8f79ab
# python ./runner/main.py --out driazati.github.io/torchscript --hash eb2c5930b2a5a9117928e327ccbfa45f310e1ec1
# python ./runner/main.py --out driazati.github.io/torchscript --hash c142dbf8763a9e200f210c0ee58bdae86a8ac50e
# python ./runner/main.py --out driazati.github.io/torchscript --hash add57fd2677d0dbc1ad589c5537cee64bbce4215
# python ./runner/main.py --out driazati.github.io/torchscript --hash 0eb55f9dddd055fbf63bba5f0f4536b2ed94bade
# python ./runner/main.py --out driazati.github.io/torchscript --hash 5aa0f89d65d351ce71ba21336b3cc2e82a8b6135
# python ./runner/main.py --out driazati.github.io/torchscript --hash b59fa077b3a088f3e6934c72bf5bb3d6f0a23f64
