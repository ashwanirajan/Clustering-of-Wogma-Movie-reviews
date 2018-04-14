import nltk
#nltk.download()
import os
import random
import codecs
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string
import re
from gensim import corpora
from operator import itemgetter
#import pandas as pd

def rem_ascii(s):
    return "".join([c for c in s if ord(c) < 128 ])


def clean(doc):
    doc_ascii = rem_ascii(doc)
    doc_ascii = re.sub(r"http\S+"," ",doc_ascii)
    stop_free = " ".join([i for i in doc_ascii.lower().split() if i not in stop])
   
    normalized = " ".join([lemma.lemmatize(word, 'v') for word in stop_free.split()])
    #print(nltk.tag.pos_tag(nltk.word_tokenize(normalized)))
    normalized = " ".join(word for word, tag in nltk.tag.pos_tag(nltk.word_tokenize(normalized)) if tag != 'NNP' and tag != 'NNPS' and tag != 'DT' and tag != 'RB' and tag != 'CC' and tag != 'CD' and tag != 'EX' and tag != 'IN' and tag != 'MD' and tag != 'PDT' and tag != 'PRP' and tag != 'PRP$' and tag !='VBD' and tag !='VBG' and tag !='JJ' and tag !='JJS')
    normalized  = ''.join([ch for ch in normalized if ch not in exclude])
    normalized  = " ".join([word for word in normalized.split() if word in eng_words])
    x = normalized.split()
    y = [s for s in x if len(s) > 2]
    return y


corpus_path = "D:\\Unfound\\reviews_new\\"
article_paths = [os.path.join(corpus_path,p) for p in os.listdir(corpus_path) if p.endswith("txt")]

# Read contents of all the reviews in a list "doc_complete"
doc_complete = []
for path in article_paths:
    fp = codecs.open(path,'r','utf-8')
    doc_content = fp.read()
    doc_complete.append(doc_content)  

# Randomly sample reviews      
docs_all = random.sample(doc_complete, 1000)


# Use 700 articles for training.
docs_train = docs_all[:700]
#docs_train = doc_complete[:700]
# Cleaning reviews
stop = set(stopwords.words('english'))
exclude = set(string.punctuation) 
lemma = WordNetLemmatizer()
eng_words = set(nltk.corpus.words.words())
doc_clean = [clean(doc) for doc in docs_train]



# Creating term dictionary of corpus 
dictionary = corpora.Dictionary(doc_clean)

#Filter terms which occurs in less than 10 articles & more than 40% of the reviews Note: This can be 
#optimized for better accuracy
dictionary.filter_extremes(no_below=10, no_above= 0.4)


# List of few words which are content neutral
stoplist = set('also blog bolly subhash deepa hes joshi direct will shall would should can could director write writer view makes viewer bollywood act bobby guha year sequence abusive appeal attention away brings care carry chatterjee chronicle actor actors menon share dont play played playing call called calling acting main may windowadsbygoogle taken seems instead perfect bit khan cinematic singh sharma here there where might this that these those nice great important bhai good bad awesome best worse worst better iamsrk film filmmaker anyone everyone use make break people 0 reviewer reviews know many call include part find become shah rukh shahrukh swetha ramakrishnan like mean often different \
               usually take due cant days months yes today pass no bool team mind issue direction pradeep green dutt bhansali sanjay ali dev jai priyankasoso india indian full scene movie man woman dialogue cinema watching doesnt running genre martini red blue mumbai dvd effect  annavetticadgoes2themovies wwwyoutubecomcyberpradeep right narrative  all thumb thumbs one two three four five six seven eight nine ten down up the brilliant another too him her city town however village done music cast you me meetu us her kunal singh kapoor kumar khanna experience usual despite wonderful perhaps almost problem never when come give well get since type list say change see refer actually iii \
               aisne kinds ask would beginning think desi camera fan  more move way something need things want every str'.split())
stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
dictionary.filter_tokens(stop_ids)

corpus = [dictionary.doc2bow(sent) for sent in doc_clean]
#vocab = list(dictionary.values()) #list of terms in the dictionary
#vocab_tf = [dict(i) for i in corpus]
#vocab_tf = list(pd.DataFrame(vocab_tf).sum(axis=0))

doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

num_t = int(input("How many topics do you want?\n"))
num_w = int(input("How many words do you want to see for each topic?\n\n"))

print("Training the model... please wait.")



from gensim.models.ldamodel import LdaModel as Lda
# Creating the object for LDA model using gensim library & Training LDA model on the document term matrix.
ldamodel = Lda(doc_term_matrix, num_topics=num_t, id2word = dictionary, passes=50, iterations=100)


# Print all the topics
for i,topic in enumerate(ldamodel.print_topics(num_topics=num_t, num_words=num_w)):
   words = topic[1].split("+")
   print(words)


def cluster_similar_documents(corpus, dirname):
    clean_docs = [clean(doc) for doc in corpus]
    test_term = [ldamodel.id2word.doc2bow(doc) for doc in clean_docs]
    doc_topics = ldamodel.get_document_topics(test_term, minimum_probability=0.1)    
    for k,topics in enumerate(doc_topics):        
        if topics:
            #print(topics[0][1])
            topics.sort(key = itemgetter(1), reverse=True)
            dir_name = dirname + "/" + str(topics[0][0])           
            file_name = dir_name + "/" + str(k) + ".txt"
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)    
            fp = open(file_name,"w", encoding="utf-8")
            fp.write(docs_test[k] + "\n\n" + str(topics[0][1]) )
            fp.close()        
        else:           
            if not os.path.exists(dirname + "/unknown"):
                os.makedirs(dirname + "/unknown")  
            file_name = dirname + "/unknown/" + str(k) + ".txt"
            fp = open(file_name,"w")
            fp.write(docs_test[k])
            
            
            
docs_test = docs_all[:700]
cluster_similar_documents(docs_test,"YOUR_DIRECTORY_HERE")
