import pandas as pd
import os

def create_csv(folder):
    for filename in os.listdir(folder):
        if filename.endswith('.trans.txt'):
            break
    filename_and_transcript_path = folder + '/' + filename
    with open(filename_and_transcript_path , 'r') as fd:
        file_name_and_transcript = fd.readline().split(' ')
        fileName = []
        transcript = []
        while len(file_name_and_transcript) != 1:
            #df.append([file_name_and_transcript[0], ' '.join(file_name_and_transcript[1: ])])
            fileName.append(file_name_and_transcript[0])
            transcript.append((' '.join(file_name_and_transcript[1: ]))[:-1])
            file_name_and_transcript = fd.readline().split(' ')
        
        fileName_and_transcript_dict = {'wav_filename': fileName, 'transcript': transcript}
        df = pd.DataFrame(fileName_and_transcript_dict)
        df.to_csv(folder + '/fileName_and_transcript.csv',  index = False)
    
        
            

#for filename in os.listdir(filename_and_transcript_path):
#        if filename.endswith('.trans.txt'):
#            break
create_csv('C:/E/Yash/KarvAnalytics/DataSet/train/61/70968')