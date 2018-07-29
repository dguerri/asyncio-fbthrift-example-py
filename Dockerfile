FROM ubuntu:18.04

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y \
  autoconf \
  automake \
  binutils-dev \
  bison \
  build-essential \
  cmake \
  flex \
  g++ \
  git \
  libboost-all-dev \
  libdouble-conversion-dev \
  libevent-dev \
  libgflags-dev \
  libgoogle-glog-dev \
  libiberty-dev \
  libjemalloc-dev \
  libkrb5-dev \
  liblz4-dev \
  liblzma-dev \
  libmstch-dev \
  libsnappy-dev \
  libssl-dev \
  libzstd-dev \
  make \
  pkg-config \
  python3-future \
  python3-six \
  zlib1g-dev

ENV FOLLY_TAG v2018.07.23.00
RUN cd /root && \
  git clone --branch $FOLLY_TAG https://github.com/facebook/folly.git

RUN cd /root/folly && \
  mkdir _build && cd _build && \
  cmake configure ..  -DBUILD_TESTS=OFF && \
  make -j $(nproc) && \
  make install

ENV WANGLE_TAG v2018.07.23.00
RUN cd /root && \
  git clone --branch $WANGLE_TAG https://github.com/facebook/wangle.git

RUN cd /root/wangle/wangle && \
  cmake . -DBUILD_TESTS=OFF && \
  make -j $(nproc) && \
  make install

ENV FBTHRIFT_TAG v2018.07.23.00
RUN cd /root && \
  git clone --branch $FBTHRIFT_TAG https://github.com/facebook/fbthrift.git

RUN cd /root/fbthrift && \
  cd build && \
  cmake .. && \
  make -j $(nproc) && \
  make install

RUN cd /root/fbthrift/thrift/lib/py && \
  python3 ./setup.py install

COPY demo-ssl-stuff-do-not-use /root/ssl-stuff
COPY source /root/fbthrift-example

RUN cd /root/fbthrift-example && \
  thrift1 -v --gen py:asyncio,new_style mytest.thrift
