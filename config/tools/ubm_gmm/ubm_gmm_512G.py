#!/usr/bin/env python

import spear
import bob.learn.misc

tool = spear.tools.UBMGMMTool


# 2/ GMM Training
n_gaussians = 512
iterk = 10
iterg_train = 25
update_weights = True
update_means = True
update_variances = True
norm_KMeans = True


# 3/ GMM Enrolment and scoring
iterg_enrol = 1
convergence_threshold = 0.0001
variance_threshold = 0.0001
relevance_factor = 4
responsibilities_threshold = 0

# Scoring
scoring_function = bob.learn.misc.linear_scoring

