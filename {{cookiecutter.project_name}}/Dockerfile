# Requires rocker/verse image
FROM rocker/verse:3.6.1

#################################################
# Install additional required R packages        #
#################################################

# github API calls are limited, cloning is more reliable because it does not require API
RUN git clone -b 0.9.3 --single-branch https://github.com/rstudio/renv.git renv 
RUN R -e "devtools::install('renv/')"
RUN rm -r -f renv

###########################################
# Install Conda                           #
###########################################

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

RUN apt-get update --fix-missing && \
    apt-get install -y wget bzip2 ca-certificates curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-4.5.11-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda clean -tipsy && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

###########################################
# Install Snakemake                       #
###########################################

RUN apt-get update
RUN apt-get install build-essential -y
RUN apt-get install graphviz -y
RUN conda update -n base -c defaults conda
RUN conda install git
RUN apt-get -qq update 
RUN apt-get install -qqy python3-setuptools python3-docutils python3-flask
RUN pip install psutil
RUN conda install datrie
# snakemake >5.10 makes --cores parameter mandatory 
RUN pip install snakemake==5.10
RUN pip install networkx pygraphviz
RUN apt install imagemagick -y
RUN pip install pygments
RUN pip install jinja2

###########################################
# Prepare code folder                     #
###########################################

# code folder ----------------------------------------------------------
# data/ folder is not added by default, change .dockerignore if needed
# use docker run -w /repo when executing container without mounting to repo
COPY . /repo 

#  mount folder --------------------------------------------------------
WORKDIR /app


###########################################
# Install R packages for demo             #
###########################################
  
RUN R -e "remotes::install_version('easyalluvial', version = '0.2.0', repos='http://cran.us.r-project.org', upgrade = 'never')"

###########################################
# Install python packages for demo        #
###########################################

# # option 1 -----------------------------------------------------------
# # specify OS-specific conda environment yml file in envs/
# # alternatively use requirements.txt or python3 env

# # option 2 -----------------------------------------------------------
# # install directly into base environment
# RUN conda install thrift_sasl=0.2.1 -c conda-forge
# RUN pip install thrift_sasl==0.2.1

# # option 3 -----------------------------------------------------------
# # create conda env inside container
# RUN conda create --name impala python=3.6 ibis-framework=0.13.0
# RUN conda install -n impala thrift_sasl=0.2.1 -c conda-forge

# # add pip conf file if alternative pip server should be used
# # needs to be added to repo first
# ADD pip.conf /etc/ 

# ENV PATH /opt/conda/envs/impala/bin:$PATH
# RUN /bin/bash -c "source activate impala" && \
#     pip install hdfs==2.1.0 

# # activate conda environment per default
# RUN echo "conda activate impala" >> ~/.bashrc

## option 4 ------------------------------------------------------------
# (prefered option, can be repeated for jupyter notebook image)
# specify packages in envs/cookiedsdemo_conda.yml

RUN conda env update --file /repo/envs/cookiedsdemo_conda.yml

###########################################
# Set environment variables               #
###########################################

ENV JOB_VAR1=USE_ENVVARS_TO_CONFIGURE_JOBS
ENV CORES=1

###########################################
# default container command               #
###########################################

CMD snakemake test -F && \
    snakemake -F --cores $CORES && \
    R -f .doc_templates/render_docs.R 