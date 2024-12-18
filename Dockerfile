# Base image must at least have pytorch and CUDA installed.
# We are using NVIDIA NGC's PyTorch image here, see: https://ngc.nvidia.com/catalog/containers/nvidia:pytorch for latest version
# See https://docs.nvidia.com/deeplearning/frameworks/support-matrix/index.html#framework-matrix-2021 for installed python, pytorch, etc. versions

# for LSV A100s server
FROM nvcr.io/nvidia/pytorch:24.09-py3

# for LSV V100 server
# FROM nvcr.io/nvidia/pytorch:21.07-py3

# Set path to CUDA
ENV CUDA_HOME=/usr/local/cuda

# Install additional programs
RUN apt update && \
    apt install -y build-essential \
    pkg-config \
    git \
    sudo \
    htop \
    gnupg \
    curl \
    ca-certificates \
    vim \
    tmux
#    rm -rf /var/lib/apt/lists

# Update pip
RUN SHA=ToUcHMe which python3
RUN python3 -m pip install --upgrade pip

# See http://bugs.python.org/issue19846
ENV LANG C.UTF-8

# Install Rust and Cargo
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y && \
    echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc && \
    source ~/.bashrc

# Add Rust and Cargo to PATH for all users
ENV PATH="/root/.cargo/bin:$PATH"

# clone parser and make evaluation folder(?)
WORKDIR /
RUN git clone https://github.com/nikitakit/self-attentive-parser.git
WORKDIR /self-attentive-parser/EVALB
RUN make

# install python dependencies from requirements.txt file
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Specify a new user (USER_NAME and USER_UID are specified via --build-arg)
ARG USER_UID
ARG USER_NAME
ENV USER_GID=$USER_UID
ENV USER_GROUP="users"

# Create the user
RUN mkdir /home/$USER_NAME
RUN useradd -l -d /home/$USER_NAME -u $USER_UID -g $USER_GROUP $USER_NAME

# this will fix a wandb issue
RUN mkdir /home/$USER_NAME/.local

# Change owner of home dir (Note: this is not the lsv nethome)
RUN chown -R ${USER_UID}:${USER_GID} /home/$USER_NAME/

CMD ["/bin/bash"]
