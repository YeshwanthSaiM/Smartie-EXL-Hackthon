# Making data for NER system:

# pos tagger
from nltk import word_tokenize, pos_tag

sample = "how do i edit my M T P by upload Customers"

# pos tagget
print(pos_tag(word_tokenize(sample)))


# Identity key words tagger:
# Type : keyword 


# Identify intention


# format: 
"""
Afghan	JJ	N[nom]/N[nom]	afghan	O
[word]   [Noun] [subclass of noun] [type] [IOB tag]
"""

# we need
"""
1. sample utterance patter
2. keywords to fill
3. Get the index of those filled keywords and mark with I tag
4. generate the format for each word in .tag files
"""

utterances = [
'{prefix} {location} of {company} in {state}',
'{prefix} {gst} of {company} in {state}',
'{prefix} {location} of {company}',
'{prefix} {gst} of {company} ',
'{prefix} {location} in {state}',
'{prefix} {gst} in {state}',
'{prefix} {location}',
'{prefix} {gst}']


entity_values = {'prefix' : ['what is the', 'can you tell me', 'I want to know'],
'gst' : ['GST', 'GSTIN', 'goods and services tax', 'GST number', 'GST no'],
'location' : ['principal place of business', 'main place of business', 'business address','address'],
'company': ['ABBOTT INDIA LIMITED', 'ail', 'ABBOTT HEALTHCARE PRIVATE LIMITED', 'ahpl', 'AHPL', 'AIL'],
'state' : ['Gujarat', 'Maharashtra', 'Chattisgarh', 
             'Uttar Pradesh', 'Delhi', 'Kerala','Tamil Nadu',
             'Karnataka','Telangana',
            'Andhra Pradesh','GOA','Uttarakhand','Rajasthan', 
             'Punjab','Haryana','Himachal Pradesh', 
             'Madhya Pradesh', 'Jammu & Kashmir', 'Puducherry', 
             'West Bengal','Bihar', 'Jharkhand', 'Assam', 'Odisha']
         }

# the above are for GST Domain getgstinfo Intent

def extract(s):
    start = s.find('{')
    if start == -1:
        # No opening bracket found. Should this be an error?
        return ''
      # skip the bracket, move to the next character
    end = s.find('}', start)
    if end == -1:
        # No closing bracket found after the opening bracket.
        # Should this be an error instead?
        return s[start:]
    else:
        return s[start:end+1]

def helper(string):
    new_string = ''
    boolean = True
    for c in string:
        if c == '{':
            boolean = False
            new_string += c
        if c == '}':
            boolean = True
            pass
        if boolean == True:
            new_string += c
    return new_string

import itertools
def getCombinations(json):
    #print('Started combinations')
    keys, values = zip(*json.items())
    for v in itertools.product(*values):
        yield dict(zip(keys, v))
    return 'End'

import re
utt = utterances[0]
utt_bare = helper(utt)
regex = re.compile('[^a-zA-Z]')
entities =  [regex.sub('', entity) for entity in re.findall(r'\{(.*?)\}', utt)]

temp_values = {}
for ent in entities:
    temp_values[ent] = entity_values[ent]
    
comb_gen = getCombinations(temp_values)
comb = ''

i = 0
file_index = 0
utt_index = 0
file_root_path = "D:\\Projects\\ConversationaFramework\\Others\\nerdata"

while(comb != 'End') and i < 100:
    i += 1
    try:
        print('For file number', file_index)
        print('For utterance index', utt_index)
        utt_index += 1
        comb = next(comb_gen)
        vals = comb.values()
        utt = utt_bare.format(*vals)
        print("The filled utterence:")
        print(utt)
        
        # breaking into words:
        utt_bare_words = word_tokenize(utt_bare)
        utt_words = word_tokenize(utt)
        print('Utt bare words', utt_bare_words)
        print('Filled words', utt_words)
        
        with open(file_root_path +"\\"+ str(file_index) + '.txt', 'a+') as file:
            #file.write('Hello')
            for word in utt_words:
                if word in utt_bare_words:
                    t = str(word+"\t"+ pos_tag([word])[0][1]+"\t"+ word.lower() + '\t'+'O')
                    file.write(t)
                    file.write("\n")
                else:
                    t = str(word+ '\t'+ pos_tag([word])[0][1]+'\t'+'keyword'+'\t'+ 'I')
                    file.write(t)
                    file.write("\n")
            file.write('\n')
            file.write('\n')

        if utt_index == 20:
            file_index += 1
            utt_index = 0
    except:
        comb = ''
    
    



with open(file_root_path +"\\"+ str(file_index) + '.txt', 'w') as file:
    file.write("hello")