import os
from os.path import join, dirname
from dotenv import load_dotenv

env_path = join(dirname(__file__), '.env')
load_dotenv(env_path)

BEARER_TOKEN  = os.environ.get("BEARER_TOKEN")
API_KEY  = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
ACCESS_TOKEN   = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET   = os.environ.get("ACCESS_TOKEN_SECRET")
FIREBASE_KEY = {"type":os.environ.get("FB_TYPE"),"project_id":os.environ.get("FB_PROJECT_ID"),"private_key_id":os.environ.get("FB_PRIVATE_KEY_ID"),"private_key":os.environ.get("FB_PRIVATE_KEY"),"client_email":os.environ.get("FB_CLIENT_EMAIL"),"client_id":os.environ.get("FB_CLIENT_ID"),"auth_uri":os.environ.get("FB_AUTH_URI"),"token_uri":os.environ.get("FB_TOKEN_URI"),"auth_provider_x509_cert_url":os.environ.get("FB_AUTH_PROVIDER_CERT"),"client_x509_cert_url":os.environ.get("FB_CLIENT_CERT")}
    


