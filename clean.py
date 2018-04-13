import nltk
#nltk.download()
import os
import random
import codecs
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import _pickle as cPickle
import string
import re
from gensim import corpora
from operator import itemgetter
import pandas as pd
def rem_ascii(s):
    return "".join([c for c in s if ord(c) < 128 ])


def clean(doc):
    doc_ascii = rem_ascii(doc)
    doc_ascii = re.sub(r"http\S+"," ",doc_ascii)
    stop_free = " ".join([i for i in doc_ascii.lower().split() if i not in stop])
    p_free  = ''.join([ch for ch in stop_free if ch not in exclude])
    normalized = " ".join([lemma.lemmatize(word) for word in p_free.split()])
    #print(nltk.tag.pos_tag(nltk.word_tokenize(normalized)))
    normalized = " ".join(word for word, tag in nltk.tag.pos_tag(nltk.word_tokenize(normalized)) if tag != 'NNP' and tag != 'NNPS')
    x = normalized.split()
    y = [s for s in x if len(s) > 2]
    return y


corpus_path = "D:\\Unfound\\reviews_data\\"
article_paths = [os.path.join(corpus_path,p) for p in os.listdir(corpus_path) if p.endswith("txt")]

# Read contents of all the articles in a list "doc_complete"
doc_complete = []
for path in article_paths:
    fp = codecs.open(path,'r','utf-8')
    doc_content = fp.read()
    doc_complete.append(doc_content)  

# Randomly sample 70000 articles from the corpus created from wiki_parser.py      
docs_all = random.sample(doc_complete, 100)
docs = open("reviews.pkl",'wb')
cPickle.dump(docs_all,docs)

# Use 60000 articles for training.
docs_train = docs_all[:70]

# Cleaning all the 60,000 simplewiki articles
stop = set(stopwords.words('english'))
exclude = set(string.punctuation) 
lemma = WordNetLemmatizer()
doc_clean = [clean(doc) for doc in docs_train]


# Creating term dictionary of corpus, where each unique term is assigned an index. 
dictionary = corpora.Dictionary(doc_clean)

# Filter terms which occurs in less than 4 articles & more than 40% of the articles 
dictionary.filter_extremes(no_below=10)
corpus = [dictionary.doc2bow(sent) for sent in doc_clean]
vocab = list(dictionary.values()) #list of terms in the dictionary
vocab_tf = [dict(i) for i in corpus]
vocab_tf = list(pd.DataFrame(vocab_tf).sum(axis=0))
# List of few words which are removed from dictionary as they are content neutral
stoplist = set('also singh sharma salman khan nice great important bhai shahurkh good bad awesome best worse worst better iamsrk film filmmaker anyone everyone use make break people 0 reviewer reviews know many call include part find become like mean often different \
               usually take brilliant him her city town village done music cast you me meetu us her kunal singh kapoor kumar khanna experience usual despite wonderful perhaps almost problem never when come give well get since type list say change see refer actually iii \
               aisne kinds pas ask would way something need things want every str'.split())
stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
dictionary.filter_tokens(stop_ids)

doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

from gensim.models.ldamodel import LdaModel as Lda
# Creating the object for LDA model using gensim library & Training LDA model on the document term matrix.
ldamodel = Lda(doc_term_matrix, num_topics=10, id2word = dictionary, passes=50, iterations=100)


# Print all the 50 topics
for i,topic in enumerate(ldamodel.print_topics(num_topics=10, num_words=15)):
   words = topic[1].split("+")
   print(words)
   

def cluster_similar_documents(corpus, dirname):
    clean_docs = [clean(doc) for doc in corpus]
    test_term = [ldamodel.id2word.doc2bow(doc) for doc in clean_docs]
    doc_topics = ldamodel.get_document_topics(test_term, minimum_probability=0.10)    
    for k,topics in enumerate(doc_topics):        
        if topics:
            topics.sort(key = itemgetter(1), reverse=True)
            dir_name = dirname + "/" + str(topics[0][0])           
            file_name = dir_name + "/" + str(k) + ".txt"
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)    
            fp = open(file_name,"w")
            fp.write(docs_test[k] + "\n\n" + str(topics[0][1]) )
            fp.close()        
        else:           
            if not os.path.exists(dirname + "/unknown"):
                os.makedirs(dirname + "/unknown")  
            file_name = dirname + "/unknown/" + str(k) + ".txt"
            fp = open(file_name,"w")
            fp.write(docs_test[k])
            
            
            
docs_test = docs_all[60:]
cluster_similar_documents(docs_test,"Unfound")