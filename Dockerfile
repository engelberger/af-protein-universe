FROM pytorch/pytorch:2.1.2-cuda12.1-cudnn8-runtime
ENV DEBIAN_FRONTEND=noninteractive

COPY requirements.txt /tmp/requirements.txt

RUN python -m pip install --no-cache-dir -r /tmp/requirements.txt

#RUN wget -P /tmp \
#    "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh" \
#    && bash /tmp/Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda \
#    && rm /tmp/Miniconda3-latest-Linux-x86_64.sh
#ENV PATH /opt/conda/bin:$PATH
#
#
### installing into the base environment since the docker container wont do anything other than run openfold
#RUN conda install -c conda-forge mamba
#
#
#
#RUN mamba create -n e3nndens python=3.11 -y
#RUN mamba env update -n basis --file /tmp/e3nndens