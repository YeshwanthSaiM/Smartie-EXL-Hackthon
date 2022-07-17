# Libraries:

# summarizing the text:
from gensim.summarization.summarizer import summarize

def summarize_paragraph(para):
    try:
        return summarize(para)
    except:
        return para

