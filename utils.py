def status_matcher(QA_tokens:list, representative_words:dict) -> result:dict:
    # 생성된 Q, A의 단어들을 words와 매치​
    # # 몇 개가 매치되었느냐? (각 status 별로)를 리턴​
    result = {}
    status = representative_words.keys()

    for s in status:
        target_list = representative_words[s]
        total_count = 0
        for word in target_list:
            total_count = total_count + QA_tokens.count(word)
        result[s] = total_count

    return result

# clean the text (tokenize, lower the case, remove the punctuations and stopwords)
def clean_text(text:str, stops:set) -> str:
    tokens = word_tokenize(text)                     # tokenize the words
    tokens = [w.lower() for w in tokens]             # lower the case
    tokens = [w for w in tokens if w.isalpha()]      # remove the punctuations
    tokens = [w for w in tokens if not w in stops]   # remove stopwords
    return tokens