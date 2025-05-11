FROM mcr.microsoft.com/devcontainers/miniconda:latest

# Copy the environment.yml into the container
COPY environment.yml /tmp/environment.yml

# Create the Conda environment
RUN conda env create -f /tmp/environment.yml

# Activate the environment by default in all shells
RUN echo "conda activate thermo" >> /etc/bash.bashrc