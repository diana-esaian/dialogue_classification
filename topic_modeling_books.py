# import libraries
import pandas as pd
import os
import re
import natasha
from natasha import (Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger, NewsSyntaxParser, NewsNERTagger, Doc)
segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)
import gensim
from gensim.models import CoherenceModel, LdaModel 
from tqdm import tqdm

# filtering and lemmatizing function
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
            if span.normal.lower() not in names:
                names.append(span.normal.lower())
    black_list = stop_words + list(punctuation)
    for name in names:
        word = name.lower()
        black_list = black_list + word.split(' ')
    for token in doc_natasha.tokens:
        if token.pos in allowed_pos:
            token.lemmatize(morph_vocab)
            if token.lemma.lower() not in black_list:
                if re.findall('\D+', token.lemma) != 0:
                    if token.lemma.lower() != 'то':
                        lemmatized_text.append(token.lemma.lower())
    return lemmatized_text

with open ('final_stop.txt', encoding="utf8") as stop_file:
    rus_stops = [word.strip() for word in stop_file.readlines()]

punctuation = '!\"#$%&\'()*+,…-./' + ":;<=>?@[\]^_`{|}~—»«...–"

# lists with final results 
topics_dialogues = []
topics_books = []
authors = []
titles = []

# extract topics
text_folder = 'texts'
texts = os.listdir(text_folder)

dataset = pd.read_csv('dataset_1book.csv')

def main():
    count = 1
    for text in texts:
        with open(os.path.join(text_folder, text), encoding="utf-8") as f:
            book = f.read()
        # author
        index_author = text.index('.')
        author = text[:index_author]
        authors.append(author)
        # extract book title 
        index_title = text.rindex('.')
        title = text[index_author+1:index_title]
        titles.append(title)
        # extract topics from dialogues
        dialogues = ' '.join(dataset[(dataset['book'] == title) & (dataset['author'] == author)]['dialogues'].to_list())
        preprocessed_dialogues = [preprocess(dialogues, punctuation, rus_stops)]
        print('preprocess: done')
        gensim_dict = gensim.corpora.Dictionary(preprocessed_dialogues)
        gensim_dict.compactify()
        corpus = [gensim_dict.doc2bow(dial) for dial in preprocessed_dialogues]
        scores = []
        models = []
        for number in tqdm(range(2, 21)):
            model = LdaModel(corpus = corpus, num_topics = number, id2word = gensim_dict, passes = 10, random_state = 0)
            models.append(model)
            coherence = CoherenceModel(model = model, texts = preprocessed_dialogues, dictionary = gensim_dict, coherence = 'c_v')
            scores.append(coherence.get_coherence())
        model = models[scores.index[max(scores)]]
        topics_dialogues.append(model.print_topics())
        print('dialogues:', count)
        # separate replicas in the dialogues
        dialogues_split = []
        normal = re.findall("', '", dialogues)
        not_normal = re.findall('", "', dialogues)
        if len(noraml) > len(not_normal):
            replicas = dialogues.split("', '")
            for replica in replicas:
                letters = re.findall('\w', replica)
                if len(replica) != 0:
                    dialogues_split.append(replica)
        else:
            replicas = dialogues.split('", "')
            for replica in replicas:
                letters = re.findall('\w', replica)
                if len(replica) != 0:
                    dialogues_split.append(replica)
        # extract dialogues from the books
        for dialogue in dialogues_split:
            book = book.replace(dialogue, ' ')
        # extract topics from the book
        preprocessed_books = [preprocess(book, punctuation, rus_stops)]
        print('preprocess: done')
        gensim_dict = gensim.corpora.Dictionary(preprocessed_books)
        gensim_dict.compactify()
        corpus = [gensim_dict.doc2bow(text) for text in preprocessed_books]
        scores = []
        models = []
        for number in tqdm(range(2, 21)):
            model = LdaModel(corpus = corpus, num_topics = number, id2word = gensim_dict, passes = 10, random_state = 0)
            models.append(model)
            coherence = CoherenceModel(model = model, texts = preprocessed_books, dictionary = gensim_dict, coherence = 'c_v')
            scores.append(coherence.get_coherence())
        model = models[scores.index[max(scores)]]
        topics_books.append(model.print_topics())
        print('book', count)
        count += 1

    # prepare dataset 
    df_columns = ['author', 'book', 'topics_dialogues', 'topics_book']
    dataframe = pd.DataFrame(columns = df_columns)
    dataframe['author'] = authors
    dataframe['book'] = titles
    dataframe['topics_dialogues'] = topics_dialogues
    dataframe['topics_book'] = topics_books

    # create a dataset 
    dataframe.to_csv('topics.csv')

if __name__ == '__main__':
    main()
