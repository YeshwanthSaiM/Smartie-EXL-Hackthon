# Making entity recognition system:

# Loading the files from the entities folder
import os
data_root_path = "./Data/Entities"
filenames = os.listdir(data_root_path)


training = []
for filename in filenames:
    print(filename)
    with open(data_root_path + "/" + filename, 'r') as file:
        content = file.read()
        content = content.split('\n\n')
        training.extend(content)

training_x = []
for sent in training:
    if len(sent) == 3:
        training_x.append(((sent[0], sent[1]), sent[2] ))

training_x = []
for sent in training[:2]:
    temp = []
    for s in sent.split('\n'):
        sp = s.split('\t')
        if len(sp)  == 3:
            w,t,n = sp
            temp.append(((w,t), n))

    training_x.append(temp)

import string
from nltk.stem.snowball import SnowballStemmer

def features(tokens, index, history):
    """
    `tokens`  = a POS-tagged sentence [(w1, t1), ...]
    `index`   = the index of the token we want to extract features for
    `history` = the previous predicted IOB tags
    """
 
    # init the stemmer
    stemmer = SnowballStemmer('english')
 
    # Pad the sequence with placeholders
    tokens = [('[START2]', '[START2]'), ('[START1]', '[START1]')] + list(tokens) + [('[END1]', '[END1]'), ('[END2]', '[END2]')]
    history = ['[START2]', '[START1]'] + list(history)
 
    # shift the index with 2, to accommodate the padding
    index += 2
 
    word, pos = tokens[index]
    prevword, prevpos = tokens[index - 1]
    prevprevword, prevprevpos = tokens[index - 2]
    nextword, nextpos = tokens[index + 1]
    nextnextword, nextnextpos = tokens[index + 2]
    previob = history[index - 1]
    contains_dash = '-' in word
    contains_dot = '.' in word
    allascii = all([True for c in word if c in string.ascii_lowercase])
 
    allcaps = word == word.capitalize()
    capitalized = word[0] in string.ascii_uppercase
 
    prevallcaps = prevword == prevword.capitalize()
    prevcapitalized = prevword[0] in string.ascii_uppercase
 
    nextallcaps = prevword == prevword.capitalize()
    nextcapitalized = prevword[0] in string.ascii_uppercase
 
    return {
        'word': word,
        'lemma': stemmer.stem(word),
        'pos': pos,
        'all-ascii': allascii,
 
        'next-word': nextword,
        'next-lemma': stemmer.stem(nextword),
        'next-pos': nextpos,
 
        'next-next-word': nextnextword,
        'nextnextpos': nextnextpos,
 
        'prev-word': prevword,
        'prev-lemma': stemmer.stem(prevword),
        'prev-pos': prevpos,
 
        'prev-prev-word': prevprevword,
        'prev-prev-pos': prevprevpos,
 
        'prev-iob': previob,
 
        'contains-dash': contains_dash,
        'contains-dot': contains_dot,
 
        'all-caps': allcaps,
        'capitalized': capitalized,
 
        'prev-all-caps': prevallcaps,
        'prev-capitalized': prevcapitalized,
 
        'next-all-caps': nextallcaps,
        'next-capitalized': nextcapitalized,
    }


import pickle
from collections import Iterable
from nltk.tag import ClassifierBasedTagger
from nltk.chunk import ChunkParserI

class NamedEntityChunker(ChunkParserI):
    def __init__(self, train_sents, **kwargs):
        assert isinstance(train_sents, Iterable)
 
        self.feature_detector = features
        self.tagger = ClassifierBasedTagger(
            train=train_sents,
            feature_detector=features,
            **kwargs)
 
    def parse(self, tagged_sent):
        chunks = self.tagger.tag(tagged_sent)
 
        # Transform the result from [((w1, t1), iob1), ...] 
        # to the preferred list of triplets format [(w1, t1, iob1), ...]
        iob_triplets = [(w, t, c) for ((w, t), c) in chunks]
 
        # Transform the list of triplets to nltk.Tree format
        return conlltags2tree(iob_triplets)
    
# Training with the data
chunker = NamedEntityChunker(training_x)


# Checking with sample utt:
from nltk import pos_tag, word_tokenize
from nltk.chunk import conlltags2tree, tree2conlltags
print(chunker.parse(pos_tag(word_tokenize("what is the principal place of business of ABBOTT INDIA LIMITED in Andhra Pradesh"))))


# Saving the model:

model = chunker.tagger 
save_classifier = open("./Models/EntityRecognizer.pickle","wb")
pickle.dump(model, save_classifier)
save_classifier.close()


# Loading the model:

new_model_file = open("./Models/EntityRecognizer.pickle","rb")
new_model = pickle.load(new_model_file)
new_model_file.close()

new_model.tag(pos_tag(word_tokenize("what is the principal place of business of ABBOTT INDIA LIMITED in Andhra Pradesh")))






