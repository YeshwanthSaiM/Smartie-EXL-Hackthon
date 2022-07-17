# Libraries:

# extracting the pdf file
from tika import parser
# summarizing the text:
from gensim.summarization.summarizer import summarize

raw = parser.from_file('../Data/manual.pdf')

text = raw['content']

text_paragraphs = text.split('\n\n')

text_paragraphs_cleaned = [para for para in text_paragraphs if len(para) > 1]

def summarize_paragraph(para):
    try:
        return summarize(para)
    except:
        return para
text_paragraphs_summarized = [summarize_paragraph(para) for para in text_paragraphs_cleaned]

text_paragraphs_summarized_cleaned = [ para for para in text_paragraphs_summarized if len(para) > 1]

questions = [
" How much money do I need to collect to reinstate a policy?",
"Is there going to be a refund due to a policy change?",
"How would I change the information for the electronic payments on the website?",
"Can I change the payment plan and how much would the insured need to pay?",
"Why are the insured’s policies on different account numbers?",
"Insured’s policies are on the same account why are there separate invoices issued for each policy?",
"Can we get a reinstatement fee waived?",
"When will a refund be mailed?",
"What happened to my audit credit?",
"Agent asking how to retrieve copies of invoices.",
"Agent asking to have the electronic payments removed."]

from sklearn.feature_extraction.text import TfidfVectorizer

tfv = TfidfVectorizer(min_df = 1, stop_words = 'english')

tfv_paras = tfv.fit_transform(text_paragraphs_summarized_cleaned)

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

for question in questions:
    cosine_similarities = []
    question_vector = tfv.transform([question])
    for i in range(tfv_paras.shape[0]):
        cosine_similarities.append(cosine_similarity(tfv_paras[i], question_vector))
    ind = np.argmax(np.asarray(cosine_similarities))
    print("for question: ",question )
    print("The answer is: ",text_paragraphs_summarized_cleaned[ind])
    print('')
    print('')