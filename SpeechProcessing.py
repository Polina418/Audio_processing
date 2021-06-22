# -*- coding: utf-8 -*-

"""
Created on Mon Mar 1 09:53:28 2021
@author: Polina Timofeeva

This program:
    1) Gets the wav files
    2) Filters the sounds
    3) Finds speech onset
    4) Recognizes speech
    5) Creates a .csv file with long format data for all participants for further analysis

Make sure your file has the following structure: 
- Experimental folder
    - Task1
        - Participant1
        - Participant2
        - ...
    - Task2
        - Participant3
        - Participant4
        - ...
    
You need to add your Google API key(json file) to the environmental variables in your system
Example: GOOGLE_APPLICATION_CREDENTIALS = "your path"    
 
"""

#cd Desktop/Python code/Audio_processing
#.\env\Scripts\activate

import os, base64, re, io, subprocess, librosa
from glob import glob
from IPython import get_ipython
from pandas import read_excel
import pandas as pd
import numpy as np
from scipy import signal
from scipy.signal import find_peaks 
import scipy.signal as sps
from  matplotlib import pyplot as plt
from playsound import playsound
from google.cloud import speech_v1p1beta1 as speech
from scipy.signal import savgol_filter
import speech_recognition as sr
from scipy import ndimage
from numba import jit
@jit(nopython=True)
#%matplotlib inline

# Speech and offset detectio n with Google API
def speech_to_text(audio_file_name, language_1, language_2):
    """

    Parameters
    ----------
    audio_file_name : string
        This is the name of the file you want to process.
    language_1 : string
        What language is used in the audio?
    language_2 : TYPE
        If it is a dual language context, what is the second language?
        The codes for specific languages can be found in https://cloud.google.com/speech-to-text/docs/languages

    Returns
    -------
    word : string
        The recognized word.
    conf : int
        Confidence with which the word was recognized.

    """
    word = "Not recognized" # Default values if the voice is not recognized
    conf = 0
    try:
        r = sr.Recognizer()
        with sr.AudioFile(audio_file_name) as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.record(source)
    
        words = r.recognize_google(audio,language_1)
        for prediction in words:
            word = prediction["text"] 
            conf = prediction["confidence"]
        return word, conf
    except: 
        try:
            client = speech.SpeechClient()
            #start_time = ''
            with io.open(audio_file_name,"rb") as source:
                content = source.read()
        
            audio = speech.RecognitionAudio(content=content)  # read the entire audio file
            config = speech.RecognitionConfig(
                                language_code = language_1,
                                alternative_language_codes = [language_2],
                                enable_word_time_offsets = True,
                                enable_word_confidence = True,
                                model = 'command_and_search')
            response = client.recognize(request={"config": config, "audio": audio})
            for result in response.results:     
                alternative = result.alternatives[0]
                for word_info in alternative.words:        
                    word = word_info.word
                    conf = word_info.confidence                  
            return word, conf
        except:
            print("Wasn't able to connect to Google services. Proceeding without Speech Recognition")
            pass

def compute_novelty_energy(x, Fs=1, N=2048, H=128, gamma=1000, norm=True):
    """Compute energy-based novelty function

    Notebook: C6/C6S1_NoveltyEnergy.ipynb

    Args:
        x (np.ndarray): Signal
        Fs (scalar): Sampling rate (Default value = 1)
        N (int): Window size (Default value = 2048)
        H (int): Hope size (Default value = 128)
        gamma (float): Parameter for logarithmic compression (Default value = 10.0)
        norm (bool): Apply max norm (if norm==True) (Default value = True)

    1) Compute the short-time energy in the signal.
    2) Compute the first-order difference in the energy.
    3) Half-wave rectify the first-order difference.
    Returns:
        novelty_energy (np.ndarray): Energy-based novelty function
        Fs_feature (scalar): Feature rate
    """
    # x_power = x**2
    w = signal.hann(N)
    Fs_feature = Fs / H
    energy_local = np.convolve(x**2, w**2, 'same')
    energy_local = energy_local[::H]
    if gamma is not None:
        energy_local = np.log(1 + gamma * energy_local)
    energy_local_diff = np.diff(energy_local)
    energy_local_diff = np.concatenate((energy_local_diff, np.array([0])))
    novelty_energy = np.copy(energy_local_diff)
    novelty_energy[energy_local_diff < 0] = 0
    if norm:
        max_value = max(novelty_energy)
        if max_value > 0:
            novelty_energy = novelty_energy / max_value
    return novelty_energy, Fs_feature


