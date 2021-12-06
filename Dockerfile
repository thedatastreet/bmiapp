FROM ubuntu

ENV INSTALL_PATH /home/bmiapp
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

LABEL classifier_version="1.0"
LABEL owner="Sitaram Tadepalli"

# Install libraries and packages
RUN apt-get update && apt-get install -y \
python3-pip \
python3-dev \
python3-numpy \
python3-scipy 

RUN pip3 install scikit-learn flask flask-restful joblib flask-material pandas

COPY app.py /home/bmiapp/app.py
COPY model /home/bmiapp/model
COPY templates /home/bmiapp/templates

# Expose the port for the API
EXPOSE 5000

# Set Environment variables
ENV environment PRODUCTION
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV FLASK_APP app.py

# Run the API
#CMD ["python3", "-m", "flask", "run", "--host", "0.0.0.0"]
CMD ["python3","app.py"]
