import os
# os.system("pip install gensim")
# os.system("pip install natasha")
# os.system("pip install pymorphy2")
# os.system("pip install nltk")
# import nltk
from nltk.tokenize import word_tokenize 
from nltk import download as nltk_download 
# nltk_download ('punkt')
# import natasha
from natasha import (Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger, NewsSyntaxParser, NewsNERTagger, Doc)
segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)
# import pymorphy2
from pymorphy2 import MorphAnalyzer
parser = MorphAnalyzer()
# gensim
import gensim
# import re
import re

def main():
    # text_folder and stop_folder
    text_folder = 'texts'
    texts = os.listdir(text_folder)
    stop_folder = 'stop'
    stop = os.listdir(stop_folder)

    # lists for future dataset
    authors = []
    books = []
    topics = []

    # initial black list
    rus_stops = []
    for st in stop:
        with open(os.path.join(stop_folder, st), encoding="utf-8") as f:
            rus_st = [word.strip() for word in f.readlines()]
            rus_stops = rus_stops + rus_st

    punctuation = '!\"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~—»«...–'

    # # function for preprocessing 
    # def preprocess(input_text):
    #     tokenized_text = word_tokenize(input_text.lower())
    #     output_text = [word for word in tokenized_text if word not in filters]
    #     clean_text = [word for word in output_text if word.isalpha()]
    #     lemmatized_text = [parser.parse(word)[0].normal_form for word in clean_text]
    #     return lemmatized_text

    # read every book
    for book in texts:
        with open(os.path.join(text_folder, book), encoding="utf-8") as f:
            text = f.read()
        text_list = []
        text_list.append(text)
        # append black list
        doc_natasha = Doc(text)
        doc_natasha.segment(segmenter)
        doc_natasha.tag_morph(morph_tagger)
        doc_natasha.parse_syntax(syntax_parser)
        doc_natasha.tag_ner(ner_tagger)
        names = []
        for span in doc_natasha.spans:
            if span.type == 'PER':
                if span.text not in names:
                    names.append(span.text)
                span.normalize(morph_vocab)
                if span.normal not in names:
                    names.append(span.normal)
        filters = rus_stops + list(punctuation)
        for name in names:
            word = name.lower()
            filters = filters + word.split(' ')
        # extract topics
        def preprocess(input_text):
            tokenized_text = word_tokenize(input_text.lower())
            output_text = [word for word in tokenized_text if word not in filters]
            clean_text = [word for word in output_text if word.isalpha()]
            lemmatized_text = [parser.parse(word)[0].normal_form for word in clean_text]
            return lemmatized_text
        preprocessed_texts = [preprocess(text_t) for text_t in text_list]
        gensim_dictionary_for_TM = gensim.corpora.Dictionary(preprocessed_texts)
        gensim_dictionary_for_TM.compactify()
        corpus = [gensim_dictionary_for_TM.doc2bow(text_p) for text_p in preprocessed_texts]
        lda = gensim.models.LdaMulticore(corpus,num_topics = 10, id2word=gensim_dictionary_for_TM, passes=10)
        topics_book = []
        for topic in lda.print_topics():
            topic_extracted = re.findall(r'(?<=")\w.*?(?=")', topic[1])
            for i in topic_extracted:
                if i not in topics_book:
                    topics_book.append(i)

        # extract author's name
        index_author = text.index('.')
        author = text[:index_author]
        authors.append(author)

        # extract book title 
        index_title = text.rindex('.')
        title = text[index_author+1:index_title]
        books.append(title)

        # topics 
        topics.append(topics_book)

    df_columns = ['author', 'book', 'topics']
    dataframe = pd.DataFrame(columns = df_columns)
    dataframe['author'] = authors
    dataframe['book'] = books
    dataframe['topics'] = topics

    # creating a dataset 
    dataframe.to_csv('topics_books.csv')



if __name__ == '__main__':
    main()
