import numpy as np
from functools import reduce
from enum import Enum
import re

class Models(Enum):
    word = 1
    n_gram = 2

class Naivebayes:
    def __init__(self, model:str, n:int|None= None) ->None:
        """
        Naives Bayes Model
        ----
        model:str can take two values: `n_gram` or `word`
        n:int where `n` is a integer greater than 1
        """
        self.model = model
        self.n = n
        assert self.model in Models._member_names_, "It is not in the model"
        if self.model == 'n_gram':
            assert isinstance(self.n, int), "`n` must be integer"
            assert self.n>1, "`n` must be greater than 1"

    def token(self, sentence: str) -> list:
        if self.model == 'n_gram':
            s = self.n
            n_gram_split = re.findall(r"(.{%s})"%s , sentence)
            return n_gram_split

        sentence_split = sentence.split()
        token_set = set(sentence_split)
        return list(token_set)

    def fit(self, data: np.ndarray, target: np.array) -> None:
        x = data.flatten()
        self.classes = np.unique(target)
        n_c, log_prior, big_doc, loglikelihood = {}, {}, {}, {}
        vocabulary = reduce(lambda a, b: a + b, [self.token(d) for d in x])

        for c in self.classes:
            n_doc = len(target)
            condition = target == c
            n_c[c] = sum(condition)
            log_prior[c] = np.log(n_c[c] / n_doc)    
            big_doc[c] = reduce(lambda a, b: a + b, [self.token(d) for d in x[condition]])
            loglikelihood[c] = {}

            uniq_doc, count_doc = np.unique(big_doc[c], return_counts=True)

            for word in vocabulary:
                
                if np.any(word == uniq_doc):
                    count = count_doc[uniq_doc == word][0]
                else:
                    count = 0
                temp = {word: np.log((count + 1) / (len(big_doc[c]) + len(set(vocabulary))))}
                loglikelihood[c].update(temp)

        self.log_prior, self.loglikelihood, self.vocabulary = log_prior, loglikelihood, vocabulary

    def predict(self, data: np.ndarray) -> np.ndarray:
        x = data.flatten()
        log_posterior = {}
        self.log_posterior_chosen = []
        results = []
        for sentence in x:
            word_test = self.token(sentence)

            for c in self.classes:
                log_posterior[c] = self.log_prior[c]    

                for word in word_test:

                    if word in self.vocabulary:
                        log_posterior[c] += self.loglikelihood[c][word]
                    else:
                        pass
            classes_posterior = np.array(tuple(log_posterior.keys()))
            log_posterior_final = np.array(tuple(log_posterior.values()))
            results.append(classes_posterior[np.argmax(log_posterior_final)])
            self.log_posterior_chosen.append(np.max(log_posterior_final))
        return np.array(results)



if __name__ == '__main__':
    nb = Naivebayes(model='word')
    

