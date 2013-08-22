Speaker Recognition Toolkit
===========================

This is the speaker recognition toolkit, designed to run speaker verification/recognition
experiments . It's originally based on facereclib tool:
https://github.com/bioidiap/facereclib

`xbob.speaker_recognition`_ is designed in a way that it should be easily possible to execute experiments combining different mixtures of:

* Speaker Recognition databases and their according protocols
* Voice activity detection
* Feature extraction
* Recognition/Verification tools

In any case, results of these experiments will directly be comparable when the same database is employed.

`xbob.speaker_recognition`_ is adapted to run speaker verification/recognition experiments with the SGE grid infrastructure at Idiap.


If you use this package and/or its results, please cite the following
publications:

1. The original paper presented at the NIST SRE 2012 workshop::

     @inproceedings{Khoury_NISTSRE_2012,
       author = {Khoury, Elie and El Shafey, Laurent and Marcel, S{\'{e}}bastien},
       month = {dec},
       title = {The Idiap Speaker Recognition Evaluation System at NIST SRE 2012},
       booktitle = {NIST Speaker Recognition Conference},
       year = {2012},
       location = {Orlando, USA},
       organization = {NIST},
       pdf = {http://publications.idiap.ch/downloads/papers/2012/Khoury_NISTSRE_2012.pdf}
    }


2. Bob as the core framework used to run the experiments::

    @inproceedings{Anjos_ACMMM_2012,
      author = {A. Anjos and L. El Shafey and R. Wallace and M. G\"unther and C. McCool and S. Marcel},
      title = {Bob: a free signal processing and machine learning toolbox for researchers},
      year = {2012},
      month = oct,
      booktitle = {20th ACM Conference on Multimedia Systems (ACMMM), Nara, Japan},
      publisher = {ACM Press},
      url = {http://publications.idiap.ch/downloads/papers/2012/Anjos_Bob_ACMMM12.pdf},
    }


Installation
------------

Just download this package and uncompressed it locally::

  $ wget http://pypi.python.org/packages/source/x/xbob.nist_sre_2012/xbob.speaker_recognition.zip
  $ unzip xbob.speaker_recognition.zip
  $ cd xbob.speaker_recognition

`xbob.speaker_recognition`_ is based on the `BuildOut`_ python linking system. You only need to use buildout to bootstrap and have a working environment ready for
experiments::

  $ python bootstrap
  $ ./bin/buildout

This also requires that bob (>= 1.2.0) is installed.


Running experiments
-------------------

These two commands will automatically download all desired packages (`gridtk`_, `pysox`_ and `xbob.db.verification.filelist`_ ) from GitHub or `pypi`_ and generate some scripts in the bin directory, including the following scripts::
  
   $ bin/spkverif_isv.py
   $ bin/spkverif_ivector.py
   $ bin/para_ubm_spkverif_isv.py
   $ bin/para_ubm_spkverif_ivector.py

  
These scripts can be used to employ different 
To use them you have to specify at least four command line parameters (see also the ``--help`` option):

* ``--database``: The configuration file for the database
* ``--preprocessing``: The configuration file for Voice Activity Detection
* ``--feature-extraction``: The configuration file for feature extraction
* ``--tool-chain``: The configuration file for the face verification tool chain

If you are not at Idiap, please precise the TEMP and USER directories:

* ``--temp-directory``: This typically contains the features, the UBM model, the client models, etc.
* ``--user-directory``: This will contain the output scores (in text format)

If you want to run the experiments in the GRID at Idiap or any equivalent SGE, you can simply specify:

* ``--grid``: The configuration file for the grid setup.

If no grid configuration file is specified, the experiment is run sequentially on the local machine.
For several databases, feature types, recognition algorithms, and grid requirements the `xbob.speaker_recognition`_ provides these configuration files.
They are located in the *config/...* directories.
It is also safe to design one experiment and re-use one configuration file for all options as long as the configuration file includes all desired information:

* The database: ``name, db, protocol; wav_input_dir, wav_input_ext``;
* The preprocessing: ``preprocessor = spkrec.preprocessing.<PREPROCESSOR>``;
* The feature extraction: ``extractor = spkrec.feature_extraction.<EXTRACTOR>``;
* The tool: ``tool = spkrec.tools.<TOOL>``; plus configurations of the tool itself
* Grid parameters: They help to fix which queues are used for each of the steps, how much files per job, etc. 


By default, the ZT score normalization is activated. To deactivate it, please add the ``-z`` to the command line.

One way to compute the final result is to use the *bob_compute_perf.py* script from your Bob installation, e.g., by calling:

.. code-block:: sh

  $ bin/bob_compute_perf.py -d PATH/TO/USER/DIRECTORY/scores-dev -t PATH/TO/USER/DIRECTORY/scores-eval


Experiment design
-----------------

To be very flexible, the tool chain in the `xbob.speaker_recognition`_ is designed in several stages::

  1. Signal Preprocessing
  2  Feature Extraction
  3. Feature Projection
  4. Model Enrollment
  5. Scoring

Note that not all tools implement all of the stages.


Voice Activity Detection 
~~~~~~~~~~~~~~~~~~~~~~~~
This step aims to filter out the non speech part. Depending on the configuration file, several routines can be enabled or disabled.

* Energy-based VAD
* 4Hz Modulation energy VAD

Feature Extraction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This step aims to extract features. Depending on the configuration file, several routines can be enabled or disabled.

* LFCC/MFCC feature extraction
* Spectrogram extraction
* Feature normalization


Feature Projection
~~~~~~~~~~~~~~~~~~
Some provided tools need to process the features before they can be used for verification.
In the `xbob.speaker_recognition`_, this step is referenced as the **projection** step.
Again, the projection might require training, which is executed using the extracted features from the training set.
Afterward, all features are projected (using the the previously trained Projector).


Model Enrollment
~~~~~~~~~~~~~~~~
Model enrollment defines the stage, where several (projected or unprojected) features of one identity are used to enroll the model for that identity.
In the easiest case, the features are simply averaged, and the average feature is used as a model.
More complex procedures, which again might require a model enrollment training stage, create models in a different way.


Scoring
~~~~~~~
In the final scoring stage, the models are compared to probe features and a similarity score is computed for each pair of model and probe.
Some of the models (the so-called T-Norm-Model) and some of the probe features (so-called Z-Norm-probe-features) are split up, so they can be used to normalize the scores later on.



Command line options
--------------------
Additionally to the required command line options discussed above, there are several options to modify the behavior of the `xbob.speaker_recognition`_ experiments.
One set of command line options change the directory structure of the output:

* ``--temp-directory``: Base directory where to write temporary files into (the default is */idiap/temp/$USER/<DATABASE>* when using the grid or */scratch/$USER/<DATABASE>* when executing jobs locally)
* ``--user-directory``: Base directory where to write the results, default is */idiap/user/$USER/<DATABASE>*
* ``--sub-directory``: sub-directory into *<TEMP_DIR>* and *<USER_DIR>* where the files generated by the experiment will be put
* ``--score-sub-directory``: name of the sub-directory in *<USER_DIR>/<PROTOCOL>* where the scores are put into

If you want to re-use parts previous experiments, you can specify the directories (which are relative to the *<TEMP_DIR>*, but you can also specify absolute paths):

* ``--preprocessed-image-directory``
* ``--features-directory``
* ``--projected-directory``
* ``--models-directories`` (one for each the Models and the T-Norm-Models)

or even trained Extractor, Projector, or Enroler (i.e., the results of the extraction, projection, or enrollment training):

* ``--extractor-file``
* ``--projector-file``
* ``--enroler-file``

For that purpose, it is also useful to skip parts of the tool chain.
To do that you can use:

* ``--skip-preprocessing``
* ``--skip-feature-extraction-training``
* ``--skip-feature-extraction``
* ``--skip-projection-training``
* ``--skip-projection``
* ``--skip-enroler-training``
* ``--skip-model-enrolment``
* ``--skip-score-computation``
* ``--skip-concatenation``

although by default files that already exist are not re-created.
To enforce the re-creation of the files, you can use the ``--force`` option, which of course can be combined with the ``--skip...``-options (in which case the skip is preferred).

There are some more command line options that can be specified:

* ``--no-zt-norm``: Disables the computation of the ZT-Norm scores.
* ``--groups``: Enabled to limit the computation to the development ('dev') or test ('eval') group. By default, both groups are evaluated.
* ``--preload-probes``: Speeds up the score computation by loading all probe features (by default, they are loaded each time they are needed). Use this option only, when you are sure that all probe features fit into memory.
* ``--dry-run``: When the grid is enabled, only print the tasks that would have been sent to the grid without actually send them. **WARNING** This command line option is ignored when no ``--grid`` option was specified!


Databases
---------

For the moment, there are 3 databases that are tested in `xbob.speaker_recognition`_. Their protocols are also shipped with the tool. You can use the script ``bob_compute_perf.py`` to compute EER and HTER on DEV and EVAL as follows:

.. code-block:: sh

  $ bin/bob_compute_perf.py -d scores-dev -t scores-eval -x


BANCA database
~~~~~~~~~~~~~~
This is a clean database. The results are already very good with a simple baseline system. In the following example, we apply the UBM-GMM system.

.. code-block:: sh

  $ bin/spkverif_isv.py -d config/database/banca_audio_G.py -t config/tools/ubm_gmm_regular_scoring.py  -p config/preprocessing/energy.py -f config/features/mfcc_60.py -z
  

* ``DEV: EER = 1.656%``
* ``EVAL: EER = 0.694%``


MOBIO database
~~~~~~~~~~~~~~
This is a more challenging database. The noise and the short duration of the segments make the task of speaker recognition very difficult. The following experiment on male group uses the ISV modelling technique.

.. code-block:: sh

  $ ./bin/spkverif_isv.py -d config/database/mobio_male_twothirds_wav.py -t config/tools/isv.py -p config/preprocessing/mfcc_60.py 
  
  
* ``DEV: EER = 19.881%``
* ``EVAL: EER = 15.508%``

NIST-SRE2012 database
~~~~~~~~~~~~~~~~~~~~~
We first invite you to read the paper describing our system submitted to the NIST-SRE2012 Evaluation, and the paper describing I4U system (joint submission with I2R, RUN, UEF, VLD, LIA, UTD, UWS). The protocols on the development set are the results of a joint work by the I4U group (check if we can make them publicly available).



.. _Bob: http://idiap.github.com/bob/
.. _local.bob.recipe: https://github.com/idiap/local.bob.recipe
.. _gridtk: https://github.com/idiap/gridtk
.. _BuildOut: http://www.buildout.org/
.. _NIST: http://www.nist.gov/itl/iad/ig/focs.cfm
.. _xbob.db.verification.filelist: https://pypi.python.org/pypi/xbob.db.verification.filelist
.. _pysox: https://pypi.python.org/pypi/pysox
.. _xbob.speaker_recognition: https://github.com/bioidiap/xbob.speaker_recognition
.. _pypi: https://pypi.python.org/pypi