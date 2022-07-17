# This is for intent classification 
# For each domain their should be an intent classification:


from sklearn.preprocessing import LabelEncoder
import numpy as np
import re
import nltk
from gensim.models import Word2Vec
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from joblib import dump, load

# Extracting Domains:
import os
domains = os.listdir("../Data/Domains")
domains

# Some helper functions:
def processText(sent):
    """
    This function is to apply all text processing steps for sentence
    """
    # removing '\n' from sentence
    sent = sent.replace('\n','')
    sent = re.sub('[^A-Z a-z0-9]+', '', sent)
    return sent

def padAndTrim(arr, threshold):
    if len(arr) < threshold:
        arr = np.append(arr, np.zeros((int(threshold) - len(arr),100), dtype=np.float), axis = 0)
    else:
        arr = arr[:int(threshold)]
    return arr

for domain in domains:
    #
    print("For domain ", domain)
    # extracting the number os intents in each domain:
    intents = os.listdir("../Data/Domains/"+ domain+"/Intents")
    print(intents)
    
    # Domain clasifiation is only needed when there are more than one intent
    
    intent_train = False
    if len(intents) > 1:
        intent_train = True
        
   
    def train_intent_classifier():
        # extracting the data for all the intents in the domain 
        x = []
        y = []
        for intent in intents:
            filenames = os.listdir("../Data/Domains/"+ domain+"/Intents/"+ intent)
            for filename in filenames:
                with open("../Data/Domains/"+ domain+"/Intents/"+ intent+"/"+filename, 'r') as file:
                    content = file.readlines()
                    x.extend(content)
                    y.extend([intent]*len(content))
                    
        # Data processing for x and y
        # label encoding for y
        lb = LabelEncoder()
        y = lb.fit_transform(y)
        
        # Shuffling the indices for x and y
        indices = np.arange(len(x))
        np.random.shuffle(indices)
        
        x = np.array(x)[indices]
        y = y[indices]
        
        x = [ processText(sent) for sent in x]
        # Word tokenizing x
        x = [ nltk.word_tokenize(sent) for sent in x]
        
        
        # Loading word2vec gensim model:
        Word2VecModel = Word2Vec.load('../Models/Word2Vec/model.bin')
        Word2VecModel = Word2Vec(x, min_count=1)
        
        x_lens = [len(sent) for sent in x]
        threshold = int(np.median(np.array(x_lens)))
        
        x = [ [Word2VecModel[word] for word in sent ] for sent in x]
        x = np.array([ np.array(sent) for sent in x] ) 
        
        x = [padAndTrim(arr,threshold = threshold) for arr in x]
        
        # Converting to arrays:
        x = np.array(x)
        y = np.array(y)
        
        # sklearn models only can handle 2D data
        x_reshaped = x.reshape((x.shape[0], x.shape[1] * x.shape[2]))
        
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
        dump(model, "../Models/IntentClassifier/"+domain+"/IntentClassifier.joblib")
        
        classes_dict = {}
        for i in range(len(lb.classes_)):
            classes_dict[i] = lb.classes_[i]
        
        import json
        with open("../Models/IntentClassifier/"+domain+"/IntentClassifier.json", 'w') as fp:
            json.dump(classes_dict, fp)
            
    if intent_train == True:
        train_intent_classifier()
        print("Training completed")
        
        