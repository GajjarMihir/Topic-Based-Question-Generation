import tensorflow as tf

# Number of hidden units.
encoder_hidden_units = 600
decoder_hidden_units = 600

from tensorflow.python.ops.rnn_cell import BasicLSTMCell

# BLSTM Encoder encoding the Question Topic
forward_topics_encoder_cell = BasicLSTMCell(encoder_hidden_units)
backward_topics_encoder_cell = BasicLSTMCell(encoder_hidden_units)

((encoder_topics_fw_outputs,			# Contains the outputs of the BLSTM.
  encoder_topics_bw_outputs),			
 (encoder_topics_fw_final_state,		# Contains the last hidden state of the BLSTM.
  encoder_topics_bw_final_state)) = (
    tf.nn.bidirectional_dynamic_rnn(cell_fw = forward_topics_encoder_cell,
    								cell_bw = backward_topics_encoder_cell,
    								inputs = encoder_inputs_topics_embedded,  # embedded topics.
    								dtype = tf.float32, time_major = True)
  )

# Concatenating the output and the final hidden state of the forward and the backward propagation.
encoder_topics_outputs = tf.concat((encoder_topics_fw_outputs, encoder_topics_bw_outputs), -1)
encoder_topics_final_state = tf.concat((encoder_topics_fw_final_state, encoder_topics_bw_final_state), -1)


# BLSTM Encoder for encoding the answer
forward_answers_encoder_cell = BasicLSTMCell(encoder_hidden_units)
backward_answers_encoder_cell = BasicLSTMCell(encoder_hidden_units)

((encoder_answers_fw_outputs,
  encoder_answers_bw_outputs),
 (encoder_answers_fw_final_state,
  encoder_answers_bw_final_state)) = (
    tf.nn.bidirectional_dynamic_rnn(cell_fw = forward_answers_encoder_cell,
    								cell_bw = backward_answers_encoder_cell,
    								inputs = encoder_inputs_answers_embedded,	# embedded answers.
    								dtype = tf.float32, time_major = True)
  )

# Concatenating the output and the final hidden state of the forward and the backward propagation.
encoder_answers_outputs = tf.concat((encoder_answers_fw_outputs, encoder_answers_bw_outputs), 2)
encoder_answers_final_state = tf.concat((encoder_answers_fw_final_state, encoder_answers_bw_final_state), 2)

# Concatenating the final hidden state of both the question type and answer encoder to initialize the decoder.
both_encoders_final_state = tf.concat((encoder_topics_final_state, encoder_answers_final_state), 2)



# # Decoder: Yet to implement
# decoder_cell = tf.nn.rnn_cell.BasicLSTMCell(decoder_hidden_units)
# decoder = tf.contrib.seq2seq.BasicDecoder(decoder_cell,both_encoders_final_state)
# outputs = tf.contrib.seq2seq.dynamic_decode(decoder)



