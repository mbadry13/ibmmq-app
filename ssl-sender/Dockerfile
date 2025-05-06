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

# Set MQ environment variables
ENV LD_LIBRARY_PATH=/opt/mqm/lib64
ENV MQ_INSTALLATION_PATH=/opt/mqm
ENV MQ_INSTALLATION_NAME=Installation1

# Install PyMQI
RUN pip install pymqi

# App setup
WORKDIR /app
COPY ../requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY app.py .

# Copy SSL key repository
COPY client.kdb /app/ssl/
COPY client.sth /app/ssl/

# Optional: Set permissions if needed
RUN chmod 600 /app/ssl/client.kdb /app/ssl/client.sth
RUN ls -l /app/ssl


CMD ["python", "app.py"]