def plot_trial(x_r, peaks, f_name, Fs, nov, pics_path):
    """

    Parameters
    ----------
    x_r : numpy.ndarray
        This is your filtered data
    peaks : numpy.ndarray
        These are the peaks of novelty function(speech onsets)
    f_name : string
        File name
    Fs : int
        Sampling frequency of your clean data.
    nov : numpy.ndarray
        Novelty curve.
    pics_path : string
        Path, where you want to save pictures produced by the code.
        This is very useful to look at after the analysis is done in order to see,
        if there are any issues and correct it manually. 
        
    Returns
    -------
    peaks : numpy.ndarray
        updated peaks information.

    """
    
    dur = len(x_r)/Fs
    interval = dur/len(x_r)   
    tim = np.arange(0,dur,interval)
    peaks1 = peaks*interval

    for x, y in zip(peaks1[0::], peaks1[1::]):
        ind1 = np.where(peaks1==x);
        ind2 = np.where(peaks1==y);
        if x < 0.55:
            peaks1 = np.delete(peaks1, ind1)
            peaks = np.delete(peaks, ind1)
        if len(peaks1)>1 and y-x < 0.35:
            peaks1 = np.delete(peaks1, ind2)
            peaks = np.delete(peaks, ind2)

    peaks = peaks[0:1]
    peaks1 = peaks1[0:1]
    labels = list(range(1,len(peaks)+1))
    fig = plt.gcf()
    fig.canvas.set_window_title(f'{f_name}')
    plt.plot(tim[:len(x_r)], x_r)
    #plt.plot(tim[:len(nov)], nov)
    for j,label in enumerate(labels):
        plt.text(peaks1[j], 0, label, fontsize=10, bbox=dict(facecolor='white', alpha=0.5))
        plt.axvline(x=peaks1[j], label=f'Onset time {label} = {round(peaks1[j],3)}', c='r', ls='--')
    plt.legend(loc='upper right')
    plt.pause(1)
    plt.savefig(pics_path+f_name[:-4])
    plt.show()
    return peaks

