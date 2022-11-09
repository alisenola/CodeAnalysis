#!/bin/sh

./tailAnalysis.py  --input ../../output_datasets/01_loc_output/ba/diffs-100-ba.csv            \
                    --output ../../output_datasets/05_tail_output/tail-analysis-ba.csv       \
                    --outstats ../../output_datasets/05_tail_output/tail-report-ba.csv       \
                    --deployments ../../auxiliary_datasets/deployments.csv             \
                    --thirdparty  ../../auxiliary_datasets/thirdparty-packages.csv              \
                    --ybase 2005  --ylast 2013
