from datetime import datetime
from  time import sleep
from fastapi import FastAPI
import database
import twitter
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


origins = [
    "https://7chord-twitter-tool-frontend.vercel.app",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


get_tw = twitter.get_twitter()
db = database.firebase_client()


@app.get("/")
def root():
    return "success!!"

# @app.get('/get_twitter')
# def get_tweets():
#     test ="ゲームを作りながら楽しく学べるPythonプログラミング (Future Coders（NextPublishing）) Kindle版 おすすめ プログラミング 初心者 本 エンジニア 入門書  https://t.co/jckW6yE0j1"
#     pluss_word_list =["ゲーム","Python","AWS"]
#     minus_word_list =["初心者"]
#     res = get_tw.scoring(test,pluss_word_list,minus_word_list)
#     return res


@app.get('/get_twitter')
def set_tweets():
    # test = get_tw.get_users_blocked()  
    users_json_array = get_tw.get_recent_tweets()
    # print(len(users_json_array))
    db.set_users(users_json_array)
    # time = datetime.now()
    # return "users_json_array"
    return None

@app.get('/get_userlist')
def get_userlist():
    users_json_array=db.get_userlist()
    return users_json_array



# @app.get('/test')
# def json():
#     return "res"

