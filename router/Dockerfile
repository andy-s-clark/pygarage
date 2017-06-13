FROM debian:jessie

ENV HOME /home/crossbar
ARG PYPY_VERSION=5.8.0
ARG PYPY_SHA256SUM=57d871a7f1135719c138cee4e3533c3275d682a76a40ff668e95150c65923035
ARG CROSSBAR_VERSION=17.5.1

# Install dependencies and Crossbar.io
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      ca-certificates \
      curl \
      expat \
      build-essential \
      libssl-dev \
    # Install PyPy3 from upstream tarball
    && set -ex \
    && curl -L --output /tmp/pypy.tar.bz2 https://bitbucket.org/pypy/pypy/downloads/pypy3-v${PYPY_VERSION}-linux64.tar.bz2 \
    && echo "$PYPY_SHA256SUM /tmp/pypy.tar.bz2" | sha256sum -c \
    && tar -xjC /usr/local --strip-components=1 -f /tmp/pypy.tar.bz2 \
    && rm /tmp/pypy.tar.bz2 \
    && curl -L --output /tmp/get-pip.py https://bootstrap.pypa.io/get-pip.py \
    && pypy3 /tmp/get-pip.py \
    && rm /tmp/get-pip.py \
    # Install Crossbar.io from PyPI
    && pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir crossbar==${CROSSBAR_VERSION} \
    # Cleanup
    && apt-get remove -y wget expat build-essential \
    && rm -rf ~/.cache \
    && rm -rf /var/lib/apt/lists/*

# Remove old crossbar home folder and create user
RUN rm -rf ${HOME} \
    ; adduser --system --group --home ${HOME} crossbar

WORKDIR ${HOME}

USER crossbar

# Verify that crossbar installed and is usable by the crossbar user
RUN crossbar version

# Copy configuration
COPY . ${HOME}

EXPOSE 8080

CMD ["crossbar", "start", "--cbdir", "/home/crossbar"]
