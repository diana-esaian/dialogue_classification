import os
os.system("pip install natasha")
os.system("pip install scikit-learn")
from natasha import (Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger, NewsSyntaxParser, NewsNERTagger, Doc)
segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

text_folder = 'texts'
texts = os.listdir(text_folder)

# lists for future dataset
all_authors = []
all_books = []
all_topics = []

def preprocess(input_text, punctuation, stop_words):
  doc_natasha = Doc(input_text)
  doc_natasha.segment(segmenter)
  doc_natasha.tag_morph(morph_tagger)
  doc_natasha.parse_syntax(syntax_parser)
  doc_natasha.tag_ner(ner_tagger)
  allowed_pos = ['NOUN', 'ADJ', 'VERB', 'ADV']
  lemmatized_text = []
  names = []
  for span in doc_natasha.spans:
    if span.type == 'PER':
      span.normalize(morph_vocab)
      if span.normal not in names:
        names.append(span.normal.lower())
  black_list = stop_words + list(punctuation)
  for name in names:
    word = name.lower()
    black_list = black_list + word.split(' ')
  for token in doc_natasha.tokens:
    if token.pos in allowed_pos:
      token.lemmatize(morph_vocab)
      if token.lemma not in black_list:
        if re.findall('\D+', token.lemma) != 0:
          lemmatized_text.append(token.lemma)
  return lemmatized_text

with open ('stop_ru.txt', encoding="utf8") as stop_file:
    rus_stops = [word.strip() for word in stop_file.readlines()]

punctuation = '!\"#$%&\'()*+,…-./' + ":;<=>?@[\]^_`{|}~—»«...–"

count = 1
for text in texts:
    with open(os.path.join(text_folder, text), encoding="utf-8") as f:
        text = f.read()
    lemmatized_text = preprocess(text, punctuation, rus_stops)
    cv = TfidfVectorizer(lowercase=True)
    dtm = cv.fit_transform(lemmatized_text)
    model=LatentDirichletAllocation(n_components=5)
    model.fit(dtm)
    lda_matrix = model.fit_transform(dtm)
    lda_components=model.components_
    terms = cv.get_feature_names_out()
    topics = []
    for index, component in enumerate(lda_components):
        zipped = zip(terms, component)
        top_terms_key=sorted(zipped, key = lambda t: t[1], reverse=True)[:7]
        top_terms_list=list(dict(top_terms_key).keys())
        # print("Topic "+str(index)+": ",top_terms_list)
        topics.append(top_terms_list)
   
    # index_author = text.index('.')
    # author = text[:index_author]
    # print(author)
    # all_authors.append(author)

    # extract book title 
    # index_title = text.rindex('.')
    # title = text[index_author+1:index_title]
    # all_books.append(title)
    # print(index_title)

    # topics
    all_topics.append(topics)
    print(topics)

    print(count)
    count +=1

df_columns = ['author', 'book', 'topics']
dataframe = pd.DataFrame(columns = df_columns)
# dataframe['author'] = all_authors
# dataframe['book'] = all_books
dataframe['topics'] = all_topics

# creating a dataset 
dataframe.to_csv('topics_books.csv')
