import json

path = '/media/mihir/Academics/Btech Project/IIT_Bombay/Filtered_Data/'		# The path containing the data.

# Reading the filtered questions.
with open(path + 'QA_Video_Games_questions.json') as json_file:  
    Questions = json.load(json_file)

# Question types "Do" "Is" "Could" etc. - can also be yes/no questions. But here I am considering only can for now.
Questions_Types = ["Can", "What", "Who","How", "Where", "Why"]

Category_Questions 	= [[],[],[],[],[],[],[]]  # Each list in this list contains the questions for every category.

break_loop = False

for ques in range(len(Questions)):
	for words in Questions[ques]:
		for i in range(len(Questions_Types)):
			if Questions_Types[i].upper() in words.upper():
				Category_Questions[i].append(Questions[ques])
				break_loop = True
				break
		if break_loop == True:
			break
	if break_loop != True:
		Category_Questions[6].append(Questions[ques])
	break_loop = False
			
	
	 
# Represents the category of the questions.
# Category_Questions[0]  # contains all the yes/no questions.
# Category_Questions[1]	 # contains all the what questions.
# Category_Questions[2]  # contains all the who questions.
# Category_Questions[3]	 # contains all the how questions.
# Category_Questions[4]  # contains all the where questions.
# Category_Questions[5]	 # contains all the why questions.
# Category_Questions[6]  # contains all the other questions.

# print len(Category_Questions[0])  # contains all the yes/no questions.
# print len(Category_Questions[1])  # contains all the what questions.
# print len(Category_Questions[2])  # contains all the who questions.
# print len(Category_Questions[3])  # contains all the how questions.
# print len(Category_Questions[4])  # contains all the where questions.
# print len(Category_Questions[5])  # contains all the why questions.
# print len(Category_Questions[6])  # contains all the other questions.