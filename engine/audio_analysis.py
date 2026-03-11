import librosa
import numpy as np
import matplotlib.pyplot as plt

#def analyse_audio(file_path: str):

    #y, sr =  librosa.load(file_path, sr=None, mono=False)

def analyse_audio(file_path: str):

    y,sr = librosa.load(file_path, sr=None)
    librosa.util.valid_audio(y)
    plt.figure(figsize=(10,4))
    librosa.display.waveshow(y, sr=sr)
    plt.title("Waveform")

    #Calculate Short Time Fourier Transform (STFT)
    stft = np.abs(librosa.stft(y))

    plt.figure(figsize=(10,4))
    librosa.display.specshow(
        librosa.amplitude_to_db(stft, ref=np.max),
        sr=sr,
        x_axis='time',
        y_axis='log'
    )
    plt.colorbar(format='%+2.0f dB')
    plt.title("Spectrogram")

    plt.show(block=True)

    plt.savefig("waveform.png")
    plt.savefig("spectrogram.png")

    return y, sr
    

if __name__ == "__main__":
    analyse_audio("dunno1.wav")


