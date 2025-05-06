import pandas as pd
# gensim 설치 필요
from gensim.models.word2vec import Word2Vec
import re
from collections import Counter

class Predict_name():
    def __init__(self,data,model):
        self.data=data
        self.DF=pd.DataFrame(data)
        self.word2vec=Word2Vec.load(model)
    def pred(self,pred_name,number:int=None):
        if number==None:
            number=5
        try:
            self.pred_name_list=[x for x in self.word2vec.wv.index_to_key if pred_name.lower() in x.lower()]
        except:
            self.pred_name_list=[]
        if len(self.pred_name_list)!=0:
        # self.pred_name=pred_name.lower()
            self.name=self.DF['name']
            total_match_list=[]
            for pred_name in self.pred_name_list:
                self.word_list=[x for x,y in self.word2vec.wv.most_similar(pred_name,topn=number)]
                match_list=[]
                for word in self.word_list:
                    match=self.DF.loc[self.name.apply(lambda x: True if word in x.lower() else False),'name'].tolist()
                    match_list.extend(match)
                total_match_list.extend(match_list)
            dict1=dict(Counter(total_match_list))
            name=list(dict(sorted(dict1.items(),key=lambda x:x[1],reverse=True)).keys())
            list1=[]
            for n in name:
                for idx,x in enumerate(self.data):
                    if n in x['name']:
                        list1.append(self.data[idx])
            if len(list1)<=5:
                return list1
            else:
                return list1[:5]     
        else:
            return '키워드 없음' 
# =================================================
# predict_name(path,word2vec.model)
# path 수정필요, word2vec 고정 
# =================================================   
# 실행코드 위치 -> __init__.py
# =================================================