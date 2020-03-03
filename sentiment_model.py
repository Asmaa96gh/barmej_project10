import pickle
import json
import numpy as np  
'''
 the dataset used for training the model https://www.kaggle.com/bittlingmayer/amazonreviews
 only 100K rows have been used 

'''
#get the model and vectorizer files 
with open('model3.pickle', 'rb') as file:
    model = pickle.load(file)

with open('vectorizer3.pickle', 'rb') as file:
    vectorizer = pickle.load(file)

#clean texts , delete the stopwords,numbers and punctuation
def clean_text(text):
    import re
    text = re.sub(r"[^a-zA-Z]+", ' ', text)
    return text

#retrieve data from the other server's database by using requests.get(url) 
def get_all_data(max_count,page,sort_order):
    import requests
   # start with first index
    all_text=[]
    all_label=[]
    while page < 50000:

        try:
            payload = {'max_count': max_count, 'page': page ,'sort_order':sort_order}
            result =requests.get("http://127.0.0.1:3000/get_data", params=payload , headers={'Content-Type': 'application/json'})
            response=result.json()
            text_15=[]
            label_15=[]
            for i in range(len(response)):
                text=response[i]
                label=response[i][-1]
                text_15.append(text)
                label_15.append(label)
            all_text.extend(text_15)
            all_label.extend(label_15)
            page += 15 

        except Exception as error:
            print ("ERROR IN GET_TEXT FUNCTION")
            print ("Exception TYPE:", type(error))
     
    return all_text , all_label


all_text , all_label = get_all_data(15,1,'ASC') 

# get the total of positive or negative values in the database
def get_total(label):
    import requests
    try:
        payload = {'label_name': label}
        result = requests.get('http://127.0.0.1:3000/get_total_data_count',params=payload , headers={'Content-Type': 'application/json'})
        response=result.json()
        return response[0] 

    except Exception as error:
        print ("ERROR IN get_total FUNCTION")
        print ("Exception TYPE:", type(error))



#clean all texts 
for i, text in enumerate(all_text):
    all_text[i]=clean_text(all_text[i])


text_vector = vectorizer.transform(all_text)
#prediction process
ArrayOfPredictions = model.predict(text_vector)

# the number of positive and negative values from the model prodiction
PositiveInPredict = (ArrayOfPredictions==0).sum()
NegativeInPredict =(ArrayOfPredictions==1).sum()

positive=get_total("positive")
Negative=get_total("negative")
 

from sklearn.metrics import accuracy_score 
accuracy=accuracy_score(all_label, ArrayOfPredictions)

print("the total texts in database = 50000, \n the total retrieved data = ",len(all_text),"\n")
print(" the total of positive values in the database = ",positive , " \n And the total of negative values in the database = ",Negative)
print(" And the total of positive values in the model predictions = ",PositiveInPredict,
    "\n And the total of negative values in the model predictions = ",NegativeInPredict)
print("\n -------- \n")
print('the model accuracy',accuracy)





  

