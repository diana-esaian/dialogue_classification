import os
os.system("pip install pandas")
import re
import pandas as pd

text_folder = 'texts'
texts = os.listdir(text_folder)

# lists for future dataset
authors = []
books = []
book_wordcount = []
dialogues = []
dialogues_wordcout = []

# extract dialogues
for text in texts:
  with open(os.path.join(text_folder, text)) as f:
    book_text = f.read()
  paragraphs = book_text.split('\n')
  all_paragraphs = []
  for para in paragraphs:
    paragraph = '\n' + para +'\n'
    all_paragraphs.append(paragraph)
  dialogue = []
  for paragraph in all_paragraphs:
    # replicas starting with -
    huge_replica_1 = re.findall('\\n *[–|-] *[А-Я].*?\\n', paragraph)
    if len(huge_replica_1) != 0:
      replicas_and_authors_1 = re.findall('[–|-].*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..](?= *[–|-].*?[(!)+|(?)+|.|...|…|..|,|!?|?!|?!?|!?!|!..|?..])', paragraph)
      if len(replicas_and_authors_1) != 0:
        for index in range(len(replicas_and_authors_1)):
          if index % 2 == 0:
            dialogue.append(replicas_and_authors_1[index])
        if len(replicas_and_authors_1) % 2 == 0:
          last_extracted = replicas_and_authors_1[len(replicas_and_authors_1)-1]
          last_extracted = last_extracted.replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
          last_replica = re.findall('(?<={last_extracted}).*'.format(last_extracted = last_extracted), paragraph)
          dialogue = dialogue + last_replica
      else:
        for replica in huge_replica_1:
          dialogue.append(replica.replace('\n', ''))
    # replicas with «»
    else:
      short_replica_1 = re.findall('[«|"].*?[»|"](?= *[–|-])', paragraph)
      if len(short_replica_1) != 0:
        dialogue = dialogue + short_replica_1
      short_replica_2 = re.findall('(?<=:) *[«|"].*?[»|"]', paragraph)
      if len(short_replica_2) != 0:
        dialogue = dialogue + short_replica_2
      huge_replica_2 = re.findall('[«|"].*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..] *[–|-].*?[»|"]', paragraph)
      if len(huge_replica_2) != 0:
        for sentence in huge_replica_2:
          replicas_and_authors_2 = re.findall('.*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..] *(?=[–|-])', sentence)
          for index in range(len(replicas_and_authors_2)):
            if index % 2 == 0:
              dialogue.append(replicas_and_authors_2[index])
          if len(replicas_and_authors_2) % 2 == 0:
            last_extracted_2 = replicas_and_authors_2[len(replicas_and_authors_2)-1]
            last_extracted_2 = last_extracted_2.replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
            last_replica_2 = re.findall('(?<={last_extracted_2}).*'.format(last_extracted_2 = last_extracted_2), sentence)
            dialogue = dialogue + last_replica_2
      if len(short_replica_1) == 0 and len(short_replica_2) == 0 and len(huge_replica_2) == 0:
        huge_replica_3 = re.findall('\\n *[«|"].*?[»|"] *\\n', paragraph)
        if len(huge_replica_3) != 0:
          for replica in huge_replica_3:
            dialogue.append(replica.replace('\n', ''))

  # extract author's name
  index_author = text.index('.')
  author = text[:index_author]
  authors.append(author)

  # extract book title 
  index_title = text.rindex('.')
  title = text[index_author+1:index_title]
  books.append(title)

  # book wordcount
  punctuation = ["!",'"', "#", "$", "%", "&", "'", "(", ",", ")", "*", "+", "-", ".", ":", ";", "<", "=", ">", "?", "[", "]", "^","_","`","{","|","}","~","—","»","«","...","–","…"]  
  book_no_punct = book_text
  for character in book_no_punct:
    if character in list(punctuation):
      book_no_punct.replace(character, ' ')
  book_words = len(book_no_punct.split())
  book_wordcount.append(book_words)

  # dialogues
  dialogues.append(dialogue)

  #dialogues word count
  all_dialogues = ' '.join(dialogue)
  punctuation = ["!",'"', "#", "$", "%", "&", "'", "(", ",", ")", "*", "+", "-", ".", ":", ";", "<", "=", ">", "?", "[", "]", "^","_","`","{","|","}","~","—","»","«","...","–","…"]  
  dialogue_no_punct = all_dialogues
  for character in dialogue_no_punct:
    if character in list(punctuation):
      dialogue_no_punct.replace(character, ' ')
  dialogue_words = len(dialogue_no_punct.split())
  dialogues_wordcout.append(dialogue_words)

# preparing dataset 
df_columns = ['author', 'book', 'book_wordcount', 'dialogues', 'dialogues_wordcout']
dataframe = pd.DataFrame(columns = df_columns)
dataframe['author'] = authors
dataframe['book'] = books
dataframe['book_wordcount'] = book_wordcount
dataframe['dialogues'] = dialogues
dataframe['dialogues_wordcout'] = dialogues_wordcout

# creating a dataset 
dataframe.to_csv('dataset.csv')