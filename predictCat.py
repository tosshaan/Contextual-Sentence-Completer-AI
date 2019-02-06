import pandas as pd

data = pd.read_csv('bbc-text.csv')
catList = ['business', 'entertainment', 'politics', 'sport', 'tech']
# count of documents of each category
catCount = [0]*5
# number of rows in dataframe
totalCount = len(data.index)
for row in data.itertuples():
	ind = catList.index(getattr(row, "category"))
	catCount[ind] += 1 
# proportion of each category
catProportion = [count/totalCount for count in catCount] 

# calculate proportion of a word in docs of a given category
def propWordGivenCat(word, cat):
	count = 0
	for row in data.itertuples():
		if (getattr(row, "category") == cat) and (word in getattr(row, "text").split(" ")):
			count += 1

	return count/catCount[catList.index(cat)]

def posteriorProbNum(words, cat):
	prod = 1
	for word in words.split(" "):
		prod *= propWordGivenCat(word, cat)

	numerator = catProportion[catList.index(cat)] * prod

	return numerator

def posteriorProbDenom(words):
	denom = 0
	for cat in catList:
		denom += posteriorProbNum(words, cat)

	return denom

# predict closest category based on given string of information using Naive Bayes' Classification
# Returns string corresponding to most probable category name
# Parameter: words needs to be lowercase
# (Possible concern: P = 0 if there's a certain word in given text that doesn't occur in any text related to the category)

def predictCategory(words):	
	# denom is just the normalization factor in the denominator of the formula
	denom = posteriorProbDenom(words)

	# final predictions probs for each category 
	probList = [posteriorProbNum(words, cat)/denom for cat in catList]
	print(probList)
	maxIndex = probList.index(max(probList))
	
	return(catList[maxIndex])
	
