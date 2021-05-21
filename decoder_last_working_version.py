# -*- coding: utf-8 -*-

"""
Created on Mon Mar 1 09:53:28 2021
@author: Polina Timofeeva

This program:
    1) Takes a .csv or a .xlsx file with base64 encoded strings of audio files 
    2) Decodes the strings and saves them an .webm file
    3) Converts the .webm files to .wav if don´t already exist
        - Converts the audio to mono, if not already
    4) Finds speech onset
    5) Creates a .csv file with long format data for all participants for further analysis
    6) Recognizes speech
    7) Finds on and offset of speech
    8) Creates a file with all that info saved in a long format
You need to add your Google API key(json file) to the environmental variables in your system
Example: GOOGLE_APPLICATION_CREDENTIALS = "your path"    
 
TODO list:
    1) filtering sound files
    
    2) github repository
    3) Upload scripts we have
    4) Comment our codes, clean it
    5) Shared file with TODO list
    6) email to Larraitz about the possible tasks 11th
    
    7) FLag, in case there are uncertainties about the speech onset
    
    
    

"""

#cd Desktop/Python code/Audio_processing
#.\env\Scripts\activate

import base64
import re
from pandas import read_excel
import pandas as pd
import os
import subprocess
from glob import glob
import io
import librosa
from google.cloud import speech_v1p1beta1 as speech
from scipy.signal import find_peaks
import scipy.signal as sps
import numpy as np
from scipy import signal
from  matplotlib import pyplot as plt
from playsound import playsound



# Speech and offset detectio n with Google API
def speech_to_text(audio_file_name, language_1, language_2):
    
    client = speech.SpeechClient()
    word = "Not recognized" # Default values if the voice is not recognized
    conf = 0
    start_time = 0
    end_time = 0
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
            start_time = word_info.start_time.total_seconds()
            end_time = word_info.end_time.total_seconds()
             
    return word, conf, start_time, end_time


def make_xlsx(path, file_name):
    df_new = pd.read_csv(path+f'{file_name}.csv')
    dfr = pd.ExcelWriter(path+f'{file_name}.xlsx')
    df_new.to_excel(dfr, index = False)
    dfr.save()
    dfs = read_excel(path+file_name+'.xlsx')
    return dfs


def create_webm_file(webm_file, audio_data):   
    snd = open(webm_file,"wb")
    # Decode the base64 encoded string and save it in a .webm file
    decoded = base64.b64decode(audio_data+"====")
    snd.write(decoded)
    snd.close()
    
    
def make_wav_from_webm(new_path, webm_file, output_path):
    webm = new_path+webm_file
    output = new_path+output_path
    command = ['ffmpeg', '-i', f'{webm}','-ac','1', f'{output}']
    # 15sec timeout in case it gets stuck
    subprocess.call(command, timeout = 15, shell = True) 
    
    
def band_pass_filter(data, fs, order=5):
    
    fL = 0.1
    fH = 100
    b = 0.08
    N = int(np.ceil((4 / b)))
    if not N % 2: N += 1  # Make sure that N is odd.
    n = np.arange(N)
    
    # low-pass filter
    hlpf = np.sinc(2 * fH * (n - (N - 1) / 2.))
    hlpf *= np.blackman(N)
    hlpf = hlpf / np.sum(hlpf)
    
    # high-pass filter 
    hhpf = np.sinc(2 * fL * (n - (N - 1) / 2.))
    hhpf *= np.blackman(N)
    hhpf = hhpf / np.sum(hhpf)
    hhpf = -hhpf
    hhpf[int((N - 1) / 2)] += 1
    
    h = np.convolve(hlpf, hhpf)
    new_signal = np.convolve(data, h)
    return new_signal

        
