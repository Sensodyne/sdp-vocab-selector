# import packages and libraries
import pandas as pd
import numpy as np

# import nltk tools
import nltk
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from collections import Counter

# def body_normalization(body):
#   body = body.lower()
#   return body

# def word_split(body):
#   splitted_words = body.split()
#   return splitted_words

# def remove_stopwords(splitted_words, stopwords):
#   return [w for w in splitted_words if w not in stopwords]

# clean the text (tokenize, lower the case, remove the punctuations and stopwords)
def clean_text(text:str, stops:set) -> str:
    tokens = word_tokenize(text)                     # tokenize the words
    tokens = [w.lower() for w in tokens]             # lower the case
    tokens = [w for w in tokens if w.isalpha()]      # remove the punctuations
    tokens = [w for w in tokens if not w in stops]   # remove stopwords
    return tokens

def stemming_the_tokens(tokens) -> list:                   # stemming the tokens if needed
    snowball = SnowballStemmer("english")
    return [snowball.stem(w) for w in tokens]

  # count the frequency and find duplicates
def word_list_to_frequency(word_list) -> dict:
    word_freq = [word_list.count(w) for w in word_list]
    return dict(list(zip(word_list, word_freq)))

def word_list_remove_duplicates(word_list) -> list:
    word_set = set(word_list)
    word_list = list(word_set)
    return word_list

# generate columns of the result dataframe
def column_generator(df:pd.DataFrame, stops:set) -> list:
    new_column = []
    for i in range(len(df)):
        try:
            body = df.iloc[i]['body']
            tokens = clean_text(body, stops)
            word_list = word_list_remove_duplicates(tokens)
            
            new_column.extend(word_list)
        except:
            continue
    return word_list_remove_duplicates(new_column)

# generate dictionary of the frequency of the vocabularies
def frequency_dictionary_generator(df:pd.DataFrame, column:list, stops:set) -> dict:
    new_df = {}
    for i in range(len(df)):
        temp_row = df.iloc[i]
        status = temp_row['status']
        body = temp_row['body']

        # Tokenize the body text
        try:
            tokens = clean_text(body, stops)
        except:
            print("Tokenize error occcurred at row number", i)
            continue

        # Produce a dictionary of the word frequencies
        try:
            word_freq = word_list_to_frequency(tokens)       # word_freq: dict
        except:
            print("Cannot convert the tokens to frequency at row number", i)
            continue

        # Produce a list of words of the dictionary
        try:
            word_list = word_list_remove_duplicates(tokens)  # word_list: list
        except:
            print("Cannot produce word list at row number", i)
            continue
        
        # write the value 0 if the word did not appear
        try:
            word_freq_keys = word_freq.keys()
            for ele in column:
                if ele in word_freq_keys:
                    continue
                else:
                    word_freq[ele] = 0
        except:
            print("Cannot format the dictionary at row number", i)
            continue
        
        # write the result to a dictionary
        try:
            new_df[i] = [status, body, word_list, word_freq]
        except:
            print("Cannot write the result to the dictionary at row number", i)
            continue

        # if (len(column) != len(word_freq.keys())):
        #     print("Column and the keys are not matched.")
        # column_list = word_freq.keys()
        # df_example_columns = df_example.columns.tolist()
        # create_on = [x for x in column_list if x in df_example_columns]
    return new_df

# compose dataframe with the column and the dictionary
def dataframe_recomposer(tobe_column:list, tobe_df:dict) -> pd.DataFrame:
    df_recompose = {'deal_status': [], 'body_text': [], 'word_list': []}
    for j in tobe_column:
        df_recompose[j] = []

    for i in tobe_df:
        current_pack = tobe_df[i]
        # every elements in the word_freq
        df_recompose['deal_status'].append(current_pack[0])
        df_recompose['body_text'].append(current_pack[1])
        df_recompose['word_list'].append(current_pack[2])
        dict_keys = current_pack[3].keys()
        for j in tobe_column:
            if j in dict_keys:
                df_recompose[j].append(current_pack[3][j])
    return df_recompose

# count vocabs and return it as a dataframe
if __name__ == "__main__":
    # load stopwords
    stops = stopwords.words('english')
    
    # file path of the tsv file
    file_path = 'C:\\Users\\GLaDOS\\Documents\\SJ\\SDP\\Tech\\'
    read_file_name = 'final_result.tsv'
    write_file_name = 'word_counted.tsv'

    # read the input
    df = pd.read_csv(file_path + read_file_name, sep='\t')

    tobe_column = column_generator(df, stops)
    tobe_df = frequency_dictionary_generator(df, tobe_column, stops)
    df_to_compose = dataframe_recomposer(tobe_column, tobe_df)

    # produce the final dataframe
    df_final = pd.DataFrame.from_dict(df_to_compose)
    df_final.to_csv(file_path + write_file_name, index = False, sep = "\t")