# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

# Execute during the build of the image
ARG TEMPIO_VERSION
ARG BUILD_ARCH
RUN \
    curl -sSLf -o /usr/bin/tempio \
    "https://github.com/home-assistant/tempio/releases/download/${TEMPIO_VERSION}/tempio_${BUILD_ARCH}"

# Install required packages
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-setuptools \
    py3-wheel \
    git \
    && rm -rf /var/cache/apk/*

# Install Python dependencies
RUN pip3 install --no-cache-dir requests

# Install cc2538-bsl tool
RUN pip3 install --no-cache-dir git+https://github.com/JelmerT/cc2538-bsl.git

# Copy root filesystem
COPY rootfs /
