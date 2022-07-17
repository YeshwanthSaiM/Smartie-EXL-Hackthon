"""
This project is a conversational framework built using machine learning
This is made following the instructions of the Mindmeld conversational 
Framework
"""


# Libraries:
import os
from sklearn.preprocessing import LabelEncoder
import numpy as np
import nltk
import re
import matplotlib.pyplot as plt    
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from joblib import dump, load
# Getting to the data:

data_root_path =  "../Data"
os.listdir(data_root_path)


# Making a domain classification:

# flag used whether to train the domain classifier or not
train_flag = False


# Train Domain classifier:

domains = os.listdir(data_root_path + "/Domains")
domains

# Make classifcation only when num of domains are > 1:
if len(domains) > 1:
    train_flag = True

# Extracting data from Domain classification
x = []
y = []

for domain in domains:
    intent_folders = os.listdir(data_root_path + "/Domains"+"/"+ domain)
    for intent_folder in intent_folders:
        text_files = os.listdir(data_root_path + "/Domains"+"/"+ domain + "/"+ intent_folder)
        for text_file in text_files:
            with open(data_root_path + "/Domains"+"/"+ domain + "/"+ intent_folder + "/"+text_file, 'r') as file:
                content = file.readlines()
                x.extend(content)
                y.extend([domain] * len(content))

# Data processing for x and y
# label encoding for y
lb = LabelEncoder()
y = lb.fit_transform(y)

# Shuffling the indices for x and y
indices = np.arange(len(x))
np.random.shuffle(indices)

x = np.array(x)[indices]
y = y[indices]

def processText(sent):
    """
    This function is to apply all text processing steps for sentence
    """
    # removing '\n' from sentence
    sent = sent.replace('\n','')
    sent = re.sub('[^A-Z a-z0-9]+', '', sent)
    return sent

x = [ processText(sent) for sent in x]

# Word tokenizing x
x = [ nltk.word_tokenize(sent) for sent in x]

# Converting words to their vectors using word2vec models 
# Trying with gensim:
from gensim.models import Word2Vec
# train model
model = Word2Vec(x, min_count=1)
print(model)
words = list(model.wv.vocab)
# saving the model:
model_path = "../Models/Word2Vec"
model.save(model_path + '/model.bin')
# load model
Word2VecModel = Word2Vec.load(model_path + '/model.bin')
print(Word2VecModel)



# finding a threshold length of sentence to pad or trim:

x_lens = [len(sent) for sent in x]
threshold = int(np.median(np.array(x_lens)))

plt.boxplot(x_lens)
plt.title("The Box plot of lens of the reviews")
plt.show()


# converting each word with word vectors
x = [ [Word2VecModel[word] for word in sent ] for sent in x]
x = np.array([ np.array(sent) for sent in x] )               

# padding and trimming the sentences with keras
np.zeros((2,100), dtype=np.float)
def padAndTrim(arr, threshold = threshold):
    if len(arr) < threshold:
        arr = np.append(arr, np.zeros((int(threshold) - len(arr),100), dtype=np.float), axis = 0)
    else:
        arr = arr[:int(threshold)]
    return arr
x = [padAndTrim(arr) for arr in x]

# Converting to arrays:
x = np.array(x)
y = np.array(y)

# sklearn models only can handle 2D data
x_reshaped = x.reshape((x.shape[0], x.shape[1] * x.shape[2]))

# Making models:
# 1. Logistic 
# 2. Random Forest

# Logistic model with RandomizedSearchCV

estimator = LogisticRegression()
param_dist = {
        'solver' : ['newton-cg', 'lbfgs', 'saga']}

random_search_logistic = RandomizedSearchCV(estimator = estimator,
                                            param_distributions = param_dist,
                                            cv=4,
                                            n_iter = 3)

random_search_logistic.fit(x_reshaped, y)



# Random Forest with RandomizedSearchCV
estimator = RandomForestClassifier()
param_dist = {
        'n_estimators': [5,10,15,20],
        'criterion': ['gini', 'entropy'], 
        'max_depth': [5,10,15]}

random_search_rf= RandomizedSearchCV(estimator = estimator,
                                            param_distributions = param_dist,
                                            cv=4,
                                            n_iter = 10)
random_search_rf.fit(x_reshaped, y)

if random_search_logistic.best_score_ > random_search_rf.best_score_:
    model = random_search_logistic.best_estimator_
else:
    model = random_search_rf.best_estimator_

# Saving the model
dump(model, "../Models/DomainClassifier/DomainClassifier.joblib")


loaded_model = load( "../Models/DomainClassifier/DomainClassifier.joblib")

classes_dict = {}
for i in range(len(lb.classes_)):
    classes_dict[i] = lb.classes_[i]

import json
with open("../Models/DomainClassifier/DomainClassifier.json", 'w') as fp:
    json.dump(classes_dict, fp)

# Making prediction for a sentence for Domain classification
        
domain_classifier = load( "../Models/DomainClassifier/DomainClassifier.joblib")
 
with open("../Models/DomainClassifier/DomainClassifier.json",encoding='utf', errors='ignore') as json_data:
    domain_classes = json.load(json_data, strict=False)

# Making a prediction:
def DomainPrediction(sent):
    """
    This is to make prediction for the domain:
    """
    sent = "what is the principal place of business of ABBOTT INDIA LIMITED in Gujarat"
    sent = processText(sent)
    sent_words = nltk.word_tokenize(sent)

    sent_vec = []
    for word in sent_words:
        try:
            sent_vec.append(Word2VecModel[word])
        except:
            pass
    sent_vec = padAndTrim(sent_vec)
    sent_vec = np.array(sent_vec)
    sent_vec_reshaped = sent_vec.reshape((1, sent_vec.shape[0] * sent_vec.shape[1]))
    sent_class = domain_classes[str(domain_classifier.predict(sent_vec_reshaped)[0])]
    return sent_class

# example : A single instance:
sent = "what is the principal place of business of ABBOTT INDIA LIMITED in Gujarat"
sent = processText(sent)

sent_words = nltk.word_tokenize(sent)
sent_words

# converting to vec
sent_vec = []
for word in sent_words:
    try:
        sent_vec.append(Word2VecModel[word])
    except:
        pass

sent_vec = padAndTrim(sent_vec)

sent_vec = np.array(sent_vec)

sent_vec_reshaped = sent_vec.reshape((1, sent_vec.shape[0] * sent_vec.shape[1]))



sent_class = domain_classes[str(domain_classifier.predict(sent_vec_reshaped)[0])]
sent_class