def main():
        # Change to your current working directory
        path = input('Write your full path containing your .wav files    ')
        os.chdir(path)
        tasks = []
        conditions = []
        num_tasks = int(input('How many tasks are there?    '))
        for num in range(0, num_tasks):
            tasks.append(input('Type the name of your %d task (should be specified in the name of your wav file)     '%(num+1)))
        res_audios = input('What is the extension of your audios?(e.x. wav)    ')
        num_cond = int(input('How many conditions there are?    '))
        if num_cond-1 >=1:
            for cond in range(0, num_cond):
                conditions.append(input('Type the name of your %d condition (should be specified in the name of your wav file)     '%(cond+1)))
        fmri = input('Is it (f)MRI data y/n    ')
        # Structure of your desired output file
        structure = ['Subject ID', 
                     'Task',
                     'Condition', 
                     'Trial', 
                     'Start_time',
                     'Response',
                     'Confidence']
        
        speech_recog = input('Do you want to use Speech Recognition? (y/n)   ')
        if speech_recog == 'n':
            conf = 1
            word = 'OFF'
        
        for task in tasks:  
            subjects = list()
            os.chdir(path+task)
            for name in glob('*/' ):
                subjects.append(name[:-1]) 
                    
            for subject in subjects:
                print('Processing subject ', subject)
                i = 0
                file_names = list()
                os.chdir(path+task+f'/{subject}/')
                dataf = pd.DataFrame(columns = structure, dtype='str')
                pics_path = path + f'{task}/{subject}/plots/'
                try:
                    os.makedirs(pics_path)
                except:
                    pass

                for file in glob( f'**.{res_audios}' ):
                    if re.search(task.lower(),file.lower()):
                        file_names.append(file) 
                    elif num_cond == 0:    
                        file_names.append(file) 
                # Change to the new directory and create, if doesn´t already exist
                
                for file in file_names:    
                    x, Fs = librosa.load(file)
                    x_s = ndimage.median_filter(x, 11)
                    x_r = savgol_filter(x_s, 11, 4)
                    nov, Fs_nov = compute_novelty_energy(x_r)
                    nov = sps.resample(nov,len(x_r))
                    peaks, _ = find_peaks(nov, prominence=0.4, width=10)
                    
                    # If the part above doesn´t do too well, try this!
                    #x_s = savgol_filter(x, 51, 4)
                    #sif = int(len(x)/1000)
                    #x_r = ndimage.median_filter(x_s, size=sif)
                    #nov, Fs_nov = compute_novelty_energy(x_r, Fs)
                    #nov = sps.resample(nov, len(x_r))
                    #peaks, _ = find_peaks(nov, prominence=0.2, width=10)   
                    
                    # Speech recognition part with Google API speech to text  
                    if speech_recog == 'y':  
                        language_1 = 'es_ES' # Here you can specify languages you want to use in your experiment
                        language_2 = 'eu_ES' # Here you can specify languages you want to use in your experiment
                        word, conf = speech_to_text(file, language_1, language_2)
                        
                    peaks = plot_trial(x_r, peaks, file, Fs, nov, pics_path)
                    
                    if len(peaks) > 1:
                        playsound(f'{file}')
                        txt = input("Which one of the onsets is the correct one? Enter a number eg. 1. If the starting point is not there, enter - ")                              
                        if txt == '-':
                            start_time = 'Check the file'
                        else:
                            try:
                                print("Writing ", peaks[int(txt)-1]/Fs, " as the onset time")
                                start_time = peaks[int(txt)-1]/Fs
                            except ValueError:
                                start_time = txt
                                print("This is not a valid number. Make sure to follow the order of the peaks with stars")
                        plt.close()
                        
                    elif len(peaks) == 1:
                        playsound(f'{file}')
                        start_time = peaks[0]/Fs
                        if start_time > (len(x_r)/Fs-0.3):
                                txt = input("Which one of the onsets is the correct one? Enter a number eg. 1. If the starting point is not there, enter - ")                              
                                if txt == '-':
                                    start_time = 'Check the file'
                                else:
                                    try:
                                        print("Writing ", peaks[int(txt)-1]/Fs, " as the onset time")
                                        start_time = peaks[int(txt)-1]/Fs
                                    except ValueError:
                                        start_time = txt
                                        print("This is not a valid number. Make sure to follow the order of the peaks with stars")
                    else:
                        start_time = 'Empty'
                        sprec_reply = 'Empty'
                    
                    if fmri == 'y':
                        start_time = peaks[0]/Fs
                        
                    if conf < 0.5:   
                        sprec_reply = input("Was it %s ? If no, type the word. If yes press Enter."%word)
                        if sprec_reply == '':
                            pass
                        else:
                            word = sprec_reply
                            conf = 1
                    plt.close()
                    new_row = {'Subject ID':subject,
                                'Task':task,
                                'Condition':f'{file}',
                                'Trial':f'{i}',
                                'Start_time': start_time,
                                'Response': word,
                                'Confidence': conf}
                    
                    dataf = dataf.append(new_row,ignore_index=True)
                    get_ipython().magic('clear')
                    i += 1 
                try:            
                    result_file = path+f'/{task}/{subject}/{task}_result_{subject}.csv'
                    dataf.to_csv(result_file, index = False, header=True)   
                except PermissionError:
                    result_file = path+f'/{task}/{subject}/{task}_result_{subject}_1.csv'
                    dataf.to_csv(result_file, index = False, header=True)

                
if __name__=='__main__':
    main()
    
 
