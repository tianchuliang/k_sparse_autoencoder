#!/usr/bin/env sh

/usr/local/caffe/build/tools/caffe train -solver /Users/tianchuliang/Documents/GT_Acad/CSE6240Spring16/tliang37-project2/code/Autoencoder/solver_plain.prototxt  2>&1 | tee  /Users/tianchuliang/Documents/GT_Acad/CSE6240Spring16/tliang37-project2/code/Autoencoder/autoencoder_plain_training.log

