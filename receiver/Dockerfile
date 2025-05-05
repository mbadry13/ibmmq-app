FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    make \
    libffi-dev \
    libssl-dev \
    tar \
    && rm -rf /var/lib/apt/lists/*

# Add MQ Client
COPY ../ibmmq-client-linux-x64.tar.gz /tmp/
RUN mkdir -p /opt/mqm && \
    tar -xzf /tmp/ibmmq-client-linux-x64.tar.gz -C /opt/mqm && \
    rm /tmp/ibmmq-client-linux-x64.tar.gz && \
    cd /opt/mqm/bin && \
    ./mqlicense -accept

# Set environment variables for MQ
ENV LD_LIBRARY_PATH=/opt/mqm/lib64
ENV MQ_INSTALLATION_PATH=/opt/mqm
ENV MQ_INSTALLATION_NAME=Installation1

# Install PyMQI after MQ client is available
RUN pip install pymqi

# App setup
WORKDIR /app
COPY ../requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]

