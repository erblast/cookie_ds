|Snakemake| |Build Status| `snakemake
report <https://erblast.github.io/snakemake_minimal/>`__ |gitrepo|

snakemake minimal workflow
==========================

In ``Snakefile`` a set of rules are supplied on the basis of which
output files are supposed to be produced by the workflow.

It is customary to start with ``rule all`` a blank rule that uses all
final output files as input files. ``snakemake`` will go through the
rest of the rules and create an execution sequence for all rules based
on the first rule. It will also determine which steps can be executed in
parallel.

Run in docker container
-----------------------

::

   docker run -it --rm -v "$PWD":/app erblast/r_conda_snakemake_pkgs

Execute
-------

.. code:: shell

   snakemake

Dryrun
------

.. code:: shell

   snakemake -n

Execute after code changes
--------------------------

.. code:: shell

   snakemake -R `snakemake --list-code-changes`

Force re-execution
------------------

.. code:: shell

   snakemake -F

Parallel Processing
-------------------

.. code:: shell

   snakemake --cores 3

Execute and build conda environment
-----------------------------------

The conda environment will be reconstructed from ``yml`` file and stored
in ``./.snakemake/conda``. A single conda environment can be defined for
each rule.

.. code:: shell

   conda env export --name snakemake_minimal -f ./envs/snake_minimal_macos.yml

.. code:: shell

   snakemake --use-conda

Bringing it all together
------------------------

.. code:: shell

   snakemake -R `snakemake --list-code-changes` --use-conda --cores 3

Visualize workflow
------------------

.. code:: shell

   snakemake --dag | dot -Tpng > ./docs/wflow.png

|image3|

Build Report
------------

::

   snakemake --report docs/index.html

YAML configuration file
-----------------------

``config.yml``

Shell vs Scripts
================

Scripts in ``R`` and ``python`` have access to a ``snakemake`` object
carrying all rule parameters as attributes. However when shell commands
can be constructed snakemake’s parallel processing and logging
capabilities can be leveraged.

R Scripts and Markdown
======================

R scripts can be added as ``.R`` or as ``.Rmd``. When they are added as
``.Rmd`` they can only produce one single html-output file. A workaround
is to use an intermediate R script as shown in rule.

**see rules ``plot_rmd_direct`` and ``plot_rmd_via_script``
in**\ `Snakefile <https://github.com/erblast/snakemake_minimal/blob/master/Snakefile>`__

Python Scripts and Jupyter Notebooks
====================================

Python scripts can be added as ``.py`` files. We can use ``papermill``
to execute parametrized jupyter notebooks which we can then render as
html. html is preferred to notebooks because there is no doubt about the
execution state.

**see rules ``plot_execute_nb`` and
``plot_nb_2_html``**\ `Snakefile <https://github.com/erblast/snakemake_minimal/blob/master/Snakefile>`__

\*\* the rules for rendering notebooks are not compatible with
``nb_conda`` as is.*\*

Testing
=======

All common R functions are collected in an R package under utilR which
is checked and tested

Benchmarking
------------

Execution times of each rule are stored in ``./benchmark``. Can be
defined in ``Snakefile``

Logging
-------

unfortunately logging is not supported for scripts thus needs to be
setup for each script individually using script-language-specific tools.
https://bitbucket.org/snakemake/snakemake/issues/917/enable-stdout-and-stderr-redirection

.. |Snakemake| image:: https://img.shields.io/badge/snakemake-≥5.6.0-brightgreen.svg?style=flat
   :target: https://snakemake.readthedocs.io
.. |Build Status| image:: https://travis-ci.org/erblast/snakemake_minimal.svg?branch=master
   :target: https://travis-ci.org/erblast/snakemake_minimal
.. |gitrepo| image:: https://icons-for-free.com/iconfiles/png/128/git+github+icon-1320191654571298174.png
   :target: https://github.com/erblast/snakemake_minimal
.. |image3| image:: ./docs/wflow.png
