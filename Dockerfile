FROM python:3

# Exposes this container's port 4141 to other containers.
EXPOSE 9900

# Sets the workdir of our container to dir below.
WORKDIR /usr/src/app

# Copies our project and its requirements.txt over to the dir above.
COPY requirements.txt .
COPY config.yml .
COPY CryptoBook .

# Installs the requirements of our project.
RUN pip install --no-cache-dir -r requirements.txt

# Runs the API when the container is ran.
CMD [ "python", "api.py" ]