def compute_novelty_energy(x, Fs=1, N=2048, H=256, gamma=1000, norm=True):
    """Compute energy-based novelty function

    Notebook: C6/C6S1_NoveltyEnergy.ipynb

    Args:
        x (np.ndarray): Signal
        Fs (scalar): Sampling rate (Default value = 1)
        N (int): Window size (Default value = 2048)
        H (int): Hope size (Default value = 128)
        gamma (float): Parameter for logarithmic compression (Default value = 10.0)
        norm (bool): Apply max norm (if norm==True) (Default value = True)

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

def plot_trial(x, peaks, f_name, Fs, Fs_nov):
    
    number_of_samples = round(len(x) * Fs_nov / Fs)-1
    data = sps.resample(x, int(number_of_samples))
    dur = round(len(data)/round(Fs_nov))
    interval = dur/len(data)   
    time = np.arange(0,dur,interval)
    peaks1 = peaks*interval
    
    fig = plt.gcf()
    fig.canvas.set_window_title(f'{f_name}')
    plt.plot(time,data)
    plt.plot(peaks1, data[peaks], "x")
    plt.pause(2)
    plt.show()


def main():
    # Change to your current working directory
    path = 'E:/Desktop/Switch_beh/Results/SwitchVO/'
    os.chdir(path)
    tasks = ['spanish','euskera'] # ['spanish','euskera','eus-sp'] list of the tasks
    # conditions are the relevant conditions, skip the ones you don´t care about
    conditions = ['11','12','22','31','32','41','42'] 
    # Structure of your desired output file
    structure = ['Subject ID', 
                 'Gender', 
                 'Age', 
                 'Task',
                 'Condition', 
                 'Trial', 
                 'Image', 
                 'Start_time',
                 'Response',
                 'Confidence']
    
    language_1 = 'es_ES'
    language_2 = 'eu_ES'
    
    for task in tasks:
           
        file_names=list()
        for name in glob( '*/**.csv' ):
            if re.search(task,name):
                file_names.append(name[:-4])
     
        for file_name in file_names:
            i = 0
            dataf = pd.DataFrame(columns = structure,dtype='str')
            # Check if the file is .xlsx already and if no, make a xlsx from csv
            try:
                dfs = read_excel(path+file_name+'.xlsx')
            except FileNotFoundError:
                # If doesn't exist, create it and read
                dfs = make_xlsx(path,file_name)
                pass
    
            # Load the .xlsx file and create a pattern to match(here, any string with any alphabonumeric values is chosen)
            pattern = re.compile("\w")
            
            for r in range (0,len(dfs)):  
                
                if pattern.match(dfs.audio_data[r]):
                    if dfs.Condition[r] =='0':
                        print('Finished', i, 'out of 336')
                        i+=1 
                        continue
                    # Change to the new directory and create, if doesn´t already exist
                    try:
                        new_path = path + f'{file_name}/audios_{task}/{dfs.Condition[r]}/'
                        os.chdir(new_path)
                    except FileNotFoundError:
                        # Directory already exists
                        os.makedirs(new_path)
                        pass
                    
                    if dfs.Condition[r] in conditions:

                        webm_file = f'{i}_{dfs.Condition[r]}_{dfs.Image[r][:-4]}.webm'
                        output_path = ''+webm_file[:-4]+'wav'  
                        try:
                            io.open(output_path,"rb")
                        except FileNotFoundError:
                            create_webm_file(webm_file, dfs.audio_data[r])
                            make_wav_from_webm(new_path, webm_file, output_path)
                            
                        x, Fs = librosa.load(output_path)
                        #clean_signal = band_pass_filter(x,fs=Fs)
                        nov, Fs_nov = compute_novelty_energy(x, Fs=Fs, N=N, H=H, gamma=gamma)
                        peaks, _ = find_peaks(nov, prominence=0.7, width=1)
                        
                        
                        if len(peaks) > 1:
                            plot_trial(x, peaks, output_path, Fs,Fs_nov)
                            playsound(f'{output_path}')
                            txt = input("Which one of the onsets is the correct one? Enter a number eg. 1. If the starting point is not there, enter - ")
                            playsound(f'{output_path}')
                            plt.close()
                            if txt == '-':
                                start_time='Check the file'
                            try:
                                print("Writing the ", txt, " as a peak")
                                start_time=peaks[int(txt)-1]/Fs_nov
                            except ValueError:
                                print("This is not a valid number. Make sure to follow the order of the peaks with stars")
                        
                        else:
                            start_time = peaks[0]/Fs_nov
                            
                        # if there are any webm files, delete it to save space
                        try:
                            os.remove(webm_file)
                        except FileNotFoundError:
                            pass 
                        
                        # Speech recognition part with Google API speech to text    
                        #word, conf, start_time, end_time = speech_to_text(output_path, language_1, language_2)
                        
                        word=''
                        conf=''
                        new_row={'Subject ID':file_name,
                                 'Gender':'',
                                 'Age':'',
                                 'Task':task,
                                 'Condition':f'{dfs.Condition[r]}',
                                 'Trial':f'{i}',
                                 'Image':f'{dfs.Image[r][:-4]}',
                                 'start_time': start_time,
                                 'Response': word,
                                 'Confidence': conf}
                        
                        dataf = dataf.append(new_row,ignore_index=True)
                        
                        print('Finished', i, 'out of 336')
                        i+=1  
                    
            result_file = f'{path}/{file_name}/{task}_result_{file_name[:4]}.csv'
            dataf.to_csv(result_file, index = False, header=True)
        
if __name__=='__main__':
    main()