FROM {{cookiecutter.docker_base_image}}

COPY ./ /app/
WORKDIR /app

CMD snakemake --use-conda