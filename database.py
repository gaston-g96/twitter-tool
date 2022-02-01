from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import config

# Use a service account
current_dir = os.getcwd()
account = current_dir+'/firebase.json'
fb_account = config.FIREBASE_KEY

class firebase_client():
    def __init__(self):
        if not firebase_admin._apps:
            try:
                cred = credentials.Certificate(str(account))
                firebase_admin.initialize_app(cred)
                self.__db = firestore.client()
            except Exception as e:
                raise f"This is firebase initialize error : {e}"
                

    def test(self):
        res = fb_account
        # print(type(str(fb_account)))
        # print(type(account))
        return res      

    

    def set_users(self,users_json_array:list):
        users_list = users_json_array
        i = 1
        for user in users_list:
            # print(user)
            # print(type(user))
            i += 1
            text=f"{i}回目"
            print(text)
            doc_ref= self.__db.collection(u'users').document(user['name'])
            doc = doc_ref.get()
            #現在のスコア
            # if doc.exists:
            #     # アベレージの値を追加し、個数で割る
            #     print(doc.to_dict())
            # else:
            #     # セットするだけ
            #     print("set")

            try:
                doc = doc_ref.get()
                time_tweet = user['created_at']
                if doc.exists:
                    # average_scoreを更新
                    average_score_now = doc.to_dict()["average_score"]
                    tweet_length=len(doc.to_dict())-1
                    average_score_updated = average_score_now / tweet_length

                    doc_ref.update({
                                    'average_score':average_score_updated ,
                                    'tweets':{
                                            u'time_tweet':f'{time_tweet}',
                                            u'user_id': user['user_id'],
                                            u'score':user['score'],
                                            u'user_name': user['user_name'],
                                            u'text': user['text'],
                                            u'tweet_link': user['tweet_link'],
                                            u'_updatedAt': firestore.SERVER_TIMESTAMP,
                                        } 
                    })
                else:
                    doc_ref.set({   
                                   'average_score':user['score'],
                                   '_createdAt':firestore.SERVER_TIMESTAMP,
                                   'tweets':{
                                        
                                            u'time_tweet':f'{time_tweet}',
                                            u'user_id': user['user_id'],
                                            u'score':user['score'],
                                            u'user_name': user['user_name'],
                                            u'text': user['text'],
                                            u'tweet_link': user['tweet_link'],
                                            u'_updatedAt': firestore.SERVER_TIMESTAMP,
                                        
                                   }
                                   
                    })
            

            except Exception as e:
                print("Can not set to Firestore")
                print(e)               
        return None

    def get_userlist(self):
        users_array =  []
        docs = self.__db.collection(u'users').order_by(u'average_score', direction=firestore.Query.DESCENDING).stream()
        for doc in docs:
            try:
                res = doc.to_dict()
                # print(res["average_score"])
                users_array.append(res)
            except Exception as e:
                print("unknown error")
      
        return users_array


