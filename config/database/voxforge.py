#!/usr/bin/env python

import bob.db.voxforge

# 0/ The database to use
name = 'VoxForge'
# put the full path to the database filelist
db = bob.db.voxforge.Database()
protocol = None

# directory where the wave files are stored
wav_input_dir = "PATH/TO/WAV"
wav_input_ext = ".wav"

