import tensorflow as tf

# Hyper-Parameters
# learning_rate = 0.0001
# training_epochs = 15
# batch_size = 100

n_nodes_hl1 = 600           # Number of hidden units.

x = tf.placeholder('float', [None, 300])   # Because the embedding is of 300 dimenstion

# Fully Connected Neural Network.
def fully_connected_neural_network_model(input_data, output_classes):

    hidden_1_layer = {'weights':tf.Variable(tf.random_normal([300, n_nodes_hl1]))
					  'biases':tf.Variable(tf.random_normal(n_nodes_hl1))}

    output_layer = {'weights':tf.Variable(tf.random_normal([n_nodes_hl1, output_classes]))
					  'biases':tf.Variable(tf.random_normal(output_classes))}

    l1 = tf.add(tf.matmul(input_data,hidden_1_layer['weights']), hidden_1_layer['biases'])
    l1 = tf.nn.tanh(l1)         

    output = tf.add(tf.matmul(l1,output_layer['weights']), output_layer['biases'])
    output = tf.nn.sigmoid(output)

    return output

