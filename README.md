# sdp-vocab-selector
To select vocabularies that represents PPI status of the deal represented in the article

- final_results.tsv: a list of body texts and its covering deal status extracted from the original news articles
- vocabcounter.py: a program that counts the number of appearance of each vocabulary from the texts listed in final_results.tsv
- word_counted.tsv: a result created after the execution of vocabcounter.py
- 0829_find_representative_words.ipynb: 4 different attempts to figure out the representative vocabularies of each deal status based on the result written in word_counted.tsv
