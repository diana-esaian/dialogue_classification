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

# extract paragraphs
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
        huge_replica_1 = re.findall('\n *[–|-].*\w.*?\n', paragraph)
        if len(huge_replica_1) != 0:
            for hugereplica in huge_replica_1:
                replicas_and_authors_1_2 = re.findall('[–|-][–|-].*?\w.*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..](?= *[–|-][–|-].*?\w.*?[(!)+|(?)+|.|...|…|..|,|!?|?!|?!?|!?!|!..|?..])', hugereplica)
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
                    replicas_and_authors_1 = re.findall('–.*?\w.*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..](?= *–.*?\w.*?[(!)+|(?)+|.|...|…|..|,|!?|?!|?!?|!?!|!..|?..])', hugereplica)
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
                        replicas_and_authors_1_1 = re.findall('-.*?\w.*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..](?= *-.*?\w.*?[(!)+|(?)+|.|...|…|..|,|!?|?!|?!?|!?!|!..|?..])', paragraph)
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
            # all replicas and not replicas starting with «»
            all_replicas_and_not = re.findall('«.*?\w.*?»', paragraph)
            if len(all_replicas_and_not) != 0:
                for element in all_replicas_and_not:
                    extracted = element.replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                    # check if the replica has the following structure «Direct speech» - author's comment
                    short_replica_1 = re.findall('{direct_sp}(?= *,? *[–|-])'.format(direct_sp=extracted), paragraph)
                    if len(short_replica_1) != 0:
                        dialogue = dialogue + short_replica_1
                    else:
                        # check if the replica has the following structure Author's comment: «Direct speech»
                        short_replica_2 = re.findall('(?<=:) *{direct_sp}'.format(direct_sp=extracted), paragraph)
                        if len(short_replica_2) != 0:
                            dialogue = dialogue + short_replica_2
                        else:
                            # check if direct speach is split by author's comments (quotation marks «)
                            huge_replica_2 = re.findall('«.*?\w.*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..] *[–|-][–|-].*?\w.*?»', element)
                            if len(huge_replica_2) != 0:
                                for sentence in huge_replica_2:
                                    replicas_and_authors_2 = re.findall('.*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..] *(?=[–|-][–|-])', sentence)
                                    if len(replicas_and_authors_2) != 0:
                                        for index in range(len(replicas_and_authors_2)):
                                            if index % 2 == 0:
                                                dialogue.append(replicas_and_authors_2[index])
                                        if len(replicas_and_authors_2) % 2 == 0:
                                            last_extracted_2 = replicas_and_authors_2[len(replicas_and_authors_2)-1]
                                            last_extracted_2 = last_extracted_2.replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                            last_replica_2 = re.findall('(?<={last_extracted_2}).*'.format(last_extracted_2 = last_extracted_2), sentence)
                                            dialogue = dialogue + last_replica_2
                            else:
                                huge_replica_2_1 = re.findall('«.*?\w.*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..] *–.*?\w.*?»', element)
                                if len(huge_replica_2_1) != 0:
                                    for sentence in huge_replica_2_1:
                                        replicas_and_authors_2 = re.findall('.*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..] *(?=–)', sentence)
                                        if len(replicas_and_authors_2) != 0:
                                            for index in range(len(replicas_and_authors_2)):
                                                if index % 2 == 0:
                                                    dialogue.append(replicas_and_authors_2[index])
                                            if len(replicas_and_authors_2) % 2 == 0:
                                                last_extracted_2 = replicas_and_authors_2[len(replicas_and_authors_2)-1]
                                                last_extracted_2 = last_extracted_2.replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                                last_replica_2 = re.findall('(?<={last_extracted_2}).*'.format(last_extracted_2 = last_extracted_2), sentence)
                                                dialogue = dialogue + last_replica_2
                                else:
                                    huge_replica_2_2 = re.findall('«.*?\w.*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..] *-.*?»', element)
                                    if len(huge_replica_2_2) != 0:
                                        for sentence in huge_replica_2_2:
                                            replicas_and_authors_2 = re.findall('.*?\w.*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..] *(?=-)', sentence)
                                            if len(replicas_and_authors_2) != 0:
                                                for index in range(len(replicas_and_authors_2)):
                                                    if index % 2 == 0:
                                                        dialogue.append(replicas_and_authors_2[index])
                                                if len(replicas_and_authors_2) % 2 == 0:
                                                    last_extracted_2 = replicas_and_authors_2[len(replicas_and_authors_2)-1]
                                                    last_extracted_2 = last_extracted_2.replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                                    last_replica_2 = re.findall('(?<={last_extracted_2}).*'.format(last_extracted_2 = last_extracted_2), sentence)
                                                    dialogue = dialogue + last_replica_2
                                    else:
                                        huge_replica_3 = re.findall('(?<=\n) *«.*?\w.*?» *(?=\n)', paragraph)
                                        if len(huge_replica_3) != 0:
                                            dialogue = dialogue + huge_replica_3
            # all replicas and not replicas starting with ""
            else:
                all_replicas_and_not_2 = re.findall('\" *\w.*?\"', paragraph)
                if len(all_replicas_and_not_2) != 0:
                    for element in all_replicas_and_not_2:
                        extracted = element.replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                        # check if the replica has the following structure «Direct speech» - author's comment
                        short_replica_1 = re.findall('{direct_sp}(?= *,? *[–|-])'.format(direct_sp=extracted), paragraph)
                        if len(short_replica_1) != 0:
                            dialogue = dialogue + short_replica_1
                        else:
                            # check if the replica has the following structure Author's comment: «Direct speech»
                            short_replica_2 = re.findall('(?<=:) *{direct_sp}'.format(direct_sp=extracted), paragraph)
                            if len(short_replica_2) != 0:
                                dialogue = dialogue + short_replica_2
                            else:
                                # check if direct speach is split by author's comments (quotation marks "")
                                huge_replica_2 = re.findall('\".*?\w.*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..] *[–|-][–|-].*?\"', element)
                                if len(huge_replica_2) != 0:
                                    for sentence in huge_replica_2:
                                        replicas_and_authors_2 = re.findall('.*?\w.*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..] *(?=[–|-][–|-])', sentence)
                                        if len(replicas_and_authors_2) != 0:
                                            for index in range(len(replicas_and_authors_2)):
                                                if index % 2 == 0:
                                                    dialogue.append(replicas_and_authors_2[index])
                                            if len(replicas_and_authors_2) % 2 == 0:
                                                last_extracted_2 = replicas_and_authors_2[len(replicas_and_authors_2)-1]
                                                last_extracted_2 = last_extracted_2.replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                                last_replica_2 = re.findall('(?<={last_extracted_2}).*'.format(last_extracted_2 = last_extracted_2), sentence)
                                                dialogue = dialogue + last_replica_2
                                else:
                                    huge_replica_2_1 = re.findall('\".*?\w.*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..] *–.*?\"', element)
                                    if len(huge_replica_2_1) != 0:
                                        for sentence in huge_replica_2_1:
                                            replicas_and_authors_2 = re.findall('.*?\w.*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..] *(?=–)', sentence)
                                            if len(replicas_and_authors_2) != 0:
                                                for index in range(len(replicas_and_authors_2)):
                                                    if index % 2 == 0:
                                                        dialogue.append(replicas_and_authors_2[index])
                                                if len(replicas_and_authors_2) % 2 == 0:
                                                    last_extracted_2 = replicas_and_authors_2[len(replicas_and_authors_2)-1]
                                                    last_extracted_2 = last_extracted_2.replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                                    last_replica_2 = re.findall('(?<={last_extracted_2}).*'.format(last_extracted_2 = last_extracted_2), sentence)
                                                    dialogue = dialogue + last_replica_2
                                    else:
                                        huge_replica_2_2 = re.findall('\".*?\w.*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..] *-.*?\"', element)
                                        if len(huge_replica_2_2) != 0:
                                            for sentence in huge_replica_2_2:
                                                replicas_and_authors_2 = re.findall('.*?\w.*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..] *(?=-)', sentence)
                                                if len(replicas_and_authors_2) != 0:
                                                    for index in range(len(replicas_and_authors_2)):
                                                        if index % 2 == 0:
                                                            dialogue.append(replicas_and_authors_2[index])
                                                    if len(replicas_and_authors_2) % 2 == 0:
                                                        last_extracted_2 = replicas_and_authors_2[len(replicas_and_authors_2)-1]
                                                        last_extracted_2 = last_extracted_2.replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                                        last_replica_2 = re.findall('(?<={last_extracted_2}).*'.format(last_extracted_2 = last_extracted_2), sentence)
                                                        dialogue = dialogue + last_replica_2
                                        else:
                                            huge_replica_3 = re.findall('(?<=\n) *\".*?\w.*?\" *(?=\n)', paragraph)
                                            if len(huge_replica_3) != 0:
                                                dialogue = dialogue + huge_replica_3
                # all replicas and not replicas starting with ""
                else:
                    all_replicas_and_not_3 = re.findall('\'.*?\w.*?\'', paragraph)
                    if len(all_replicas_and_not_3) != 0:
                        for element in all_replicas_and_not_3:
                            extracted = element.replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                            # check if the replica has the following structure «Direct speech» - author's comment
                            short_replica_1 = re.findall('{direct_sp}(?= *,? *[–|-])'.format(direct_sp=extracted), paragraph)
                            if len(short_replica_1) != 0:
                                dialogue = dialogue + short_replica_1
                            else:
                                # check if the replica has the following structure Author's comment: «Direct speech»
                                short_replica_2 = re.findall('(?<=:) *{direct_sp}'.format(direct_sp=extracted), paragraph)
                                if len(short_replica_2) != 0:
                                    dialogue = dialogue + short_replica_2
                                else:
                                    # check if direct speach is split by author's comments (quotation marks «)
                                    huge_replica_2 = re.findall('\'.*?\w.*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..] *[–|-][–|-].*?\'', element)
                                    if len(huge_replica_2) != 0:
                                        for sentence in huge_replica_2:
                                            replicas_and_authors_2 = re.findall('.*?\w.*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..] *(?=[–|-][–|-])', sentence)
                                            if len(replicas_and_authors_2) != 0:
                                                for index in range(len(replicas_and_authors_2)):
                                                    if index % 2 == 0:
                                                        dialogue.append(replicas_and_authors_2[index])
                                                if len(replicas_and_authors_2) % 2 == 0:
                                                    last_extracted_2 = replicas_and_authors_2[len(replicas_and_authors_2)-1]
                                                    last_extracted_2 = last_extracted_2.replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                                    last_replica_2 = re.findall('(?<={last_extracted_2}).*'.format(last_extracted_2 = last_extracted_2), sentence)
                                                    dialogue = dialogue + last_replica_2
                                    else:
                                        huge_replica_2_1 = re.findall('\'.*?\w.*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..] *–.*?\'', element)
                                        if len(huge_replica_2_1) != 0:
                                            for sentence in huge_replica_2_1:
                                                replicas_and_authors_2 = re.findall('.*?\w.*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..] *(?=–)', sentence)
                                                if len(replicas_and_authors_2) != 0:
                                                    for index in range(len(replicas_and_authors_2)):
                                                        if index % 2 == 0:
                                                            dialogue.append(replicas_and_authors_2[index])
                                                    if len(replicas_and_authors_2) % 2 == 0:
                                                        last_extracted_2 = replicas_and_authors_2[len(replicas_and_authors_2)-1]
                                                        last_extracted_2 = last_extracted_2.replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                                        last_replica_2 = re.findall('(?<={last_extracted_2}).*'.format(last_extracted_2 = last_extracted_2), sentence)
                                                        dialogue = dialogue + last_replica_2
                                        else:
                                            huge_replica_2_2 = re.findall('\'.*?\w.*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..] *-.*?\'', element)
                                            if len(huge_replica_2_2) != 0:
                                                for sentence in huge_replica_2_2:
                                                    replicas_and_authors_2 = re.findall('.*?\w.*?[(!)+|(?)+|.|,|...|…|..|!?|?!|?!?|!?!|!..|?..] *(?=-)', sentence)
                                                    if len(replicas_and_authors_2) != 0:
                                                        for index in range(len(replicas_and_authors_2)):
                                                            if index % 2 == 0:
                                                                dialogue.append(replicas_and_authors_2[index])
                                                        if len(replicas_and_authors_2) % 2 == 0:
                                                            last_extracted_2 = replicas_and_authors_2[len(replicas_and_authors_2)-1]
                                                            last_extracted_2 = last_extracted_2.replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                                            last_replica_2 = re.findall('(?<={last_extracted_2}).*'.format(last_extracted_2 = last_extracted_2), sentence)
                                                            dialogue = dialogue + last_replica_2
                                            else:
                                                huge_replica_3 = re.findall('(?<=\n) *\'.*?\w.*?\' *(?=\n)', paragraph)
                                                if len(huge_replica_3) != 0:
                                                    dialogue = dialogue + huge_replica_3
                                                else:
                                                    # replicas starting with : -- 
                                                    tiny_replica = re.findall(': *[–|-][–|-] *[А-Я].*?[(!)+|(?)+|,|.|...|…|..|!?|?!|?!?|!?!|!..|?..]', paragraph)
                                                    if len(tiny_replica) != 0:
                                                        for tiny in tiny_replica:
                                                            tiny_clean = tiny.replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                                            full_replica = re.findall('{tiny_clean}.*?[(!)+|(?)+|,|.|...|…|..|!?|?!|?!?|!?!|!..|?..] *[–|-][–|-]'.format(tiny_clean=tiny_clean), paragraph)
                                                            if len(full_replica) != 0:
                                                                inside_new_replica = re.findall('[А-Я].*?: *[–|-][–|-]', full_replica[0])
                                                                if len(inside_new_replica) != 0:
                                                                    several_sentences = re.split('\?|!|\.|\.\.\.|…|\.\.|\!\?|\?!|\?!\?|!\?!|!\.\.|\?\.\.', inside_new_replica[0])
                                                                    several_sentences_clean = several_sentences[len(several_sentences)-1].replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                                                    prefinal = re.findall('{tiny_clean}.*?(?={several_sentences_clean})'.format(tiny_clean=tiny_clean, several_sentences_clean=several_sentences_clean), full_replica[0])
                                                                    new_direct_indirect = re.findall('[(!)+|(?)+|,|.|...|…|..|!?|?!|?!?|!?!|!..|?..] *[–|-][–|-] *\w.*', prefinal[0])
                                                                    if len(new_direct_indirect) != 0:
                                                                        first_new_direct_indirect = re.findall('[–|-][–|-] *\w.*', new_direct_indirect[0])
                                                                        first_new_direct_indirect_clean = first_new_direct_indirect[0].replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                                                        final = re.findall('{tiny_clean}.*?(?={first_new_direct_indirect_clean})'.format(tiny_clean=tiny_clean, first_new_direct_indirect_clean=first_new_direct_indirect_clean), full_replica[0])
                                                                        # final
                                                                        dialogue = dialogue + final
                                                                    else:
                                                                        final = prefinal
                                                                        # final
                                                                        dialogue = dialogue + final
                                                                else:
                                                                    new_direct_indirect = re.findall('[(!)+|(?)+|,|.|...|…|..|!?|?!|?!?|!?!|!..|?..] *[–|-][–|-] *\w.*', full_replica[0])
                                                                    if len(new_direct_indirect) != 0:
                                                                        first_new_direct_indirect = re.findall('[–|-][–|-] *\w.*', new_direct_indirect[0])
                                                                        first_new_direct_indirect_clean = first_new_direct_indirect[0].replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                                                        final = re.findall('{tiny_clean}.*?(?={first_new_direct_indirect_clean})'.format(tiny_clean=tiny_clean, first_new_direct_indirect_clean=first_new_direct_indirect_clean), full_replica[0])
                                                                        # final
                                                                        dialogue = dialogue + final
                                                                    else:
                                                                        # final
                                                                        final = full_replica
                                                                        dialogue = dialogue + final
                                                            else:
                                                                tiny_last_char = tiny[-1]
                                                                if tiny_last_char == ',':
                                                                    # final
                                                                    final = re.findall('{tiny_clean}.*?[(!)+|(?)+|.|...|…|..|!?|?!|?!?|!?!|!..|?..]'.format(tiny_clean = tiny_clean), paragraph)
                                                                    dialogue = dialogue + final
                                                                else:
                                                                    # final
                                                                    final = []
                                                                    final.append(tiny)
                                                                    dialogue.append(tiny)
                                                            # find replicas after the final 
                                                            final_edited = re.findall('[А-Я].*', final[0])
                                                            final_edited = final_edited[0].replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                                            next_till_colon = re.findall('{final_edited}.*?: *[–|-][–|-]'.format(final_edited=final_edited), paragraph)
                                                            if len(next_till_colon) != 0:
                                                                next_replicas = re.findall('[(!)+|(?)+|,|.|...|…|..|!?|?!|?!?|!?!|!..|?..] *[–|-][–|-] *[А-Я].*?[(!)+|(?)+|,|.|...|…|..|!?|?!|?!?|!?!|!..|?..] *[–|-][–|-]', next_till_colon[0])
                                                                if len(next_replicas) != 0:
                                                                    # add new
                                                                    dialogue = dialogue + next_replicas
                                                                    next_replicas_last = next_replicas[len(next_replicas)-1].replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                                                    last_before_colon = re.findall('(?<={next_replicas_last}) *[А-Я].*?[(!)+|(?)+|.|...|…|..|!?|?!|?!?|!?!|!..|?..]'.format(next_replicas_last=next_replicas_last), next_till_colon[0])
                                                                    if len(last_before_colon) != 0:
                                                                        # add the last replica
                                                                        dialogue = dialogue + last_before_colon
                                                            else:
                                                                next_till_para = re.findall('{final_edited}.*'.format(final_edited=final_edited), paragraph)
                                                                next_replicas = re.findall('[(!)+|(?)+|,|.|...|…|..|!?|?!|?!?|!?!|!..|?..] *[–|-][–|-] *[А-Я].*?[(!)+|(?)+|,|.|...|…|..|!?|?!|?!?|!?!|!..|?..] *[–|-][–|-]', next_till_para[0])
                                                                if len(next_replicas) != 0:
                                                                    # add new
                                                                    dialogue = dialogue +next_replicas
                                                                    next_replicas_last = next_replicas[len(next_replicas)-1].replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                                                    last_before_para = re.findall('(?<={next_replicas_last}) *[А-Я].*?[(!)+|(?)+|.|...|…|..|!?|?!|?!?|!?!|!..|?..]'.format(next_replicas_last=next_replicas_last), next_till_para[0])
                                                                    if len(last_before_para) != 0:
                                                                        # add the last replica
                                                                        dialogue = dialogue + last_before_para
                                                    # replicas starting with : -
                                                    else:
                                                        tiny_replica = re.findall(': *– *[А-Я].*?[(!)+|(?)+|,|.|...|…|..|!?|?!|?!?|!?!|!..|?..]', paragraph)
                                                        if len(tiny_replica) != 0:
                                                            for tiny in tiny_replica:
                                                                tiny_clean = tiny.replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                                                full_replica = re.findall('{tiny_clean}.*?[(!)+|(?)+|,|.|...|…|..|!?|?!|?!?|!?!|!..|?..] *–'.format(tiny_clean=tiny_clean), paragraph)
                                                                if len(full_replica) != 0:
                                                                    inside_new_replica = re.findall('[А-Я].*?: *–', full_replica[0])
                                                                    if len(inside_new_replica) != 0:
                                                                        several_sentences = re.split('\?|!|\.|\.\.\.|…|\.\.|\!\?|\?!|\?!\?|!\?!|!\.\.|\?\.\.', inside_new_replica[0])
                                                                        several_sentences_clean = several_sentences[len(several_sentences)-1].replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                                                        prefinal = re.findall('{tiny_clean}.*?(?={several_sentences_clean})'.format(tiny_clean=tiny_clean, several_sentences_clean=several_sentences_clean), full_replica[0])
                                                                        new_direct_indirect = re.findall('[(!)+|(?)+|,|.|...|…|..|!?|?!|?!?|!?!|!..|?..] *– *\w.*', prefinal[0])
                                                                        if len(new_direct_indirect) != 0:
                                                                            first_new_direct_indirect = re.findall('– *\w.*', new_direct_indirect[0])
                                                                            first_new_direct_indirect_clean = first_new_direct_indirect[0].replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                                                            final = re.findall('{tiny_clean}.*?(?={first_new_direct_indirect_clean})'.format(tiny_clean=tiny_clean, first_new_direct_indirect_clean=first_new_direct_indirect_clean), full_replica[0])
                                                                            # final
                                                                            dialogue = dialogue + final
                                                                        else:
                                                                            final = prefinal
                                                                            # final
                                                                            dialogue = dialogue + final
                                                                    else:
                                                                        new_direct_indirect = re.findall('[(!)+|(?)+|,|.|...|…|..|!?|?!|?!?|!?!|!..|?..] *– *\w.*', full_replica[0])
                                                                        if len(new_direct_indirect) != 0:
                                                                            first_new_direct_indirect = re.findall('– *\w.*', new_direct_indirect[0])
                                                                            first_new_direct_indirect_clean = first_new_direct_indirect[0].replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                                                            final = re.findall('{tiny_clean}.*?(?={first_new_direct_indirect_clean})'.format(tiny_clean=tiny_clean, first_new_direct_indirect_clean=first_new_direct_indirect_clean), full_replica[0])
                                                                            # final
                                                                            dialogue = dialogue + final
                                                                        else:
                                                                            # final
                                                                            final = full_replica
                                                                            dialogue = dialogue + final
                                                                else:
                                                                    tiny_last_char = tiny[-1]
                                                                    if tiny_last_char == ',':
                                                                        # final
                                                                        final = re.findall('{tiny_clean}.*?[(!)+|(?)+|.|...|…|..|!?|?!|?!?|!?!|!..|?..]'.format(tiny_clean = tiny_clean), paragraph)
                                                                        dialogue = dialogue + final
                                                                    else:
                                                                        # final
                                                                        final = []
                                                                        final.append(tiny)
                                                                        dialogue.append(tiny)
                                                                # find replicas after the final 
                                                                final_edited = re.findall('[А-Я].*', final[0])
                                                                final_edited = final_edited[0].replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                                                next_till_colon = re.findall('{final_edited}.*?: *–'.format(final_edited=final_edited), paragraph)
                                                                if len(next_till_colon) != 0:
                                                                    next_replicas = re.findall('[(!)+|(?)+|,|.|...|…|..|!?|?!|?!?|!?!|!..|?..] *– *[А-Я].*?[(!)+|(?)+|,|.|...|…|..|!?|?!|?!?|!?!|!..|?..] *–', next_till_colon[0])
                                                                    if len(next_replicas) != 0:
                                                                        # add new
                                                                        dialogue = dialogue + next_replicas
                                                                        next_replicas_last = next_replicas[len(next_replicas)-1].replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                                                        last_before_colon = re.findall('(?<={next_replicas_last}) *[А-Я].*?[(!)+|(?)+|.|...|…|..|!?|?!|?!?|!?!|!..|?..]'.format(next_replicas_last=next_replicas_last), next_till_colon[0])
                                                                        if len(last_before_colon) != 0:
                                                                            # add the last replica
                                                                            dialogue = dialogue + last_before_colon
                                                                else:
                                                                    next_till_para = re.findall('{final_edited}.*'.format(final_edited=final_edited), paragraph)
                                                                    next_replicas = re.findall('[(!)+|(?)+|,|.|...|…|..|!?|?!|?!?|!?!|!..|?..] *– *[А-Я].*?[(!)+|(?)+|,|.|...|…|..|!?|?!|?!?|!?!|!..|?..] *–', next_till_para[0])
                                                                    if len(next_replicas) != 0:
                                                                        # add new
                                                                        dialogue = dialogue +next_replicas
                                                                        next_replicas_last = next_replicas[len(next_replicas)-1].replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                                                        last_before_para = re.findall('(?<={next_replicas_last}) *[А-Я].*?[(!)+|(?)+|.|...|…|..|!?|?!|?!?|!?!|!..|?..]'.format(next_replicas_last=next_replicas_last), next_till_para[0])
                                                                        if len(last_before_para) != 0:
                                                                            # add the last replica
                                                                            dialogue = dialogue + last_before_para
                                                        else:
                                                        # replicas starting with : -
                                                            tiny_replica = re.findall(': *- *[А-Я].*?[(!)+|(?)+|,|.|...|…|..|!?|?!|?!?|!?!|!..|?..]', paragraph)
                                                            if len(tiny_replica) != 0:
                                                                for tiny in tiny_replica:
                                                                    tiny_clean = tiny.replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                                                    full_replica = re.findall('{tiny_clean}.*?[(!)+|(?)+|,|.|...|…|..|!?|?!|?!?|!?!|!..|?..] *-'.format(tiny_clean=tiny_clean), paragraph)
                                                                    if len(full_replica) != 0:
                                                                        inside_new_replica = re.findall('[А-Я].*?: *-', full_replica[0])
                                                                        if len(inside_new_replica) != 0:
                                                                            several_sentences = re.split('\?|!|\.|\.\.\.|…|\.\.|\!\?|\?!|\?!\?|!\?!|!\.\.|\?\.\.', inside_new_replica[0])
                                                                            several_sentences_clean = several_sentences[len(several_sentences)-1].replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                                                            prefinal = re.findall('{tiny_clean}.*?(?={several_sentences_clean})'.format(tiny_clean=tiny_clean, several_sentences_clean=several_sentences_clean), full_replica[0])
                                                                            new_direct_indirect = re.findall('[(!)+|(?)+|,|.|...|…|..|!?|?!|?!?|!?!|!..|?..] *- *\w.*', prefinal[0])
                                                                            if len(new_direct_indirect) != 0:
                                                                                first_new_direct_indirect = re.findall('- *\w.*', new_direct_indirect[0])
                                                                                first_new_direct_indirect_clean = first_new_direct_indirect[0].replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                                                                final = re.findall('{tiny_clean}.*?(?={first_new_direct_indirect_clean})'.format(tiny_clean=tiny_clean, first_new_direct_indirect_clean=first_new_direct_indirect_clean), full_replica[0])
                                                                                # final
                                                                                dialogue = dialogue + final
                                                                            else:
                                                                                final = prefinal
                                                                                # final
                                                                                dialogue = dialogue + final
                                                                        else:
                                                                            new_direct_indirect = re.findall('[(!)+|(?)+|,|.|...|…|..|!?|?!|?!?|!?!|!..|?..] *- *\w.*', full_replica[0])
                                                                            if len(new_direct_indirect) != 0:
                                                                                first_new_direct_indirect = re.findall('- *\w.*', new_direct_indirect[0])
                                                                                first_new_direct_indirect_clean = first_new_direct_indirect[0].replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                                                                final = re.findall('{tiny_clean}.*?(?={first_new_direct_indirect_clean})'.format(tiny_clean=tiny_clean, first_new_direct_indirect_clean=first_new_direct_indirect_clean), full_replica[0])
                                                                                # final
                                                                                dialogue = dialogue + final
                                                                            else:
                                                                                # final
                                                                                final = full_replica
                                                                                dialogue = dialogue + final
                                                                    else:
                                                                        tiny_last_char = tiny[-1]
                                                                        if tiny_last_char == ',':
                                                                            # final
                                                                            final = re.findall('{tiny_clean}.*?[(!)+|(?)+|.|...|…|..|!?|?!|?!?|!?!|!..|?..]'.format(tiny_clean = tiny_clean), paragraph)
                                                                            dialogue = dialogue + final
                                                                        else:
                                                                            # final
                                                                            final = []
                                                                            final.append(tiny)
                                                                            dialogue.append(tiny)
                                                                    # find replicas after the final 
                                                                        final_edited = re.findall('[А-Я].*', final[0])
                                                                        final_edited = final_edited[0].replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                                                        next_till_colon = re.findall('{final_edited}.*?: *-'.format(final_edited=final_edited), paragraph)
                                                                        if len(next_till_colon) != 0:
                                                                            next_replicas = re.findall('[(!)+|(?)+|,|.|...|…|..|!?|?!|?!?|!?!|!..|?..] *- *[А-Я].*?[(!)+|(?)+|,|.|...|…|..|!?|?!|?!?|!?!|!..|?..] *-', next_till_colon[0])
                                                                            if len(next_replicas) != 0:
                                                                                # add new
                                                                                dialogue = dialogue + next_replicas
                                                                                next_replicas_last = next_replicas[len(next_replicas)-1].replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                                                                last_before_colon = re.findall('(?<={next_replicas_last}) *[А-Я].*?[(!)+|(?)+|.|...|…|..|!?|?!|?!?|!?!|!..|?..]'.format(next_replicas_last=next_replicas_last), next_till_colon[0])
                                                                                if len(last_before_colon) != 0:
                                                                                    # add the last replica
                                                                                    dialogue = dialogue + last_before_colon
                                                                        else:
                                                                            next_till_para = re.findall('{final_edited}.*'.format(final_edited=final_edited), paragraph)
                                                                            next_replicas = re.findall('[(!)+|(?)+|,|.|...|…|..|!?|?!|?!?|!?!|!..|?..] *- *[А-Я].*?[(!)+|(?)+|,|.|...|…|..|!?|?!|?!?|!?!|!..|?..] *-', next_till_para[0])
                                                                            if len(next_replicas) != 0:
                                                                                # add new
                                                                                dialogue = dialogue +next_replicas
                                                                                next_replicas_last = next_replicas[len(next_replicas)-1].replace('.','\.').replace('?','\?').replace('*','\*').replace('+','\+').replace('(','\(').replace(')','\)').replace('[','\[').replace(']','\]')
                                                                                last_before_para = re.findall('(?<={next_replicas_last}) *[А-Я].*?[(!)+|(?)+|.|...|…|..|!?|?!|?!?|!?!|!..|?..]'.format(next_replicas_last=next_replicas_last), next_till_para[0])
                                                                                if len(last_before_para) != 0:
                                                                                    # add the last replica
                                                                                    dialogue = dialogue + last_before_para


    # extract author's name
    index_author = text.index('.')
    author = text[:index_author]
    authors.append(author)

    # extract book title 
    index_title = text.rindex('.')
    title = text[index_author+1:index_title]
    books.append(title)

    # book wordcount
    book_split = book_text.split(' ')
    book_words = 0
    for word in book_split:
        letters = re.findall('\w', word)
        if len(letters) != 0:
            book_words += 1
    book_wordcount.append(book_words)

    # dialogues
    dialogues.append(dialogue)

    #dialogues word count
    all_dialogues = ' '.join(dialogue)
    dialogues_split = all_dialogues.split(' ')
    dialogue_words = 0
    for word in dialogues_split:
        letters = re.findall('\w', word)
        if len(letters) != 0:
            dialogue_words += 1
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
