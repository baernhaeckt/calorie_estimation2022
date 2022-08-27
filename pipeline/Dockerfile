FROM tensorflow/tensorflow:2.5.0-gpu

# Fix for the public key error
# https://github.com/NVIDIA/nvidia-docker/issues/1632
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/7fa2af80.pub


# Install Common Dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    ffmpeg \
    libsm6 \
    libxext6

# Conda Environment
ENV MINICONDA_VERSION py38_4.11.0
ENV PATH /opt/miniconda/bin:$PATH
RUN wget -qO /tmp/miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh && \
    bash /tmp/miniconda.sh -bf -p /opt/miniconda && \
    conda clean -ay && \
    rm -rf /opt/miniconda/pkgs && \
    rm /tmp/miniconda.sh && \
    find / -type d -name __pycache__ | xargs rm -rf