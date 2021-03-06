import numpy as np
import soundfile as sf
import librosa
import os
from sklearn import preprocessing
from scipy.io import wavfile
from .webrtcvad_support import Get_Wavefile


def GetSingleFile(Audio_file):

    if os.path.isfile(Audio_file):
        Track = sf.read(Audio_file)
        dataType = Track[0].dtype
        ch = len(Track[0].shape)
        sr = Track[1]
        MFCC = librosa.feature.mfcc(Track[0], sr=Track[1], n_mfcc=13)
        MFCCN = preprocessing.scale(MFCC)
        return [MFCCN,sr]

    else:
        return print('File Not Found')


#Feature Extraction for All the Files in a Given Directory

def Features(PATH, Aformat):
   
    FT = np.asarray(())
    sr = 0
    print(Aformat)
    if os.path.isdir(PATH):

        for files in os.listdir(PATH):
            file_path = os.path.join(PATH, files)
            if os.path.isfile(file_path):
                
                if files.endswith('.{}'.format(Aformat)):
                    Audio=sf.read(file_path)
                    dataType=Audio[0].dtype
                    ch=len(Audio[0].shape)
                    sr=Audio[1]
                    Mfcc=librosa.feature.mfcc(Audio[0],sr=Audio[1],n_mfcc=13).transpose()
                    Mfcc_Normalized=preprocessing.scale(Mfcc)
                    FT=Mfcc_Normalized if FT.size==0 else np.vstack((FT,Mfcc_Normalized))            
        print(FT)
        return [FT,sr]
    else:
        print('Directory Not Found')

def SilenceRemoval(AudioSignal,sr,threshold_only=False):
    
    """Teste Function for Silence Removal"""


    dataType=AudioSignal.dtype
    Signal=AudioSignal
    ##Frame Length
    fl=0.025
    #samples per frame
    spf=int(np.ceil(fl*sr))
    L=len(Signal)
    #number of frames
    nf=int(np.ceil(len(Signal)/spf))
    #Setting a silence threshold
    threshold=np.amax(Signal)*.003
    #Option of only returning the voice thresold
    if threshold_only:
        return threshold
    #length to be padded
    toPad=int((nf*spf)-L)
    padZeros=np.zeros(toPad)
    #Checking the Channels
    if Signal.shape==(L,1):
        SignalPadded=np.append(Signal,padZeros)
        #Signal Framing for Detecting the Silent parts
        SignalFrames=np.reshape(SignalPadded,(nf,spf))
        indexes=list()
        #Finding the Silent Frames
        for i in range(0,nf):
            if np.amax(SignalFrames[i])> threshold:
            
                indexes.append(i)
    
        AudioWout=SignalFrames[indexes,:]
        #Reconstruction of the Signal
        AudioReconst=np.ravel(AudioWout)
        AudioReconst=np.asarray(AudioReconst,dtype=dataType)
        return AudioReconst
    elif Signal.shape==(L,2):
        #Processing for an audio with two channels
        SignalPadded=np.append(Signal[:,0],padZeros)
        #Framing
        SignalFrames=np.reshape(SignalPadded,(nf,spf))
        indexes=list()
        #Finding the Silent Parts
        for i in range(0,nf):
            if np.amax(SignalFrames[i])> threshold:
            
                indexes.append(i)
        #Reconstruction of the two channels
        AudioOut1=SignalFrames[indexes,:]
        AudioOut1.shape[0]*AudioOut1.shape[1]
        AudioOut1=np.reshape(AudioOut1,(int(AudioOut1.size),1))
        AudioChan1=np.asarray(AudioOut1,dtype=dataType)
        SignalPaddedChan2=np.append(Signal[:,1],padZeros)
        SignalFramesChan2=np.reshape(SignalPaddedChan2,(nf,spf))
        AudioOut2=SignalFramesChan2[indexes,:]
        AudioOut2=np.reshape(AudioOut2,(int(AudioOut2.size),1))
        AudioChan2=np.asarray(AudioOut2,dtype=dataType)
        AudioReconst=np.concatenate((AudioChan1,AudioChan2),axis=1)
        return AudioReconst,

def Gather_WAV_Files(Files_List, Base_Dir):
    
    Total_Length = 0
    Audio_Signals = []

    try:
        for File in Files_List:
            Path = os.path.join(Base_Dir, File)
            Audio, sr = sf.read(Path)
            Total_Length += len(Audio)
            Audio_Signals.append(Audio)

        Audio_Array = np.zeros(Total_Length)
        Start = 0
        for Signal in Audio_Signals:
            Audio_Array[Start:(Start+len(Signal))] = Signal
            Start += len(Signal)-1
        
        return Audio_Array
    
    except FileNotFoundError:

        print('Audio File Not Found')

def Voice_Activity_Detection(filename):

    """ Function for separating the voiced parts from audio files"""
   
    Rec_Dir = os.path.dirname(filename)
    Audio_File = os.path.basename(filename)
    Audio_Name = Audio_File.split('.')[0]
    Output_Wavefile = 'VAD_{}'.format(Audio_Name)
    Output_Wavefile_Path = os.path.join(Rec_Dir, Output_Wavefile)
    Files = Get_Wavefile(filename, Rec_Dir, Output_Wavefile)
    for File in Files:
        if os.path.isfile(File):
            print('File Created')
        else:
            print('Error: Output Audio File has not been created correctly')

    return Files
