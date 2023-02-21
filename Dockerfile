# app/Dockerfile

FROM python:3.10-slim

WORKDIR /app
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/Toroi0610/autopiet-streamlit .

RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install matplotlib 
RUN pip3 install numpy 
RUN pip3 install streamlit

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]