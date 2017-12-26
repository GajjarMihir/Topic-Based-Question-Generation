# Topic-Based-Question-Generation

1. Preprocessing.py: Amazon question/answer corpus (AQAD) is used for training and testing. This file contains the code which                        removes the question-answer pairs which contain:
                     a) Answers which cannot be used to generate meaningful questions, like "yes/no".
                     b) Questions with more than 50 words.
                     The words whose chances for being the topic are negligible such as "is", "does" are removed using the                          stop words from the nltk library. Also, the punctuation marks are removed from the questions and the                            answers. In addition, it extracts all the questions and the answers and stores them in two separate                            files to the path specified for every file in the data set.

2. Extract_Question_Types.py: It parses through all the questions and groups them into seven categories as discussed in the                                   paper. Hence, we can know the question types.

3. Fully_connected_neural_network: A fully connected neural network is implemented using the tensorflow library. One of its use                                    is that it is used to convert the question type embedding of seven different categories in                                      to the internal vector representation. Hence, it serves as an encoder to encoder the                                            question types.

4. Topic-Based Question Generation.py: It implements the proposed model of the paper i.e. Topic 4.3. Here, there are three                                            encoders: question type encoder, topic encoder, answer encoder and 2 decoders: a pre-                                          decoder and a final decoder. Here, the filtered questions and answers are read from the                                        path. Then, topics are extracted from every question-answer pair using the 4.1 Topic                                            Extraction Mechanism explained in the paper. Glove is used to obtain embeddings. Then,                                          the extracted question types are embedded using glove. Then these type embeddings are                                          converted into internal vector representation using the fully connected neural network.
                                       Bi-directional Long Short-Term Memory is used to encode the topic and answer. Pre-decode                                        mechanism is used as to filter out the noise in the topics extracted using the topic                                            extraction process.
                                       The encoders for the question type, topic and answer and the pre-decoder have been                                              implemented i.e. the fully connected neural network for the question type, the Bi-                                              directional Long Short- Term Memory for the topic and the answer and the LSTM with                                              attention for the decoder have been implemented. Currently, I am trying to implement                                            the final decoder which will complete the entire model.
                                       
Language Used: Python 2.7.14
Libraries Used: Tensorflow 1.4.1, json_file, gzip, os, nltk 3.2.5, numpy, sklearn.
    
