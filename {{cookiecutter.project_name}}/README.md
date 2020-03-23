[![Snakemake](https://img.shields.io/badge/snakemake-≥5.6.0-brightgreen.svg?style=flat)](https://snakemake.readthedocs.io)
[![Build Status]({{cookiecutter.travis_badge}})]({{cookiecutter.travis_address}})

# {{cookiecutter.project_name}}

{{cookiecutter.description}}

# Git Page with Documentation

[{{cookiecutter.git_pages_address}}]({{cookiecutter.git_pages_address}})

## Start-up development endpoint

```
docker-compose build --parallel # needs internet connection
docker-compose up -d 
docker container exec -it {{cookiecutter.project_name}}_shell_1 /bin/bash 
# exit
# docker-compose down
```

This starts the following images mounted with the local working directory:
- [RStudio server, http://localhost:8787/](http://localhost:8787/)
- [jupyter notebook server, http://localhost:8888/](http://localhost:8888/)
- [jekyll server, http://localhost:4000/](http://localhost:4000/) (renders content of docs/ folder)

## Available Shell Commands

```
snakemake                               # runs exec rule
snakmeake exec                          # runs exec rule
snakemake test                          # runs test rule
snakemake job                           # runs job rule
snakemake -n                            # dry-run of exec rule
snakemake -F                            # force re-execution of rule input and output files
snakemake plot -f                       # limit re-execution to rule output files
snakemake --cores 3                     # set number of cores, snakemake will execute rules in parallel if possible
R -f .doc_templates/render_docs.R       # renders documentation, needs internet connection
```

## Execute Container

- runs **test**, **exec** and renders documentation into docs/

Code in **test** shoulld be leightweight and execute in minutes. It usually executes unit tests of packaged functions and objects and renders package documentation

Code in **exec** should accesses a inmutable data. It can contain static experiments or code for training models. 
Critical parts should be packaged and unit tested. This step is allowed to take up many computational ressources.

```
docker run -v"$PWD:/app/" {{cookiecutter.project_name}}               # uses code in mounted folder
docker run -w /repo {{cookiecutter.project_name}}                     # uses code copied into container
docker run -w /repo -e NCPUS=12 {{cookiecutter.project_name}}         # increase number of CPU

```

## Execute Job Rule

The **job** rule in this demo repo does not do much. Code executed by a **job** rule should have a very high test coverage and configuration should be expressive using envirnment variables, rather than hidden in config files. Should be used for accessing data that periodcially refreshes and is allowed to take up many computationanl ressources. A typical application would be to generate predictions from a pre-trained model on new data.

```
docker run -v"$PWD:/app/" -e JOB_VARS1=job_configuration {{cookiecutter.project_name}} snakemake job -F --cores 1
docker run -w /repo -e JOB_VARS1=job_configuration {{cookiecutter.project_name}} snakemake job -F --cores 1
```

## CI/CD using travis

the folders `docs/` and `data/` were added to `.gitignore` because there content is dependent on code execution which can easily be forgotten before commiting to git. Data input and output is preferably stored outside the repo in a database or another form of remote data storage. The documentation containing reports, plots and references can be added automatically deployed to a separate branch in the code repository.

For example travis can be set-up to publish the content of the `docs/` folder to the `gh-pages` branch.

- enable gitpage rendering in github repository settings, and publish to gh-pages branch
- follow these [instructions](https://www.r-bloggers.com/continuous-deployment-of-package-documentation-with-pkgdown-and-travis-ci/) to set configure travis.


`.travis.yml` file

```
language: ruby

services:
  - docker
  
script: 
  - docker build -t {{cookiecutter.project_name}} .
  # in CI we would only run light weight tests 
  - docker run -v"$PWD:/app/" {{cookiecutter.project_name}} snakemake test -F
  # in CD we would run the entire container default command here we use travis for both
  - docker run -v"$PWD:/app/" {{cookiecutter.project_name}}
  # we would normally use a job scheduler to run jobs, here we also use travis
  - docker run -v"$PWD:/app/" -e JOB_VARS1=job_configuration {{cookiecutter.project_name}} snakemake job -F --cores 1
  
# https://www.r-bloggers.com/continuous-deployment-of-package-documentation-with-pkgdown-and-travis-ci/
deploy:
  provider: pages
  skip_cleanup: true
  github_token: $GITHUB_TOKEN  # Set in the settings page of your repository, as a secure variable
  keep_history: true
  local-dir: docs
```


In this case executing the entire code in the container is pretty lightweight and we can have travis test all of the rules.

