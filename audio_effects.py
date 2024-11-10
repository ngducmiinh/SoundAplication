# audio_effects.py
import librosa
import numpy as np
import soundfile as sf
import tempfile
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
import speech_recognition as sr
from gtts import gTTS

# Thiết lập mặc định cho matplotlib
plt.rcParams['figure.figsize'] = [12, 4]
plt.style.use('dark_background')

def chipmunk_effect(audio_path, rate=2.0):
    y, sr = librosa.load(audio_path)
    y_fast = librosa.resample(y, orig_sr=sr, target_sr=int(sr * rate))
    y_high_pitch = librosa.effects.pitch_shift(y_fast, sr=int(sr * rate), n_steps=12)

    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
        sf.write(temp_file.name, y_high_pitch, int(sr * rate))
        processed_audio_path = temp_file.name

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(y, label="Original Audio", alpha=0.7)
    ax.plot(y_high_pitch, label="Processed Audio", alpha=0.7)
    ax.legend(loc="upper right")
    ax.set_xlabel("Time")
    ax.set_ylabel("Amplitude")
    plt.tight_layout()
    plt.savefig("waveform_chipmunk.png", dpi=300, bbox_inches='tight')
    plt.close()

    return processed_audio_path, "waveform_chipmunk.png"

def robot_effect(audio_path):
    y, sr = librosa.load(audio_path)
    y_low_pitch = librosa.effects.pitch_shift(y, sr=sr, n_steps=-6)
    y_robot = np.clip(y_low_pitch, -0.5, 0.5)

    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
        sf.write(temp_file.name, y_robot, sr)
        processed_audio_path = temp_file.name

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(y, label="Original Audio", alpha=0.7)
    ax.plot(y_robot, label="Processed Audio", alpha=0.7)
    ax.legend(loc="upper right")
    ax.set_xlabel("Time")
    ax.set_ylabel("Amplitude")
    plt.tight_layout()
    plt.savefig("waveform_robot.png", dpi=300, bbox_inches='tight')
    plt.close()

    return processed_audio_path, "waveform_robot.png"

def echo_effect(audio_path, delay=0.2):
    y, sr = librosa.load(audio_path)
    echo = np.zeros_like(y)
    delay_samples = int(delay * sr)
    echo[delay_samples:] = y[:-delay_samples]
    y_echo = y + 0.6 * echo

    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
        sf.write(temp_file.name, y_echo, sr)
        processed_audio_path = temp_file.name

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(y, label="Original Audio", alpha=0.7)
    ax.plot(y_echo, label="Processed Audio", alpha=0.7)
    ax.legend(loc="upper right")
    ax.set_xlabel("Time")
    ax.set_ylabel("Amplitude")
    plt.tight_layout()
    plt.savefig("waveform_echo.png", dpi=300, bbox_inches='tight')
    plt.close()

    return processed_audio_path, "waveform_echo.png"

def electronic_voice_effect(audio_path):
    y, sr = librosa.load(audio_path)
    y_low_pitch = librosa.effects.pitch_shift(y, sr=sr, n_steps=-3)
    noise = np.random.normal(0, 0.002, y.shape)
    y_electronic = np.sin(y_low_pitch * 2 * np.pi) + noise

    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
        sf.write(temp_file.name, y_electronic, sr)
        processed_audio_path = temp_file.name

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(y, label="Original Audio", alpha=0.7)
    ax.plot(y_electronic, label="Processed Audio", alpha=0.7)
    ax.legend(loc="upper right")
    ax.set_xlabel("Time")
    ax.set_ylabel("Amplitude")
    plt.tight_layout()
    plt.savefig("waveform_electronic.png", dpi=300, bbox_inches='tight')
    plt.close()

    return processed_audio_path, "waveform_electronic.png"

def stutter_effect(audio_path, repeat=3):
    y, sr = librosa.load(audio_path)
    y_stutter = np.concatenate([y[:len(y)//10]] * repeat + [y])

    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
        sf.write(temp_file.name, y_stutter, sr)
        processed_audio_path = temp_file.name

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(y, label="Original Audio", alpha=0.7)
    ax.plot(y_stutter, label="Processed Audio", alpha=0.7)
    ax.legend(loc="upper right")
    ax.set_xlabel("Time")
    ax.set_ylabel("Amplitude")
    plt.tight_layout()
    plt.savefig("waveform_stutter.png", dpi=300, bbox_inches='tight')
    plt.close()

    return processed_audio_path, "waveform_stutter.png"

def butter_lowpass_filter(data, cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = lfilter(b, a, data)
    return y

def remove_non_voice_sounds(y, sr):
    Y = np.fft.fft(y)
    freqs = np.fft.fftfreq(len(Y), 1/sr)
    Y[(freqs > 3000)] = 0
    Y[(freqs < 300)] = 0
    y_filtered = np.fft.ifft(Y).real
    return y_filtered

def remove_echo(y, sr, delay=0.2, attenuation=0.6):
    delay_samples = int(delay * sr)
    y_echo = np.zeros_like(y)
    y_echo[delay_samples:] = y[:-delay_samples]
    y_no_echo = y - attenuation * y_echo
    return y_no_echo

def process_voice(audio_path, cutoff=3000, delay=0.2, attenuation=0.6):
    y, sr = librosa.load(audio_path)
    y_filtered = butter_lowpass_filter(y, cutoff, sr)
    y_voice_only = remove_non_voice_sounds(y_filtered, sr)
    y_no_echo = remove_echo(y_voice_only, sr, delay, attenuation)

    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
        sf.write(temp_file.name, y_no_echo, sr)
        processed_audio_path = temp_file.name

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(y, label="Original Audio", alpha=0.7)
    ax.plot(y_no_echo, label="Processed Audio", alpha=0.7)
    ax.legend(loc="upper right")
    ax.set_xlabel("Time")
    ax.set_ylabel("Amplitude")
    plt.tight_layout()
    plt.savefig("waveform_voice_processing.png", dpi=300, bbox_inches='tight')
    plt.close()

    return processed_audio_path, "waveform_voice_processing.png"

def text_to_speech(text, lang='vi'):
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
        tts.save(temp_file.name)
        return temp_file.name

def speech_to_text(audio_path, language="vi-VN"):
    r = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio = r.record(source)
        text = r.recognize_google(audio, language=language)
        return text
    except sr.UnknownValueError:
        return "Không thể nhận diện giọng nói."
    except sr.RequestError as e:
        return f"Lỗi khi kết nối đến dịch vụ nhận diện: {e}"
    except Exception as e:
        return f"Lỗi: {str(e)}"
