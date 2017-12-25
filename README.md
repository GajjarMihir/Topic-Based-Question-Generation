# Topic-Based-Question-Generation

1. Preprocessing.py: Amazon question/answer corpus (AQAD) is used for training and testing. This file contains the code which                        removes the question-answer pairs which contain:
                     a) Answers which cannot be used to generate meaningful questions, like "yes/no". Moreover, all the                                 questions which are of the type "yes/no" are removed.
                     b) Questions with more than 50 words.
                     In addition, it extracts all the questions and the answers and stores them in two separate files to the                        path specified for every file in the data set.

2. Topic extraction.py: Can be used to extract the topic from the given question-answer pair. Here, a sample question-answer                           pair is used as an example. The questions and the answers obtained from the preprocessing task can be                           used here and the topics can be extracted for all the question-answer pairs. Additionally, the words                           whose chances for being the topic are negligible such as prepositions can be removed using the nltk                             stop words from the nltk library and also the punctuation marks can be removed.

3. Fully_connected_neural_network: A fully connected neural network is implemented using the tensorflow library. One of its use                                   is that it is used to convert the question type embedding of seven different categories in to                                   the internal vector representation. Hence, it serves as an encoder to encoder the question                                     types.

4. Topic-Based Question Generation.py: It implements the proposed model of the paper i.e. Topic 4.3. Here, there are three                                            encoders: question type encoder, topic encoder, answer encoder and 2 decoders: a                                                pre-decoder and a final decoder. Fully connected neural network is used to encode the                                          question type. Bi-directional Long Short Term Memory is used to encode the topic and                                            answer. Pre-decode mechanism is used as to filter out the noise in the topics extracted                                        using the topic extraction process. Final decoder is used to predict words by decoding                                          the internal vector representation. 
                                       The encoders for the question type, topic and answer have been implemented i.e. the
                                       fully connected neural nework for the question type and the Bi-directional Long Short                                          Term Memory for the topic and the answer have been implemented. Currently, I am trying                                          to implement the pre-decoder and the final decoder which will complete the entire model.
                                       
Language Used: Python 2.7.14
Libraries Used: Tensorflow 1.4.1, json_file, gzip, os, nltk 3.2.5, numpy, sklearn.
    
