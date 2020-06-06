import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes, svm
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
import pickle
import spacy
import pandas as pd
import numpy as np
import sys
from collections import defaultdict
import re
nlp = spacy.load("ComprehendMedModel/")
with open('comprehend_assets/Encoder.pickle', 'rb') as handle:
    Encoder = pickle.load(handle)
with open('comprehend_assets/Tfidf_vect.pickle', 'rb') as handle:
    Tfidf_vect = pickle.load(handle)
with open('comprehend_assets/Naive.pickle', 'rb') as handle:
    Naive = pickle.load(handle)
with open('dict4.pickle', 'rb') as handle:
    dict4 = pickle.load(handle)
df3 = pd.read_excel('input_output_frequenct.xlsx')
def prescription_translate_description(text):
    input = text
    predict_df = pd.DataFrame()
    input_copy = [[input]]
    predict_df = pd.DataFrame.from_records(input_copy , columns=['input'])
    predict_df['input'] = [entry.lower() for entry in predict_df['input']]
    predict_df['input']= [word_tokenize(entry) for entry in predict_df['input']]
    predict_df['input']= predict_df['input'].astype(str)
    temp_slot = Tfidf_vect.transform(predict_df['input'])
    pre = Naive.predict(temp_slot)
    first_slot = Encoder.inverse_transform(pre)
    predicted=[]
    for i in range(len(predict_df)):
        doc=nlp(str(input))
        str_temp=""
        str_temp_text=""
        for j in doc.ents:
            str_temp+=j.label_+", "
            str_temp_text+=j.text+", "
        str_temp=str_temp[:-2]
        str_temp_text=str_temp_text[:-2]
        if len(str_temp)==0:
            predicted.append(predict_df['input'][i])
            continue
        str1=first_slot[i]+" "
        tempo=[]
        try:
            for j in dict4[str_temp].split(", "):
                count=0
                temp=0
                flag=0
                tempo.append(j)
                for k in tempo:
                    if j==k:
                        flag+=1
            for k in str_temp.split(", "):
                if j==k:
                    if count+1>=flag:
                        temp=count
                        break
                count+=1
            flag=0
            for k in range(len(df3)):
                if df3['input'][k]==str_temp_text.split(", ")[temp]:
                    str1+=df3['output'][k]+" "
                    flag=1
                    break
            if flag==0:
                str1+=str_temp_text.split(", ")[temp]+" "
            predicted.append(str1[:-1])
        except:
            for j in str_temp_text.split(", "):
                flag=0
                for k in range(len(df3)):
                    if df3['input'][k]==j:
                        str1+=df3['output'][k]+" "
                        flag=1
                        break
            if flag==0:
                str1+=j+" "
            predicted.append(str1[:-1])
    return predicted[0]

if __name__ == '__main__':
    predicted = prescription_translate_description(sys.argv[1])
    print(predicted)

