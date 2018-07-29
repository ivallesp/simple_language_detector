# Simple language detection system

This repository contains a very simple language detection system which is applied to differentiate between sentences in three different languages

- Afrikaans
- Dutch
- English

This is a supervised learning problem for which a labeled dataset has been provided (it can be found in the data folder). A frequentist approach has been chosen as a good candidate to solve this problem. Two families of features have been generated

- Tf-Idf features extracted from the content of the sentences provided in the dataset
- External corpora for each of the languages. For each sentence in the dataset, the proportion of words appearing in each of the corpora has been measured. The corpora are build from samples of afrikaans, dutch and english wikipedia dumps.

ExtraTrees has been selected as the supervised learning model to perform the classification.

With this setting, the results achieved are the following ones.

`
=============== Results Training set ===============
Accuracy: 0.972757162987318

             precision    recall  f1-score   support

  Afrikaans       0.93      1.00      0.97       470
    English       0.99      0.99      0.99      1544
 Nederlands       0.97      0.57      0.72       115

avg / total       0.97      0.97      0.97      2129

===================================================

 -- 	 -- 	 -- 	 -- 	 -- 	 -- 	 --

================= Results Test set ================
Accuracy: 0.956338028169014

             precision    recall  f1-score   support

  Afrikaans       0.92      0.94      0.93       163
    English       0.98      0.99      0.99       513
 Nederlands       0.70      0.47      0.56        34

avg / total       0.95      0.96      0.95       710

===================================================
` 

These results can be reproduced following the code in the jupyter notebook located in `notebooks/example.ipynb`. To be able to run it, settings.json needs to be filled with the project paths and Python 3 with all the required libraries (pandas, numpy, scikit-learn,...) must be installed.

If there is any doubt or need for clarification, write to `ivanvallesperez[at]gmail.com`.