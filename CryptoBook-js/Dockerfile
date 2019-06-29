FROM ubuntu:18.04

# Install NodeJS and npm
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install nodejs
RUN apt-get install -y npm

RUN npm install -g socket.io-client
RUN npm install -g socket.io
RUN npm install -g express
RUN npm install -g js-yaml

# Exposes this container's port 5050 to other containers.
EXPOSE 5050

# Sets the workdir of our container to dir below.
WORKDIR /usr/src/app/

RUN npm link socket.io-client
RUN npm link express
RUN npm link socket.io
RUN npm link js-yaml

COPY config.yml ./
COPY CryptoBook-js/ccc-streamer-utilities.js ./
COPY CryptoBook-js/cryptocompare_streamer.js ./

# Runs the js server.
CMD [ "node", "cryptocompare_streamer" ]
