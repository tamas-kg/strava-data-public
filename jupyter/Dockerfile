FROM jupyter/base-notebook:python-3.11

USER root

# Install system deps
RUN apt-get update && apt-get install -y \
    openjdk-17-jdk \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Add JDBC driver for Spark
RUN wget https://jdbc.postgresql.org/download/postgresql-42.7.3.jar \
    -P /opt/spark/jars/

USER jovyan

# Python packages
RUN pip install --no-cache-dir \
    pandas==2.2.2 \
    psycopg2-binary \
    sqlalchemy==2.0.36 \
    jupyterlab \
    ipython-sql \
    pyspark \
    prettytable==3.9.0 \
    dbt-postgres

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64
ENV PATH=$JAVA_HOME/bin:$PATH

ENV JUPYTER_ENABLE_LAB=yes

WORKDIR /home/jovyan/work

CMD ["start-notebook.sh", "--NotebookApp.token=''", "--NotebookApp.password=''", "--NotebookApp.notebook_dir=/home/jovyan/work"]