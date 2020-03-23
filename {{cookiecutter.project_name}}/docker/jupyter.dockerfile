FROM jupyter/minimal-notebook
COPY envs/ /envs
RUN rm /opt/conda/.condarc 
RUN conda env update --file /envs/{{cookiecutter.project_slug}}_conda.yml
