FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /opt/endee

# Install base dependencies required for building Endee
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    wget gnupg2 ca-certificates lsb-release sudo curl unzip git build-essential cmake \
    software-properties-common \
    libssl-dev libcurl4-openssl-dev \
 && rm -rf /var/lib/apt/lists/*

# Install LLVM/Clang 19 (install.sh expects clang-19)
RUN wget https://apt.llvm.org/llvm.sh -O /tmp/llvm.sh \
 && chmod +x /tmp/llvm.sh \
 && /tmp/llvm.sh 19 \
 && rm /tmp/llvm.sh

# Copy repository and run the project's install script
COPY . /opt/endee
WORKDIR /opt/endee

# Make install/run scripts executable
RUN chmod +x ./install.sh ./run.sh || true

# Run install script to build Endee (release build)
RUN ./install.sh --release || true

# Expose default Endee port and set runtime command
EXPOSE 8080

VOLUME ["/data"]

CMD ["/bin/bash", "./run.sh", "ndd_data_dir=/data"]
