import argparse
import sounddevice as sd
from scipy.io import wavfile
import Speaker_Verification.Training_Verification as GND
import Speaker_Verification.FeatureExtraction as FtE
import soundfile as sf
import pandas as pd
import noisereduce as nr
import detect_voice

def get_arguments():

    parser=argparse.ArgumentParser()
    parser.add_argument('Option',help='(train/verify) Choose between training a new model or performing the verification of an audio')
    parser.add_argument('Speaker',help='Speaker Id to Verify or Train a new model')
    parser.add_argument('-A','--Audio',default='audioDef',help='Audio File for Verification or Directory for Training if file option was selected on -audm argument')
    parser.add_argument('-ff','--fileformat',default='wav',help='Format of the Audio File(Default=wav)')
    parser.add_argument('Method',help='Method for delivering the audio to perform the verification(file/microphone)')
    return parser.parse_args()


def Main():
    arguments=get_arguments()
    SpeakerId=arguments.Speaker
    AudioF=arguments.Audio
    opt=arguments.Option
    af=arguments.fileformat
    if opt=='verify':
        ##REVER A MANIPULAÇÃO DOS FORMATOS     
        if arguments.Method=='file':
            GND.Verification(SpeakerId,AudioF)
        elif arguments.Method=='microphone':
            AudioP=pd.read_csv('AudioProperties.csv')
            AudioProps=AudioP[AudioP['Name']==SpeakerId]
            sr=int(AudioProps.SamplingRate[AudioProps.index[0]])
            ch=int(AudioProps.channels[AudioProps.index[0]])
            dataType=str(AudioProps.dtype[AudioProps.index[0]])
            af=str(AudioProps.AudioFormat[AudioProps.index[0]])
            recording=sd.rec(int(sr*6),samplerate=sr,channels=ch,dtype=dataType)
            print('RECORDING')
            sd.wait()
            print('Recording Finished')
            noise,sn=sf.read('noise.flac')
            reducenoise=nr.reduce_noise(audio_clip=recording.flatten(),noise_clip=noise,verbose=False)
            fileName='Verify'+'.'+af
            if detect_voice.is_speech(reducenoise,sr):    
                sf.write(fileName,reducenoise,sr)
                GND.Verification(SpeakerId,fileName)
            else:
                print('Voice Activity was not Detected')
        else:
            print('Invalid Method')
    elif opt=='train':
        GND.TrainModel(AudioF,SpeakerId,Aformat=af)
    else:
        print('Invalid Option')

if __name__=='__main__':
    
    Main()
    
