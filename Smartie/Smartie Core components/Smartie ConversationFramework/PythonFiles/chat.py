# This file to load all the trained models and initiate the chat

"""
procedure:
    Step1: query
    
    Step2: processing the query
        word tokenize
        padding
        Word2vec model
        
    Step3: Domain Classification
        Predicts the Domain
    
    Step4: Based on the domain
        Intent classification
    
    Step5: Entity recognition
        
    Step 6: Reply
        For now the entity are replied back
        But for future Knowledge base is added
"""

import numpy as np
query = "what is the principal place of business of ail in Maharashtra"

# Preprocessing for the query:
def padAndTrim(arr, threshold ):
    if len(arr) < threshold:
        arr = np.append(arr, np.zeros((int(threshold) - len(arr),100), dtype=np.float), axis = 0)
    else:
        arr = arr[:int(threshold)]
    return arr
import re
def processText(sent):
    """
    This function is to apply all text processing steps for sentence
    """
    # removing '\n' from sentence
    sent = sent.replace('\n','')
    sent = re.sub('[^A-Z a-z0-9]+', '', sent)
    return sent

query_processed = processText(query)

import nltk
query_words = nltk.word_tokenize(query)

from gensim.models import Word2Vec
Word2VecModel = Word2Vec.load('../Models/Word2Vec/model.bin')
#print(Word2VecModel)


# converting to vec
query_vec = []
for word in query_words:
    try:
        query_vec.append(Word2VecModel[word])
    except:
        pass
query_vec_padded = padAndTrim(query_vec, 11)

import numpy as np
query_vec_padded = np.array(query_vec_padded)

query_vec_reshaped = query_vec_padded.reshape((1, query_vec_padded.shape[0] * query_vec_padded.shape[1]))

from joblib import load
import json
# Loading the model and json:
domain_classifier = load( "../Models/DomainClassifier/DomainClassifier.joblib")
 
with open("../Models/DomainClassifier/DomainClassifier.json",encoding='utf', errors='ignore') as json_data:
    domain_classes = json.load(json_data, strict=False)


predicted_domain= domain_classes[str(domain_classifier.predict(query_vec_reshaped)[0])]



# With help of this Domain classification 
# Making the Intent Classification:

# Loading the Intent classification model:

intent_classifier = load( "../Models/IntentClassifier/"+predicted_domain+"/IntentClassifier.joblib")
with open("../Models/IntentClassifier/"+predicted_domain+"/IntentClassifier.json",encoding='utf', errors='ignore') as json_data:
    intent_classes = json.load(json_data, strict=False)


query_vec_padded = padAndTrim(query_vec, 9)
query_vec_padded = np.array(query_vec_padded)
query_vec_reshaped = query_vec_padded.reshape((1, query_vec_padded.shape[0] * query_vec_padded.shape[1]))
 
intent_predicted = intent_classes[str(intent_classifier.predict(query_vec_reshaped)[0])]



# Extracting the entities:
# Loading the model:
import pickle
from nltk import pos_tag, word_tokenize
if __name__=='__main__':
                                                        
    with open("./Models/EntityRecognizer.pickle","rb") as m:
        new_model = pickle.load(m)
    #new_model_file.close()



import pickle

class CustomUnpickler(pickle.Unpickler):

    def find_class(self, module, name):
        if name == 'Manager':
            from settings import Manager
            return Manager
        return super().find_class(module, name)

new_model_file = open("../Models/TempEntityRecognizer.pkl", 'rb')
new_model = pickle.load(new_model_file)
new_model_file.close()

new_model.tag(pos_tag(word_tokenize(query)))


# loading with joblib
from joblib import load
new_model = load("../Models/JoblibEntityRecognizer.joblib")



