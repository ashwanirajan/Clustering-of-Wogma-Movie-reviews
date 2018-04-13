# Clustering-of-Wogma-Movie-reviews
This repository includes python script to extract, download and cluster movie reviews on wogma.


Step 1: Extraction of Urls from the tagret website
This step has been performed in extract_urls.py. I used requests.get() in order to extract url from a parent websits and stored it to a text file.

Step 2: Extraction of data from each url from the list of urls
In data_import.py, I have used beautifulsoup along with request.get() in order to recieve the HTML text from the website and using the HTML text, I have iterated over the tags like <p> and <a> present in the target class and ids.

Step 3: Cleaning/preprocessing the data performed by clean(doc) function
  1. removing the ascii characters
  2. removing the urls
  3. removing stop_words(a list of 127 common words in nltk) and performing lemmatization
  4. removing the words which are not present in english dictionary(to remove proper nouns like salman, kapoor etc)
  5. removing punctuations
  6. dividing the reviews set to test and train data and radnomly sampling the reviews for each iteration using random.sample()
  
Step 4: Creating token to id dictionary
  1.Using corpora.Dictionary to create words to id number mapping. 
  2.Filtering the dictionary for some common words like cinema, industry etc.
  3.Filtering the dictionary for words which occur in less than x no. of reviews and words which appear in more than y no. of reviews. Optimizing x and y helps in increasing accuracy
  4.Creating bag of words using dictionary.doc2bow() and hence creating corpus

Step 5: LDA model training
  1. Creating a doc_term_matrix to provide an an input to  LdaModel
  2. inputing no. of topics and no. of required words.
  3. Training the model by randomly sampling the input documents from the review set
  4. printing the words for each topic along with their topic probability of existence in that particular topic.
 
Step 5: Clustering performed by cluster_similar_documents function
  1.taking the test set as input and performing LDA and assigning topics to each new review.
  2.clustering and collecting each review into saperate folders based on their topic.
  
