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
    with open(os.path.join(text_folder, text), encoding="utf-8") as f:
        book_text = f.read()
    paragraphs = book_text.split('\n')
    all_paragraphs = []
    for para in paragraphs:
        paragraph = '\n' + para +'\n'
        all_paragraphs.append(paragraph)
    dialogue = []

    for paragraph in all_paragraphs:
        # replicas starting with -- 
        huge_replica_1 = re.findall('\n *[–|-].*[А-Я].*?\n|\n *[–|-].*[A-Z].*?\n', paragraph)
        if len(huge_replica_1) != 0:
            for hugereplica in huge_replica_1:
                replicas_and_authors_1_2 = re.findall('[–|-][–|-].*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..](?= *[–|-][–|-].*?[(!)+|(?)+|.|...|…|..|,|!?|?!|?!?|!?!|!..|?..])', hugereplica)
                if len(replicas_and_authors_1_2) != 0:
                    for index in range(len(replicas_and_authors_1_2)):
                        if index % 2 == 0:
                            dialogue.append(replicas_and_authors_1_2[index])
                    if len(replicas_and_authors_1_2) % 2 == 0:
                        last_extracted = replicas_and_authors_1_2[len(replicas_and_authors_1_2)-1]
                        last_extracted = last_extracted.replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                        last_replica = re.findall('(?<={last_extracted}).*'.format(last_extracted = last_extracted), hugereplica)
                        dialogue = dialogue + last_replica
                # replicas starting with –        
                else:
                    replicas_and_authors_1 = re.findall('–.*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..](?= *–.*?[(!)+|(?)+|.|...|…|..|,|!?|?!|?!?|!?!|!..|?..])', hugereplica)
                    if len(replicas_and_authors_1) != 0:
                        for index in range(len(replicas_and_authors_1)):
                            if index % 2 == 0:
                                dialogue.append(replicas_and_authors_1[index])
                        if len(replicas_and_authors_1) % 2 == 0:
                            last_extracted = replicas_and_authors_1[len(replicas_and_authors_1)-1]
                            last_extracted = last_extracted.replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                            last_replica = re.findall('(?<={last_extracted}).*'.format(last_extracted = last_extracted), hugereplica)
                            dialogue = dialogue + last_replica
                    # replicas starting with -
                    else:
                        replicas_and_authors_1_1 = re.findall('-.*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..](?= *-.*?[(!)+|(?)+|.|...|…|..|,|!?|?!|?!?|!?!|!..|?..])', paragraph)
                        if len(replicas_and_authors_1_1) != 0:
                            for index in range(len(replicas_and_authors_1_1)):
                                if index % 2 == 0:
                                    dialogue.append(replicas_and_authors_1_1[index])
                            if len(replicas_and_authors_1_1) % 2 == 0:
                                last_extracted = replicas_and_authors_1_1[len(replicas_and_authors_1_1)-1]
                                last_extracted = last_extracted.replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                last_replica = re.findall('(?<={last_extracted}).*'.format(last_extracted = last_extracted), hugereplica)
                                dialogue = dialogue + last_replica
                        # replica starting with - but without author's comments 
                        else:
                            for replica in huge_replica_1:
                                dialogue.append(replica.replace('\n', ''))
        # replicas starting with «»
        else:
            # «Direct speech» - author's comment
            short_replica_1 = re.findall('[«|\"|\'].*?[а-я].*?[»|\"|\'](?= *[–|-])', paragraph)
            if len(short_replica_1) != 0:
                dialogue = dialogue + short_replica_1
            # author's comment: «Direct speech»
            short_replica_2 = re.findall('(?<=:) *[«|\"|\'].*?[»|\"|\']', paragraph)
            if len(short_replica_2) != 0:
                for rep in short_replica_2:
                    if rep not in short_replica_1:
                        dialogue.append(rep)
            

            huge_replica_3 = re.findall('\n *[«|\"|\'].*?[»|\"|\'] *\n', paragraph)
            if len(huge_replica_3) != 0:
                for replica in huge_replica_3:
                    huge_replica_2 = re.findall('[«|\"|\'].*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..] *[–|-][–|-].*?[»|\"|\']', replica)
                    if len(huge_replica_2) != 0:
                        for sentence in huge_replica_2:
                            replicas_and_authors_2 = re.findall('.*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..] *(?=[–|-][–|-])', sentence)
                            if len(replicas_and_authors_2) != 0:
                                for index in range(len(replicas_and_authors_2)):
                                    if index % 2 == 0:
                                        if replicas_and_authors_2[index] not in short_replica_1 and replicas_and_authors_2[index] not in short_replica_2:
                                            dialogue.append(replicas_and_authors_2[index])
                                if len(replicas_and_authors_2) % 2 == 0:
                                    last_extracted_2 = replicas_and_authors_2[len(replicas_and_authors_2)-1]
                                    last_extracted_2 = last_extracted_2.replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                    last_replica_2 = re.findall('(?<={last_extracted_2}).*'.format(last_extracted_2 = last_extracted_2), sentence)
                                    for i in last_replica_2:
                                        if i not in short_replica_1 and i not in short_replica_2:
                                            dialogue.append(i)
                    else:
                        huge_replica_2_1 = re.findall('[«|\"|\'].*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..] *–.*?[»|\"|\']', replica)
                        if len(huge_replica_2_1) != 0:
                            for sentence in huge_replica_2_1:
                                replicas_and_authors_2 = re.findall('.*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..] *(?=–)', sentence)
                                if len(replicas_and_authors_2) != 0:
                                    for index in range(len(replicas_and_authors_2)):
                                        if index % 2 == 0:
                                            if replicas_and_authors_2[index] not in short_replica_1 and replicas_and_authors_2[index] not in short_replica_2:
                                                dialogue.append(replicas_and_authors_2[index])
                                    if len(replicas_and_authors_2) % 2 == 0:
                                        last_extracted_2 = replicas_and_authors_2[len(replicas_and_authors_2)-1]
                                        last_extracted_2 = last_extracted_2.replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                        last_replica_2 = re.findall('(?<={last_extracted_2}).*'.format(last_extracted_2 = last_extracted_2), sentence)
                                        for i in last_replica_2:
                                            if i not in short_replica_1 and i not in short_replica_2:
                                                dialogue.append(i)
                        else:
                            huge_replica_2_2 = re.findall('[«|\"|\'].*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..] *-.*?[»|\"|\']', replica)
                            if len(huge_replica_2_2) != 0:
                                for sentence in huge_replica_2_2:
                                    replicas_and_authors_2 = re.findall('.*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..] *(?=-)', sentence)
                                    if len(replicas_and_authors_2) != 0:
                                        for index in range(len(replicas_and_authors_2)):
                                            if index % 2 == 0:
                                                if replicas_and_authors_2[index] not in short_replica_1 and replicas_and_authors_2[index] not in short_replica_2:
                                                    dialogue.append(replicas_and_authors_2[index])
                                        if len(replicas_and_authors_2) % 2 == 0:
                                            last_extracted_2 = replicas_and_authors_2[len(replicas_and_authors_2)-1]
                                            last_extracted_2 = last_extracted_2.replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                            last_replica_2 = re.findall('(?<={last_extracted_2}).*'.format(last_extracted_2 = last_extracted_2), sentence)
                                            for i in last_replica_2:
                                                if i not in short_replica_1 and i not in short_replica_2:
                                                    dialogue.append(i)
    # extract author's name
    index_author = text.index('.')
    author = text[:index_author]
    authors.append(author)

    # extract book title 
    index_title = text.rindex('.')
    title = text[index_author+1:index_title]
    books.append(title)

    # book wordcount
    book_words = len(re.findall(r'\w+', book_text))
    book_wordcount.append(book_words)

    # dialogues
    dialogues.append(dialogue)

    #dialogues word count
    all_dialogues = ' '.join(dialogue)
    dialogue_words = len(re.findall(r'\w+', all_dialogues))
    dialogues_wordcout.append(dialogue_words)

# preparing dataset 
df_columns = ['author', 'book', 'book_wordcount', 'dialogues', 'dialogues_wordcout']
dataframe = pd.DataFrame(columns = df_columns)
dataframe['author'] = authors
dataframe['book'] = books
dataframe['book_wordcount'] = book_wordcount
dataframe['dialogues'] = dialogues
dataframe['dialogues_wordcout'] = dialogues_wordcout
dataframe['ratio'] = dataframe['dialogues_wordcout'] / dataframe['book_wordcount']

# creating a dataset 
dataframe.to_csv('dataset.csv')