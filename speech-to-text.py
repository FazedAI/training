import io
import pandas as pd

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

def transcribe_speech(audio_file_path):
    client = speech.SpeechClient()
    
    with io.open(audio_file_path, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content = content)
        
    config = types.RecognitionConfig(encoding = enums.RecognitionConfig.AudioEncoding.FLAC,
                                     language_code = 'en-US')
    
    response = client.recognize(config, audio)
    
    
    for result in response.results:
        return result.alternatives[0].transcript


def wer(r, h):
    """
    Calculation of WER with Levenshtein distance.

    Works only for iterables up to 254 elements (uint8).
    O(nm) time ans space complexity.

    Parameters
    ----------
    r : list
    h : list

    Returns
    -------
    int

    Examples
    --------
    >>> wer("who is there".split(), "is there".split())
    1
    >>> wer("who is there".split(), "".split())
    3
    >>> wer("".split(), "who is there".split())
    3
    """
    # initialisation
    import numpy
    d = numpy.zeros((len(r)+1)*(len(h)+1), dtype=numpy.uint8)
    d = d.reshape((len(r)+1, len(h)+1))
    for i in range(len(r)+1):
        for j in range(len(h)+1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i

    # computation
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            if r[i-1] == h[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                substitution = d[i-1][j-1] + 1
                insertion    = d[i][j-1] + 1
                deletion     = d[i-1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)

    return d[len(r)][len(h)]

def make_audio_file_path(fileName):
    audio_file_path = 'C:\\E\\Yash\\KarvAnalytics\\test-clean'
    for name in fileName.split('-')[0:-1]:
        audio_file_path = audio_file_path + '\\' + name
    audio_file_path = audio_file_path + '\\' + fileName + '.flac'
    return audio_file_path
    
    
def transcribe_file_and_find_wer(fileName_and_transcript):
    #transcription_file = open(transcription_path)
    #fileName_and_transcript = transcription_file.readline().split(' ')
    audio_file_path = make_audio_file_path(fileName_and_transcript[0])
    api_output = transcribe_speech(audio_file_path)
    transcript = fileName_and_transcript[1:]
    transcript[-1] = transcript[-1][:-1]
    word_error_rate = wer(transcript, api_output.upper().split(' '))
    audio_file_name = fileName_and_transcript[0]
    return (audio_file_name, api_output.upper(), word_error_rate, transcript)
    

def read_transcript_and_transcribe(transcription_file):
    dataFrameDict = {}
    dataFrameDict['audio_file_name'] = []
    dataFrameDict['word_error_rate'] = []
    dataFrameDict['api_output'] = []
    dataFrameDict['correct_output'] = []
    with open(transcription_file, 'r') as fi:
        line = fi.readline()
        while len(line)!=0:
            audio_file_name, api_output, word_error_rate, correct_output = transcribe_file_and_find_wer(line.split(' '))
            print(audio_file_name, api_output, str(word_error_rate), ' '.join(correct_output))
            line = fi.readline()
            dataFrameDict['audio_file_name'].append(audio_file_name)
            dataFrameDict['word_error_rate'].append(word_error_rate)
            dataFrameDict['api_output'].append(api_output)
            dataFrameDict['correct_output'].append(' '.join(correct_output))
        
        fi.close()
    
    df = pd.DataFrame(dataFrameDict)
    df.to_excel('C:\\E\\Yash\KarvAnalytics\\GoogleWordErrorRate.xlsx', sheet_name = 'Google')
            
print(read_transcript_and_transcribe('C:\\E\\Yash\\KarvAnalytics\\test-clean\\61\\70968\\61-70968.trans.txt'))    