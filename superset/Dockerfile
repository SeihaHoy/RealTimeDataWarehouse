FROM apache/superset:latest

USER root

# Install dependencies
RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev-compat \
    libmariadb-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python packages
RUN pip install mysqlclient pinotdb

# Copy the initialization script
COPY ./superset-init.sh /superset-init.sh

# Set correct permissions
RUN chmod 755 /superset-init.sh

# Copy the Superset configuration file
COPY superset_config.py /app/
ENV SUPERSET_CONFIG_PATH /app/superset_config.py

# Switch back to Superset user
USER superset

ENTRYPOINT ["/superset-init.sh"]
