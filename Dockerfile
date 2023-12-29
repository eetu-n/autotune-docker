FROM node:alpine

COPY src/get.py /get.py
COPY src/init.sh /init.sh

RUN apk update &&\
    apk add python3 py3-requests git sudo coreutils bash jq curl &&\
    mkdir -p /openaps/settings && \
    chown -Rh node:node /openaps && \
    chown -Rh node:node /get.py && \
    chown -Rh node:node /init.sh && \
    chmod +x /init.sh

RUN git clone https://github.com/openaps/oref0
RUN chown -Rh node:node /oref0
WORKDIR /oref0
RUN npm run global-install

USER node
ENTRYPOINT /init.sh

