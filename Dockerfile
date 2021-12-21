### Duplicate of dst-panel-demo/Dockerfile



FROM continuumio/miniconda3

# TODO : split this image in Dockerfile.base and Dockerfile.prod

# The enviroment variable ensures that the python output is set straight
# to the terminal without buffering it first
ENV PYTHONUNBUFFERED 1

WORKDIR /

# TODO : move Dockerfile to this repo, then use COPY instead of clone repo
# TODO : use https://github.com/ECCC-CCCS/decision-support-tool.git, not this fork
RUN git clone https://github.com/matprov/decision-support-tool.git app

WORKDIR /app

# TODO : not necessary when changes will be merged
RUN git checkout trials

RUN conda create --name dst python=3.7

# TODO : fix deps in decision-support-tool repo
RUN sed -i '/os/d' ./requirements.txt
RUN sed -i '/json/d' ./requirements.txt
# TODO : add deps to requirements
RUN conda install --channel conda-forge cartopy
RUN pip install Cython
RUN pip install xlrd

RUN pip install -r requirements.txt
RUN pip install jupyterlab

EXPOSE 5006

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "dst", "panel", "serve", "decision-support-tool.ipynb", "--session-token-expiration", "86400"]
