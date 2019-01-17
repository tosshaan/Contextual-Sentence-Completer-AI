# Contextual Sentence Completer 
This is an interactive Python application that actively infers category of user text input and suggests up to 5 words based on context It uses an algorithm for context/category inference by merging Naive Bayes Document Classifier with a custom weighted algorithm The word suggestion algorithm using n-gram probabilities such that the user can select weights themselves to further customize prediction

The user can continuously type input into the program. At any time, there are two actions they can request from the program. The first is to infer the category of the text entered so far. There are five categories: business, entertainment, politics, sport and technology. The second is to generate suggestions for next words (up to five) in the current sentence. These suggestions are based on the inferred category: each category has its separate corpus which is used to compute the probability of the n-grams (from 1 to 5). The program uses a weighted average of the n-grams to calculate the probability, and the user can chose to modify the weights of each gram in order to experiment and get different results. We use BBC articles (https://www.kaggle.com/yufengdev/bbc-fulltext-and-category) as our corpus. The articles are separated in the categories mentioned above. All the texts are in lowercase, and we removed punctuation for simplicity.

Data set used: https://www.kaggle.com/yufengdev/bbc-fulltext-and-category

Libraries used:

Pandas (https://pandas.pydata.org/): We used pandas to import the dataset and create the files with precomputed n-grams probabilities
Tkinter (https://wiki.python.org/moin/TkInter): As described in implementation, Tkinter, a standard GUI Python library, was used to implement the user interface.
