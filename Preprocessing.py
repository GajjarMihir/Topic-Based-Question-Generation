# Preprocessing the data.

import json_file				# For the json data.
import gzip					# Using gzip because the file is in .gz format.
import os					# For listing all the files from the directory.

path = '/media/mihir/Academics/Btech Project/IIT_Bombay/Data/'		# The path containing the data.

files = os.listdir(path)	# stores all the files in the directory from the path into a list.

Questions = []				# For storing the questions.
Answers = []				# For storing the answers for a particular question.
All_Answers = []			# For storing the answers of all the questions.
max_question_word_length = 50	# Maximum word length of the question.

# Gives a generator object of the file in the dataset.
def parse(path):			
  g = gzip.open(path, 'r')
  for l in g:
    yield eval(l)

for i in range(len(files)):  # Iterating through all the files.

	file_name = parse(path+files[i])							# getting a generator object of the files.

	for data in file_name:										# the data in the file
		for question in data['questions']:						# question property of the object.
			if question['questionType'] != 'yes/no': 			# because we want to remove the 'yes/no' category questions.
				words = question['questionType'].split()		# Splitting the question into individual words for finding the length of the questions.
				if len(words) <= max_question_word_length:		# We want to remove the questions which contains more than 50 words.
					Questions.append(question['questionText'])	# Storing the question into the list.
					for ans in question['answers']:				# Iterating through its answers.
						if (ans['answerText'].upper() != "YES") and (ans['answerText'].upper() != "NO"): # Filtering out the answers which contains only yes or no.
							Answers.append(ans['answerText'])	# Storing the all the answers for the particular question.
		All_Answers.append(Answers)								# Storing the answers for a particular question in a list.
		Answers = []											# Resetting the Answers list.

	print "Data collected for " + files[i]						# displays the files for which the filtering is completed.
	print "Questions Writing"									# Writing the list containing the questions in to a file.
	with open('/media/mihir/Academics/Btech Project/IIT_Bombay/Filtered_Data/' + files[i][:-8] + '_questions.json', 'w') as outfile:
		json.dump(Questions, outfile)
	print "Answers Writing"										# Writing the list containing the all the answers for all the questions into a file.
	with open('/media/mihir/Academics/Btech Project/IIT_Bombay/Filtered_Data/' + files[i][:-8] + '_answers.json', 'w') as outfile:
		json.dump(All_Answers, outfile)

	Questions = []												# Resetting the Questions list.
	All_Answers = []											# Resetting the Answers list.
					
					




# For printing all the questions and the answers.
# for i in range(len(Questions)):
# 	for j in range(len(All_Answers[i])):
# 		print Questions[i]
# 		print "---------------------------------------------------------------"
# 		print All_Answers[i][j]
# 		print "---------------------------------------------------------------"

# For writing the json data from the list into file.
# x = [1, 2, 3]
# json write
# with open('data.json', 'w') as outfile:  
#     json.dump(x, outfile)
#     

# For reading the json data from the file into list.
#json read
# with open('data.txt') as json_file:  
#     data = json.load(json_file)
