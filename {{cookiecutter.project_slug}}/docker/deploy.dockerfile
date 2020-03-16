FROM {{cookiecutter.docker_target_image}}
RUN snakemake -F --use-conda