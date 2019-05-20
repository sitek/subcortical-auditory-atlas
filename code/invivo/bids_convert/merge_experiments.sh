#!/bin/bash
# move Experiment 2 to the main experiment
# SES1 and SES2 become SES04 and SES05, respectively

# first, rename subjects in Exp 2 based on README
# example:
mv sub-S01 f09
mv f09 sub-S09

# then, within each subject's directory, rename files
# example:
rename sub-S01_ses-SES1 sub-S09_ses-SES04 */*
rename sub-S01_ses-SES1 sub-S09_ses-SES04 */*/*
rename sub-S01_ses-SES2 sub-S09_ses-SES05 */*
rename sub-S01_ses-SES2 sub-S09_ses-SES05 */*/*

