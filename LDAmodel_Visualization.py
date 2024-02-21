import json
import pyLDAvis
import string
import re
from nltk.corpus import stopwords
from gensim import corpora, models
from nltk.tokenize import word_tokenize
import pyLDAvis.gensim_models
import matplotlib.pyplot as plt


# Load text data from the JSON file
with open("valio21.json", "r", encoding="utf-8") as fin:
    data = json.load(fin)
# Initialize a list to store the text content
texts = []

# Iterate over each JSON object in the array
for item in data:
    # Extract the text content associated with the key "text"
    text_content = item.get("text", "")
    
    # Append the extracted text content to the list
    texts.append(text_content)


preprocessed_texts = []

# Set of English stopwords
stop_words = set(stopwords.words("english"))

# Regular expression pattern to remove punctuation marks
pattern = r'[^\w\s]'  # Matches any character that is not a word character or whitespace

# Iterate over each text in the "texts" list
for text in texts:
    # Convert text to lowercase
    text = text.lower()
 # Tokenize the text using NLTK's word_tokenize()
    tokens = word_tokenize(text)
    
    # Remove stopwords and numbers, and join words back into a string
    filtered_text = [word for word in tokens if word not in stop_words and not word.isdigit()]
    preprocessed_text = ' '.join(filtered_text)
    
    # Remove remaining punctuation marks using regular expressions
    preprocessed_text = re.sub(pattern, '', preprocessed_text)
    
    # Append preprocessed text to the list
    preprocessed_texts.append(preprocessed_text)
#print(preprocessed_texts)

# Tokenize each string into a list of words
tokenized_texts = [word_tokenize(text) for text in preprocessed_texts]

# Create a dictionary and a corpus
dictionary = corpora.Dictionary(tokenized_texts)
corpus = [dictionary.doc2bow(text) for text in tokenized_texts]

# Build the LDA model
lda_model = models.LdaModel(corpus, num_topics=10, id2word=dictionary, passes=15)

# Print the topics
for topic_id, topic_words in lda_model.print_topics():
   print(f'Topic {topic_id + 1}: {topic_words}')

# Save the model
lda_model.save('lda_model')

print('LDA model has been successfully created and saved.')

# Visualize the topics
lda_display = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary, sort_topics=False)
pyLDAvis.save_html(lda_display, 'lda_visualization21.html')

# Display the local HTML file in my default web browser
import webbrowser
webbrowser.open('lda_visualization21.html')

