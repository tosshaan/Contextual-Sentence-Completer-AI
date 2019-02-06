
# coding: utf-8

# In[1]:


from collections import defaultdict


# In[2]:


wordsFile = open('general/words.txt')
words = []
for word in wordsFile:
    words.append(word.split()[0])


# In[48]:


# creating dict with every category's nGram count distribution
def generate_categories_dict():
    categories = defaultdict()
    for category in ['general', 'business', 'entertainment', 'politics', 'sport', 'tech']:
        ngrams = []
        for n in ['uni', 'bi', 'tri', 'four', 'five']:
            if category == 'general':
                filename = f'{category}/{n}grams.txt'
            else:
                filename = f'{category}/{category}_{n}grams.txt'

            file = open(filename)

            ngramVector = []
            for l in file:
                if n == 'uni':
                    ngramVector.append(int(l))
                else:
                    ngramVector.append([int(x) for x in l.split()])
            file.close()

            # precomputing probabilities for unigrams
            if n == 'uni':
                uniSum = sum(ngramVector)
                ngramVector = [x/uniSum for x in ngramVector]

            ngrams.append(ngramVector)
        categories[category] = ngrams
    return categories


# In[4]:


def probsUnigram(categories, category):
    # Returns the category's unigram probabilities for every word
    return categories[category][0]


# In[29]:


def probsNGram(evidence, categories, category, words):
    # Returns the category's nGram probabilities for every nGrams
    evidenceWords = evidence.split()
    n = len(evidenceWords)
    if n > 4:
        n = 4
        evidenceWords = evidenceWords[:n]
    if any(word not in words for word in evidenceWords):
        return [['', 0]]
    corpus = categories[category][n]
    counts = [[words[v[n]], v[n+1]] for v in corpus if [words.index(e) for e in evidenceWords] == v[:n]]
    countsSum = sum([v[1] for v in counts])
    probabilities = [[v[0], v[1]/countsSum] for v in counts]
    return probabilities


# In[46]:


def probsNGram(evidence, categories, category, words):
    # Returns the category's nGram probabilities for every nGrams
    evidenceWords = evidence.split()
    n = len(evidenceWords)
    if n > 4:
        n = 4
        evidenceWords = evidenceWords[-n:]
    corpus = categories[category][n]
    try:
        counts = [[words[v[n]], v[n+1]] for v in corpus if [words.index(e) for e in evidenceWords] == v[:n]]
    except ValueError:
        return [['', 0]]
    countsSum = sum([v[1] for v in counts])
    probabilities = [[v[0], v[1]/countsSum] for v in counts]
    return probabilities


# In[19]:


def unigramProbability(word, probVector, words):
    # Returns the category's unigram probability for a specific word
    if word in words:
        return probVector[words.index(word)]
    else:
        return 0


# In[20]:


def nGramProbability(word, probVector):
    # Returns the category's nGram probability for a specific nGram
    prob = [v[1] for v in probVector if v[0] == word]
    if len(prob) == 0:
        return 0
    else:
        return prob[0]


# In[21]:


def mixedProb(word, words, uniDist, nGramsDists, lambdas):
    # Returs the mixed probability considering all nGrams
    mixed = lambdas[0]*unigramProbability(word, uniDist, words)
    for i in range(0, len(nGramsDists)):
        mixed += lambdas[i+1]*nGramProbability(word, nGramsDists[i])
    return mixed


# In[156]:


def predictNextWord(evidence, categories, category, probsUni, lambdas=[0.2]*5):
    # Predicts the next word given a reference text
    evidenceWords = evidence.split()
    n = len(evidenceWords)
    if n > 4:
        n = 4
        evidenceWords = evidenceWords[-n:]
    sumRelevantLambdas = sum(lambdas[:n+1])
    normLambda = [x/sumRelevantLambdas for x in lambdas[:n+1]]
    nGramsDists = []
    
    for i in range(1, n+1):
        newEvidence = ' '.join(evidenceWords[-i:])
        nGramsDists.append(probsNGram(newEvidence, categories, category, words))
    
    
    probabilities = []
    for word in words:
        mixed = mixedProb(word, words, probsUni, nGramsDists, normLambda)
        probabilities.append([word, mixed])
    
    
    probabilities = sorted(probabilities, key = lambda x:-x[1])
    return probabilities[0][0]


# In[165]:


def getAllPredictions(evidence, categories, category, probsUni, lambdas=[0.2]*5):
    # Returns the 3 most probable fivegrams
    recommendedWords = []
    newEvidence = evidence
    for i in range(0, 5):
        newWord = predictNextWord(newEvidence, categories, category, probsUnigram(categories, category))

        recommendedWords.append(newWord)
        print(newWord)
        newEvidence = ' '.join(newEvidence.split()[-3:] + [newWord])
    return recommendedWords


# In[131]:


def predictCategory(evidence, categories, words):
    categoriesV = ['business', 'entertainment', 'politics', 'sport', 'tech']
    categoriesProbs = [0]*5
    categoriesCounts = [0]*5
    for word in evidence.split():
        for i in range(1, len(categories)):
            uniProbs = probsUnigram(categories, categoriesV[i-1])
            wordProb = unigramProbability(word, uniProbs, words)
            if wordProb != 0:
                categoriesCounts[i-1] += 1
                categoriesProbs[i-1] += wordProb
    

    for i in range(0, len(categoriesProbs)):
        if categoriesCounts[i] != 0:
            categoriesProbs[i] *= categoriesCounts[i]

    return categoriesV[categoriesProbs.index(max(categoriesProbs))]