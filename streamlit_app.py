import streamlit as st
from audio_effects import (chipmunk_effect, robot_effect, echo_effect,
                         electronic_voice_effect, stutter_effect,
                         process_voice, text_to_speech, speech_to_text)
from st_audiorec import st_audiorec
from googletrans import Translator
from pydub import AudioSegment
import librosa
import soundfile as sf
import numpy as np
import os

# CSS tùy chỉnh
st.markdown(
    """
    <style>
    body {
        background-color: #121212;
        color: #ffffff;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #6200ea;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #3700b3;
    }
    .stTextInput>div>input {
        background-color: #1e1e1e;
        color: white;
        border: 1px solid #6200ea;
        border-radius: 5px;
        padding: 10px;
    }
    .stTextArea>div>textarea {
        background-color: #1e1e1e;
        color: white;
        border: 1px solid #6200ea;
        border-radius: 5px;
        padding: 10px;
    }
    .stRadio>div>label {
        color: #ffffff;
    }
    .stSlider>div>label {
        color: #ffffff;
    }
    .stImage > img {
        width: 100%;
        max-width: 100%;
        height: auto;
        object-fit: contain;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Tiêu đề ứng dụng
st.title("Sound Application")

# Sidebar for navigation
st.sidebar.title("Chọn chức năng")
option = st.sidebar.radio("Chọn một chức năng:",
                         ["Hiệu ứng âm thanh", "Chuyển đổi văn bản thành giọng nói", "Nhận diện giọng nói"])

if option == "Hiệu ứng âm thanh":
    st.header("Hiệu ứng Âm thanh")

    st.write("Nhấn để ghi âm giọng nói")
    audio_data = st_audiorec()
    audio_file = st.file_uploader("Tải tệp âm thanh lên", type=["wav", "mp3"])

    effect_type = st.radio(
        "Chọn hiệu ứng âm thanh",
        ["Giọng Chipmunk", "Giọng Robot", "Hiệu ứng Echo", "Giọng Điện Tử", "Hiệu ứng Stutter", "Xử lý tiếng nói"]
    )

    # Các tham số cho hiệu ứng
    if effect_type == "Hiệu ứng Echo":
        delay = st.slider("Độ trễ (s) cho Echo", 0.1, 1.0, 0.2)
    else:
        delay = 0.2

    if effect_type == "Hiệu ứng Stutter":
        repeat = st.slider("Số lần lặp lại cho Stutter", 1, 5, 3)
    else:
        repeat = 3

    # Nút áp dụng hiệu ứng
    if st.button("Áp dụng hiệu ứng"):
        if audio_file is not None or audio_data is not None:
            # Lưu tệp âm thanh tạm thời
            if audio_file is not None:
                with open("temp_audio.wav", "wb") as f:
                    f.write(audio_file.getbuffer())
            elif audio_data is not None:
                with open("temp_audio.wav", "wb") as f:
                    f.write(audio_data)

            # Áp dụng hiệu ứng
            if effect_type == "Giọng Chipmunk":
                processed_audio_path, waveform_path = chipmunk_effect("temp_audio.wav")
            elif effect_type == "Giọng Robot":
                processed_audio_path, waveform_path = robot_effect("temp_audio.wav")
            elif effect_type == "Hiệu ứng Echo":
                processed_audio_path, waveform_path = echo_effect("temp_audio.wav", delay)
            elif effect_type == "Giọng Điện Tử":
                processed_audio_path, waveform_path = electronic_voice_effect("temp_audio.wav")
            elif effect_type == "Hiệu ứng Stutter":
                processed_audio_path, waveform_path = stutter_effect("temp_audio.wav", repeat)
            elif effect_type == "Xử lý tiếng nói":
                processed_audio_path, waveform_path = process_voice("temp_audio.wav", delay=delay)

            # Hiển thị âm thanh đã xử lý
            st.audio(processed_audio_path)

            # Hiển thị đồ thị sóng âm
            st.write("### Phân tích dạng sóng")
            st.image(waveform_path, use_container_width=True)

elif option == "Chuyển đổi văn bản thành giọng nói":
    st.header("Chuyển đổi văn bản thành giọng nói")
    text_input = st.text_area("Nhập văn bản để chuyển đổi thành giọng nói", placeholder="Nhập văn bản ở đây...")

    # Chọn ngôn ngữ đầu vào
    input_language = st.selectbox("Chọn ngôn ngữ đầu vào:", ["vi", "en", "fr", "de", "es", "it", "pt", "ru", "ja", "ko"])

    # Chọn ngôn ngữ đầu ra
    output_language = st.selectbox("Chọn ngôn ngữ đầu ra:", ["vi", "en", "fr", "de", "es", "it", "pt", "ru", "ja", "ko"])

    # Nút chuyển đổi văn bản thành giọng nói
    if st.button("Chuyển đổi văn bản thành giọng nói"):
        if text_input:
            # Dịch văn bản sang ngôn ngữ đầu ra
            translator = Translator()
            translated_text = translator.translate(text_input, src=input_language, dest=output_language).text
            tts_output_path = text_to_speech(translated_text, output_language)
            st.audio(tts_output_path)

elif option == "Nhận diện giọng nói":
    st.header("Nhận diện giọng nói")
    st.subheader("🎤 Ghi âm giọng nói trực tiếp")

    st.write("Nhấn để ghi âm giọng nói")
    audio_data = st_audiorec()

    # Chọn ngôn ngữ đầu vào
    input_language = st.selectbox("Chọn ngôn ngữ đầu vào:", ["vi-VN", "en-US", "fr-FR", "de-DE", "es-ES", "it-IT", "pt-PT", "ru-RU", "ja-JP", "ko-KR"])

    # Chọn ngôn ngữ dịch sang
    output_language = st.selectbox("Chọn ngôn ngữ dịch sang:", ["vi", "en", "fr", "de", "es", "it", "pt", "ru", "ja", "ko"])

    if st.button("Nhận diện và Dịch thuật"):
        if audio_data is not None:
            # Lưu tệp âm thanh tạm thời
            with open("temp_audio.wav", "wb") as f:
                f.write(audio_data)

            # Nhận diện giọng nói
            stt_result = speech_to_text("temp_audio.wav", language=input_language)
            # Hiển thị văn bản nhận diện
            st.text_area("Văn bản từ giọng nói", value=stt_result, height=200)

            # Dịch văn bản
            translator = Translator()
            translated_text = translator.translate(stt_result, src=input_language.split("-")[0], dest=output_language).text
            st.text_area("Văn bản sau khi dịch", value=translated_text, height=200)

# Hàm cleanup
def cleanup():
    temp_files = ["temp_audio.wav", "speed_adjusted_audio.wav"]
    for file in temp_files:
        try:
            if os.path.exists(file):
                os.remove(file)
        except Exception as e:
            st.error(f"Lỗi khi xóa file tạm thời: {e}")

# Thêm nút cleanup trong sidebar
if st.sidebar.button("Dọn dẹp file tạm"):
    cleanup()
    st.sidebar.success("Đã xóa các file tạm thời!")
