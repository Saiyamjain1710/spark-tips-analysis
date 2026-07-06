FROM openjdk:11-jre-slim-buster

# Install Python and pip (if not already in base image, or ensure correct version)
RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

# Set environment variables for Spark
ENV SPARK_VERSION=3.5.1
ENV HADOOP_VERSION=3
ENV SPARK_HOME=/spark
ENV PATH="$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin"

# Download and extract Spark
RUN wget -qO- https://archive.apache.org/dist/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION.tgz | tar xvz -C / 
RUN mv /spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION /spark

# Install PySpark and findspark
RUN pip install pyspark==$SPARK_VERSION findspark

# Create a working directory
WORKDIR /app

# Copy the Spark application and data into the container
COPY spark_app.py .
COPY tips.csv .

# Create a directory for output (and set permissions if needed)
RUN mkdir -p /app/output

# Command to run the Spark application
CMD ["spark-submit", "spark_app.py"]