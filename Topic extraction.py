import nltk     # used for separating the words from the sentence.
import numpy as np
from numpy import asarray
from sklearn.metrics.pairwise import cosine_similarity # In-built function for calculating the cosine similarity.

# load the whole embedding into memory
embeddings_index = dict()
f = open('glove.6B.300d.txt')
for line in f:
	indiv_values = line.split()
	word = indiv_values[0]
	vect_val = asarray(indiv_values[1:], dtype='float32')
	embeddings_index[word] = vect_val
f.close()
print('Loaded %s word vectors.' % len(embeddings_index))

# Example Question-Answer pair
Question = "why did you go to america?"
Answer = "i visited america for a meeting."

# Yet to implement:
# Remove the prepositions and the punctutation marks and the words like "is", "for" because their chances of being the topic is almost zero.
# can us nltk stop words for that.

K = 0.5                             # The final threshold for the averaging the individual sum.
thres_lambda = 0.4                  # Threshold for the cosine_similarity of the individual words.
indivSum = 0                        # For the addition of the (votes*cosine_similarity) for a particular token in the answer vector.
vote = 0                            # Vote for a particular token in the answer vector.
total_vote = 0                      # The total number of votes for a particular token in the answer vector.
Sum = []                            # Contains the addition of all the (votes*cosine_similarity) for all the individual tokens in the answer vector.
vote_count = []                     # Contains the total votes for all the individual tokens in the answer.
Average_Sum = []                    # Contains the average for all the individual tokens in the answer.
Topic = []                          # The topic(s) for the given question-answer pair.

# Tokenizing the given question and answer.
tokenized_question = nltk.word_tokenize(Question)  
tokenized_answer = nltk.word_tokenize(Answer)

# Deciding whether the vote should be counted or not based on the similarity between the two words using a threshold value lambda.
def bin_vote(vw1, vw2):
    if ( cosine_similarity(vw1, vw2) > thres_lambda ):
        return 1
    else:
        return 0

# Calculating the votes and (votes*cosine_similarity) for the tokens in the answer.
for ansindex,word in enumerate(tokenized_answer):
    vw1 = embeddings_index[tokenized_answer[ansindex]]
    vw1 = vw1.reshape(1,-1)
    for quesindex,word in enumerate(tokenized_question):
        vw2 = embeddings_index[tokenized_question[quesindex]]
        vw2 = vw2.reshape(1,-1)
        vote = bin_vote(vw1,vw2) 
        indivSum = indivSum + (vote * cosine_similarity(vw1, vw2))
        total_vote = total_vote + vote
    Sum.append(indivSum)
    vote_count.append(total_vote)
    total_vote = 0
    indivSum = 0

# Calculating the average vote for the tokens in the answer.
for i in range(len(Sum)):
    if(vote_count[i] != 0):
        Average_Sum.append(Sum[i] / vote_count[i])
    else:
        Average_Sum.append(0)

# Average_Sum = np.divide(Sum,vote_count) # For doing vector calculations to optimize the code.

# Deciding whether the token in the answer should be considered as a topic or not based on the threshold value K.
for i in range(len(Sum)):
    if(Average_Sum[i] > K):
        Topic.append(tokenized_answer[i])

# Displaying the best possible topic(s) for the given question-answer pair.
print Topic
