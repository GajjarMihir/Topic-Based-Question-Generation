import nltk
import json
import tensorflow as tf
import numpy as np

import fully_connected_neural_network as FC

from nltk.corpus import stopwords				# used for removing the stop words such as "is", "the".
from nltk.tokenize import RegexpTokenizer		# for tokenizing the sentence and removing the punctuation marks.
from numpy import asarray						# For doing vectorized operations.
from sklearn.metrics.pairwise import cosine_similarity # In-built function for calculating the cosine similarity.

path = 'Add the path to the data here'		# The path containing the filtered data.

# Reading the filtered questions and answers.
with open(path + 'QA_Video_Games_questions.json') as json_file:  
    Questions = json.load(json_file)
with open(path + 'QA_Video_Games_answers.json') as json_file:  
    Answers = json.load(json_file)

# Extracting the topic for the question-answer pairs.
embeddings_index = dict()
f = open('glove.6B.300d.txt')
for line in f:
	indiv_values = line.split()
	word = indiv_values[0]
	vect_val = asarray(indiv_values[1:], dtype='float32')
	embeddings_index[word] = vect_val
f.close()
print('Loaded %s word vectors.' % len(embeddings_index))

K = 0.5                             # The final threshold for the averaging the individual sum.
thres_lambda = 0.4                  # Threshold for the cosine_similarity of the individual words.
indivSum = 0                        # For the addition of the (votes*cosine_similarity) for a particular token in the answer vector.
vote = 0                            # Vote for a particular token in the answer vector.
total_vote = 0                      # The total number of votes for a particular token in the answer vector.
Topics = []							# Contains the topic(s) for all the question-answer pairs.

def bin_vote(vw1, vw2):
    if ( cosine_similarity(vw1, vw2) > thres_lambda ):
        return 1
    else:
        return 0

for pairindex in range(len(Questions)):
	Sum = []                            # Contains the addition of all the (votes*cosine_similarity) for all the individual tokens in the answer vector.
	vote_count = []                     # Contains the total votes for all the individual tokens in the answer.
	Average_Sum = []                    # Contains the average for all the individual tokens in the answer.
	Topic = []                          # The topic(s) for the given question-answer pair.
	for ansindex in range(len(Answers[pairindex][0])):
		answord = Answers[pairindex][0][ansindex].lower()  # Because currently I have glove embeddings which are uncased.
		vw1 = embeddings_index[answord]
		vw1 = vw1.reshape(1,-1)
		for quesindex in range(len(Questions[pairindex])):
			quesword = Questions[pairindex][quesindex].lower()
			vw2 = embeddings_index[quesword]
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
	Topics.append(Topic)

# Questions which are extracted from the Question-Answer Pairs.
Questions_Types_embedding = []
Questions_Types = ["Can", "What", "Who", "How", "Where", "Why"]

for i in range(len(Questions_Types)):
	Questions_Types_embedding.append(embeddings_index[Questions_Types[i].lower()])

		


#Question Type Encoder
# Here I have to pass these Question types embeddings e_ti to the fully connected neural network to get the internal vector representation qt_i
Topic_internal_vector = FC(Questions_Types_embedding,7)



# Number of hidden units.
from tensorflow.python.ops.rnn_cell import BasicLSTMCell

encoder_hidden_units = 600
decoder_hidden_units = 600


# BLSTM Encoder encoding the Question Topic
forward_topics_encoder_cell = BasicLSTMCell(encoder_hidden_units)
backward_topics_encoder_cell = BasicLSTMCell(encoder_hidden_units)

((encoder_topics_fw_outputs,			# Contains the outputs of the BLSTM.
  encoder_topics_bw_outputs),			
 (encoder_topics_fw_final_state,		# Contains the last hidden state of the BLSTM.
  encoder_topics_bw_final_state)) = (
    tf.nn.bidirectional_dynamic_rnn(cell_fw = forward_topics_encoder_cell,
    								cell_bw = backward_topics_encoder_cell,
    								inputs = Topics,  							# Topics
    								dtype = tf.float32, time_major = True)
  )

# Concatenating the output and the final hidden state of the forward and the backward propagation.
encoder_topics_outputs = tf.concat((encoder_topics_fw_outputs, encoder_topics_bw_outputs), 0)
encoder_topics_final_state = tf.concat((encoder_topics_fw_final_state, encoder_topics_bw_final_state), 0)


# BLSTM Encoder for encoding the answer
forward_answers_encoder_cell = BasicLSTMCell(encoder_hidden_units)
backward_answers_encoder_cell = BasicLSTMCell(encoder_hidden_units)

((encoder_answers_fw_outputs,
  encoder_answers_bw_outputs),
 (encoder_answers_fw_final_state,
  encoder_answers_bw_final_state)) = (
    tf.nn.bidirectional_dynamic_rnn(cell_fw = forward_answers_encoder_cell,
    								cell_bw = backward_answers_encoder_cell,
    								inputs = Answers,							# Answers.
    								dtype = tf.float32, time_major = True)
  )

# Concatenating the output and the final hidden state of the forward and the backward propagation.
encoder_answers_outputs = tf.concat((encoder_answers_fw_outputs, encoder_answers_bw_outputs), 0)
encoder_answers_final_state = tf.concat((encoder_answers_fw_final_state, encoder_answers_bw_final_state), 0)

# Concatenating the final hidden state of both the question type and answer encoder to initialize the decoder.
both_encoders_outputs = tf.concat((encoder_topics_outputs, encoder_answers_outputs), 0)
both_encoders_final_state = tf.concat((encoder_topics_final_state, encoder_answers_final_state), 0)




decoder_cell = tf.nn.rnn_cell.BasicLSTMCell(decoder_hidden_units)

# Decoder:
attention_states = tf.transpose(both_encoders_outputs, [1, 0, 2]) # The encoder has time_major = True which means that the format is time_major but for the attention we need it in batch major hence we are doing the transpose of the first two dimensions.
attention_mechanism = tf.contrib.seq2seq.LuongAttention(
	decoder_hidden_units, attention_states, memory_sequence_length = source_sequence_length) # passing the source sequence length to ensure that the attention weights are properly normalized.
decoder_cell = tf.contrib.seq2seq.AttentionWrapper(
	decoder_cell,attention_mechanism,attention_layer_size = decoder_hidden_units)
# helper
decoder = tf.contrib.seq2seq.BasicDecoder(decoder_cell,both_encoders_final_state)
(decoder_final_outputs, decoder_final_state, decoder_final_sequence_lengths) = tf.contrib.seq2seq.dynamic_decode(decoder)








