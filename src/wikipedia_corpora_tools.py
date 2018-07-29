import os
import json
import numpy as np
import codecs
import warnings
from src.common_paths import get_data_path, get_external_data_path
from src.text_tools import simple_tokenizer, canonize_language, strip_accents
from src.utilities import flatten
from collections import Counter
from sklearn.base import BaseEstimator, TransformerMixin
from src.text_tools import *



class WikipediaDfGenerator(BaseEstimator, TransformerMixin):
    """
    Feature generator compatible with scikit-learn. It is intended to be directly used as a piece
    of a sklearn.pipeline. Generates a feature containing the proportion of known words given a language
    corpora
    
    Methods:
    __init__: Initializes the feature generator
        :param wiki_name: name of the wikipedia to be used. It will be used later to build the path to find it (str)
        :param max_chunks: maximum number of wikipedia chunks to load (str)
        :param min_token_length: minimum number of word occurences to consider it (int)
        :return: None (Void)
    fit: generates the wikipedia dictionary
        :param X: dummy parameter (required by sklearn). As this is an unsupervised and not data dependent process, 
        this parameter is required but not used
        :param y: dummy parameter (required by sklearn). As this is an unsupervised and not data dependent process, 
        this parameter is required but not used
    transform: generates the features required as a np.matrix
        :param X: sentences to be converted (list of str)
        :return: vector space containing the proportion of recognized words (np.matrix)
    """
    def __init__(self, wiki_name, max_chunks, min_token_length=2):
        self.wiki_name = wiki_name
        self.max_chunks = max_chunks
        self.min_token_length = min_token_length
        self.df_dict = None

    def fit(self, X, y):
        df_dict = generate_wikipedia_df_dictionary(wiki_name=self.wiki_name, max_chunks=self.max_chunks,
                                                   min_token_length=self.min_token_length)
        self.df_dict = df_dict
        return self

    def transform(self, X):
        df_dict = self.df_dict
        tokens = list(map(lambda x:simple_tokenizer(canonize_language(x), min_token_length=2), X))
        df_aggregated = list(map(lambda sentence:np.sum(list(map(lambda x:df_dict.get(x, 0), sentence)))/float(len(sentence)), tokens))
        return np.transpose(np.matrix(df_aggregated)) 

    
def generate_wikipedia_df_dictionary(wiki_name, max_chunks, min_token_length=3):
    """
    Calculates a dictionary with the number of times a word appears in the wikipedia articles. The hapaxes and
    least frequent words have been removed
    :param wiki_name: name of the wikipedia to be used. It will be used later to build the path to find it (str)
    :param max_chunks: maximum number of wikipedia chunks to load (str)
    :param min_token_length: minimum number of word occurences to consider it (int)
    :return: dictionary of word occurrences (collections.Counter)
    """
    articles_generator = wiki_chunk_generator(wiki_name=wiki_name, max_chunks=max_chunks)
    unique_words_by_article = list(map(lambda article:list(set(simple_tokenizer(canonize_language(article["text"]), min_token_length=min_token_length))), articles_generator))
    df_dict = Counter(flatten(unique_words_by_article))
    return df_dict

    
def wiki_chunk_generator(wiki_name, max_chunks):
    """
    Generator that feeds other methods with wikipedia articles. 
    :param wiki_name: name of the wikipedia to be used. It will be used later to build the path to find it (str)
    :param max_chunks: maximum number of wikipedia chunks to load (str)
    :return: yields a wikipedia article at a time (str)
    """
    c=0
    print("Loading wikipedia language: {}".format(wiki_name))
    path = os.path.join(get_external_data_path(), "wikipedia", wiki_name)
    path_walker = os.walk(path)
    for (step_path, folders, filenames) in path_walker:
        for filename in filenames:
            if "wiki" in filename:
                c += 1
                if c <= max_chunks or max_chunks==-1:
                    file_stream = codecs.open(os.path.join(step_path, filename), "r", "utf-8")
                    for i,x in enumerate(file_stream):
                        try:
                            yield json.loads(str(x))
                        except:
                            warnings.warn("Not able to decode article NO {} in json: {}".format(i, os.path.join(step_path, filename)))
