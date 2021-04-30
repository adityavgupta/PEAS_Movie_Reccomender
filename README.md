# A Simple Movie Recommender App
Simple Movie and TV Show recommender app based on cosine similarity for CS411 at UIUC 

## Requirements
```
python >= 3.5
```

## Getting started
```bash
git clone https://github.com/a2975667/flask-gcp-mysql-demo.git
cd flask-gcp-mysql-demo
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP = app
flask run
```

## Setting up GCP
Create a `app.yaml` file in the root folder with the following content:
```yaml
runtime: python38 # or another supported version

instance_class: F1

env_variables:
  MYSQL_USER: <user_name> # please put in your credentials
  MYSQL_PASSWORD: <user_pw> # please put in your credentials
  MYSQL_DB: <database_name> # please put in your credentials
  MYSQL_HOST: <database_ip> # please put in your credentials

handlers:
# Matches requests to /images/... to files in static/images/...
- url: /img
  static_dir: static/img

- url: /script
  static_dir: static/script

- url: /styles
  static_dir: static/styles
```

Setting up the deployment
```bash
curl https://sdk.cloud.google.com | bash
gcloud components install app-engine-python
gcloud config set project cs411-sp21
gcloud auth login
gcloud app deploy
```

# Tutorial to build website on Google Cloud Platform - Credits to Ti-Chung
[![](http://img.youtube.com/vi/sY1lLGe7ECA/0.jpg)](http://www.youtube.com/watch?v=sY1lLGe7ECA "")

A comprehensive writeup is avaliable [here](https://tichung.com/blog/2021/20200323_flask/).
