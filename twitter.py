import time
import tweepy
import config
import neologdn
import emoji,re
from janome.tokenizer import Tokenizer
import collections


# API情報を記入

BEARER_TOKEN        = config.BEARER_TOKEN
API_KEY             = config.API_KEY
API_SECRET          = config.API_SECRET
ACCESS_TOKEN        = config.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = config.ACCESS_TOKEN_SECRET

# 形態素解析用
t = Tokenizer()

def ClientInfo():
    client = tweepy.Client(bearer_token    = BEARER_TOKEN,
                           consumer_key    = API_KEY,
                           consumer_secret = API_SECRET,
                           access_token    = ACCESS_TOKEN,
                           access_token_secret = ACCESS_TOKEN_SECRET,
                          )
    
    return client
    


class get_twitter():
    def __init__(self) -> None:
        try:
            self.__api = ClientInfo()
        except:
            print('twitter initialize error')
    


    # author_idからユーザーの情報を取得する
    def get_user_name(self,author_id):
        user_data = self.__api.get_user(id=author_id) 
        name = user_data[0]["name"]
        user_name = user_data[0]["username"]
        user_link = "https://twitter.com/"+ user_name
        return name,user_name,user_link

    # blockしているユーザーのリストを取得
    def get_users_blocked(self):
        res = self.__api.get_blocked()
        return res

    # 直近7週間のキーワードが含まれたツイートを取得
    def get_recent_tweets(self):
        # print(keyword_list)
        
        res_list,next_token =self.get_tweets()
        i= 1
        while next_token != "":
            if next_token== "Nothing":
                print("break!!")
                break
            else:
                try:
                    loop_list,next_token=self.get_tweets(tw_next_token=next_token)
                    for obj in loop_list:
                        res_list.append(obj)

                    print(res_list)
                    i+=1
                    print(f"===={i}回目のリクエスト=====")
                except Exception as e:
                    print(e)
                    break

        return res_list
        

    def get_tweets(self,tw_next_token:str=""):
        NEXT_TOKEN:str
        tw_list:list = []
        keyword_list = ["高山宏"]
        minus_keyword =["フォルマリズム"]
        query_keyword = "芸術"
        
        
        for k in keyword_list:
            query_keyword = query_keyword + " OR " + k
            query = f"{query_keyword} -is:retweet"

        if tw_next_token == "":
            res = self.__api.search_recent_tweets(query,max_results=100,expansions="author_id",tweet_fields="created_at" )
            try:
                for r in res[0]:
                    score = self.score(r["text"],keyword_list,minus_keyword)
                    tweets_json ={
                        u"created_at": r['created_at'],
                        u"score":score,
                        u"user_id": r['author_id'],
                        u"tweet_id": r['id'],
                        u"text": r['text'],
                    }
                    tw_list.append(tweets_json)
                # print("この回の取得ツイート")
                # print(len(res[0]))
                # print("全体の取得ツイート")
                # print(len(tw_list))
                
                if "next_token" not in res[-1]: 
                    NEXT_TOKEN = "Nothing"
                else:
                    NEXT_TOKEN = res[-1]["next_token"]
            
                tw_list = self.add_userid(tw_list)
                return tw_list, NEXT_TOKEN
                
         

            except tweepy.errors.TooManyRequests as e: 
                print("######")
                print("多すぎ")
                print(e)
                print("######")
                time.sleep(900)
                return tw_list, NEXT_TOKEN

            except Exception as e:
                print("######")
                print(e)
                print("######")
                raise Exception(f"Unknown error:{e}")
                
        elif tw_next_token == "Nothing":
            print("Nothing")
            NEXT_TOKEN = str(tw_next_token)
            return tw_list,NEXT_TOKEN
        
        else:
            res = self.__api.search_recent_tweets(query,max_results=100,next_token=tw_next_token,expansions="author_id",tweet_fields="created_at" )
            try:       
                if "next_token" not in res[-1]: 
                    NEXT_TOKEN = "Nothing"
                else:
                    NEXT_TOKEN = res[-1]["next_token"]

                for r in res[0]:
                    score = self.score(r["text"],keyword_list,minus_keyword)
                    tweets_json ={
                        u"created_at": r['created_at'],
                        u"score":score,
                        # status is union of ["not_sent","sent","achieve","failure"]
                        u"status":"not_sent",
                        u"user_id": r['author_id'],
                        u"tweet_id": r['id'],
                        u"text": r['text'],
                    }
                    tw_list.append(tweets_json)
                    

                # print(res[0])
                # print(NEXT_TOKEN)
                # print(res_list)
                
                # print(f"===={i}回目=====")
                tw_list = self.add_userid(tw_list)
                return tw_list,NEXT_TOKEN
            except Exception as e:
                print(e)

               

    def add_userid(self,tw_list:list):   
        for tw in tw_list:
            # print(tw)
            # print(type(tw))
            # print(tw["author_id"])
            user_id = tw["user_id"]
            NAME, USER_ID, TWEET = self.get_user_name(user_id)
            author_data={"name":NAME,"user_name":USER_ID,"tweet_link":TWEET,}
            tw.update(author_data)
            
            # print(tw)
        # print(res_list)
        # print(NEXT_TOKEN)
        return tw_list


    def score(self,process_text,plus_words,minus_words):
        text = process_text
        # テキストの正規化、絵文字除去、桁数の除去、URLの除去、数字を揃える
        # これを参考に→https://ohke.hateblo.jp/entry/2019/02/09/141500
        normalized_text = neologdn.normalize(text)
        text_without_url = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', '', normalized_text)
        text_without_emoji = ''.join(['' if c in emoji.UNICODE_EMOJI else c for c in text_without_url])
        tmp = re.sub(r'(\d)([,.])(\d+)', r'\1\3', text_without_emoji)
        text_replaced_number = re.sub(r'\d+', '0', tmp)
        tmp = re.sub(r'[!-/:-@[-`{-~]', r' ', text_replaced_number)
        text_removed_symbol = re.sub(u'[■-♯]', ' ', tmp)

        processed_text = text_removed_symbol
        # for token in t.tokenize(processed_text):
        #     print(token)

        data =t.tokenize(processed_text, wakati=True)
        data = collections.Counter(data)
        score = 10
        for p in plus_words:
            score = score + data[p]
            print("プラス＝＝＝＝")
            print(p)
            print(data[p])
            print(score)
        for m in minus_words:
            score = score + data[m]
            print("マイナス＝＝＝＝")
            print(m)
            print(data[m])
            print(score)
        return score