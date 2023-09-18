import requests
import numpy as np


# Define a list holding all characters to analyze character transitions 
state = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " ", "  ", ",", "'"]

# Create word2id dictionary
char2id_dict = {}
for index, char in enumerate(state):
    char2id_dict[char] = index

#Create character transition matrix with three parameters 
def CharTransitionMatrix(text, state, char2id_dict):
    #create matrix initially filled with 0s to store character transition counts
    transition_matrix = np.zeros((30, 30))
    #loop through the text for each character and it's following character
    for i in range(len(text) - 1):
        current_char = text[i].lower()
        next_char = text[i + 1].lower()
        #Checks whether characters are in state and then proceeds to calculate
        if (current_char in state) and (next_char in state):
            #Use IDs to update transition matrix  
            current_char_id = char2id_dict[current_char]
            next_char_id = char2id_dict[next_char]
            transition_matrix[current_char_id][next_char_id] += 1
    #store the sum as sum_of_each_row_all
    sum_of_each_row_all = np.sum(transition_matrix, 1)
    #Calculate row sum and normalise transition matrix 
    #0 will indicate no transitions, 1 will indicate valid probability distribution 
    for i in range(30):
        single_row_sum = sum_of_each_row_all[i]
        if (sum_of_each_row_all[i] == 0):
            single_row_sum = 1

        transition_matrix[i, :] = transition_matrix[i, :] / single_row_sum

    return transition_matrix

#Fetch text data from online source
Author1TextURL = "https://example.com/exampletext1.txt" #add desired link here 
Author2TextURL = "https://example.com/examplext2.txt" #add desired link here 
#Sample to be checked for authorship
SampleText2URL = "https://example.com/exampletext3.txt" #add desired link here

#Get the text data using the requests library 
Author1TextResponse = requests.get(Author1TextURL)
Author2TextResponse = requests.get(Author2TextURL)
Author1Text2Response = requests.get(SampleText2URL)

Author1Text = Author1TextResponse.text
Author2Text = Author2TextResponse.text
Author1Text2 = Author1Text2Response.text

TMAuthor1Text = CharTransitionMatrix(Author1Text, state, char2id_dict)
TM_Author2Text = CharTransitionMatrix(Author2Text, state, char2id_dict)
#initialisation 
Author1Likelyhood = 0
Author2Likelihood = 0
#loop through characters in text 
for i in range(len(Author1Text2) - 1): #prevent out of bounds 
    current_char = Author1Text2[i].lower()
    next_char = Author1Text2[i + 1].lower()

    if (current_char in state) and (next_char in state):
        current_char_id = char2id_dict[current_char]
        next_char_id = char2id_dict[next_char]
        #check if both author's texts have non zero probabilities given character transition 
        if TMAuthor1Text[current_char_id][next_char_id] != 0 and TM_Author2Text[current_char_id][next_char_id] != 0:
            Author1Likelyhood += np.log(TMAuthor1Text[current_char_id][next_char_id])
            Author2Likelihood += np.log(TM_Author2Text[current_char_id][next_char_id])
#higher likelihood score 
print("Likelihood for Author1:", Author1Likelyhood)
print("Likelihood for Author2:", Author2Likelihood)
