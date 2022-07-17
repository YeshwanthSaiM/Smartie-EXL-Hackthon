"""Smartie - A Smarter way of building AI Intelligent Bots
Admin API Collection : 
This script gives all required APIs that helps Smartie Admin do 
1. Build Universal Bot definition file
2. Conversion 
    Universal Bot Definition => Google DialogFlow
    Universal Bot Definition => AWS Lex
    Universal Bot Definition => Rasa
    Universal Bot Definition => Smartie Conversation Framework ( SCF )
    Universal Bot Definition => Kore AI ( raod map )
3. FAQ Engine
    Build FAQ engine
        From CSV files
        From PDF files
    Interact with FAQs
4. ML Recommendation Engine
5. OCR ( PDF/Image to Text )
6. BERT Summerization    
"""

# libraries
from './UniveralBotDefinition/conversion.py' import conversion 



# Universal bot definition
uni_path = 'UniveralBotDefinition/Universal Bot Definition.json'
with open(uni_path,'r') as f:
    uni = f.read()

DialogFlowBot = conversion.convertToDF(uni)

lexBot = conversion.convertToLex(uni)

