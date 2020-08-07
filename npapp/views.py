from django.shortcuts import render

import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
warnings.filterwarnings('ignore')

import urllib.request
from inscriptis import get_text

url = "https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/symptoms-causes/syc-20354521"
html = urllib.request.urlopen(url).read().decode('utf-8')

text = get_text(html)

sentence_list=nltk.sent_tokenize(text)


def fun(request):
    return render(request,'display.html')


def fun2(request):
    return render(request,'chat.html')
def fun3(request):
    exit_list=['bye','see u later','exit','thanks']
    while(True):
        if request.method=='POST':
            a=request.POST['exp']
            user_input=a
            if user_input.lower() in exit_list:
                return render(request,'exit.html',{'bye':'bye i will chart u later'})
            else:
                #print('hi')
                if bot_response(user_input) != None:
                    d=bot_response(user_input)
                    #print(d)
                    return render(request,'chat.html',{'data':d})










def greetings_response(text):
    text=text.lower()

    #bot greetings response
 
    bot_greetings=['howdy','hi','hey','hello','holo']
    #user greetings
    user_greetings=['hi','hello','holo','howdy']

    for word in text.split():
        if word in user_greetings:
            return random.choice(bot_greetings)



def bot_response(user_input):
    user_input=user_input.lower()
    sentence_list.append(user_input)
    bot_response=''
    cm=CountVectorizer().fit_transform(sentence_list)
    similarity_scores=cosine_similarity(cm[-1],cm)
    similarity_scores_list=similarity_scores.flatten()
    index=index_sort(similarity_scores_list)
    index=index[1:]
    response_flag=0

    j=0

    for i in range(len(index)):
        if similarity_scores_list[index[i]] > 0.0:
            bot_response=bot_response+' '+sentence_list[index[i]]
            response_flag=1
            j=j+1
        if j>2:
            break
    if response_flag == 0:
        bot_response=bot_response+' '+"sorry!,Idon't understant."
    
    sentence_list.remove(user_input)
    
    return bot_response



def index_sort(list_var):
   length=len(list_var)
   list_index=list(range(0,length))
   x=list_var
   for i in range(length):
       for j in range(length):
           if x[list_index[i]] > x[list_index[j]]:
                                   temp=list_index[i]
                                   list_index[i]=list_index[j]
                                   list_index[j]=temp
   return list_index



