FROM continuumio/miniconda3

# The enviroment variable ensures that the python output is set straight
# to the terminal without buffering it first
ENV PYTHONUNBUFFERED 1

WORKDIR /

COPY . app

WORKDIR /app

# TODO : not necessary when changes will be merged
RUN git checkout trials

RUN conda create --name dst python=3.7

RUN conda install --channel conda-forge cartopy

RUN pip install -r requirements.txt

EXPOSE 5006

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "dst", "panel", "serve", "decision-support-tool.ipynb", "--session-token-expiration", "86400"]
