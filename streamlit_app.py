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

st.set_page_config(
      page_title="Ứng dụng Âm thanh",
      page_icon="🎵",
      layout="wide",
      initial_sidebar_state="expanded",
   )
# CSS tùy chỉnh với icon và hiệu ứng
st.markdown(
    """
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');

    body {
        background-color: #121212;
        color: #ffffff;
        font-family: 'Roboto', sans-serif;
    }
    .stButton>button {
        background-color: #6200ea;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .stButton>button:hover {
        background-color: #3700b3;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .stTextInput>div>input, .stTextArea>div>textarea {
        background-color: #1e1e1e;
        color: white;
        border: 1px solid #6200ea;
        border-radius: 5px;
        padding: 10px;
    }
    .stRadio>div>label, .stSlider>div>label {
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
    .icon-button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }
    .material-icons {
        font-size: 20px;
        margin-right: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Tiêu đề ứng dụng với icon
st.title("🎵 Sound Application")

# Định nghĩa từ điển 'languages' ở phạm vi toàn cục
languages = {
    "Tiếng Việt": "vi",
    "Tiếng Anh": "en",
    "Tiếng Pháp": "fr",
    "Tiếng Đức": "de",
    "Tiếng Tây Ban Nha": "es",
    "Tiếng Ý": "it",
    "Tiếng Bồ Đào Nha": "pt",
    "Tiếng Nga": "ru",
    "Tiếng Nhật": "ja",
    "Tiếng Hàn": "ko"
}

# Sidebar for navigation
st.sidebar.title("🎯 Chọn chức năng")
option = st.sidebar.selectbox("Chọn một chức năng:",
                              ["Hiệu ứng âm thanh", "Chuyển đổi văn bản thành giọng nói", "Nhận diện giọng nói"])

if option == "Hiệu ứng âm thanh":
    st.header("🎼 Hiệu ứng Âm thanh")

    st.write("Nhấn để ghi âm giọng nói:")
    audio_data = st_audiorec()
    audio_file = st.file_uploader("📥 Tải tệp âm thanh lên", type=["wav", "mp3"])

    effect_type = st.selectbox(
        "🎛️ Chọn hiệu ứng âm thanh",
        ["Giọng Chipmunk", "Giọng Robot", "Hiệu ứng Echo", "Giọng Điện Tử", "Hiệu ứng Stutter", "Xử lý tiếng nói"]
    )

    # Các tham số cho hiệu ứng
    if effect_type == "Hiệu ứng Echo":
        delay = st.slider("⏱️ Độ trễ (s) cho Echo", 0.1, 1.0, 0.2, step=0.1)
    else:
        delay = 0.2

    if effect_type == "Hiệu ứng Stutter":
        repeat = st.slider("🔁 Số lần lặp lại cho Stutter", 1, 5, 3, step=1)
    else:
        repeat = 3

    # Nút áp dụng hiệu ứng với icon
    if st.button("✨ Áp dụng hiệu ứng"):
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
            st.image(waveform_path, use_container_width=True)

elif option == "Chuyển đổi văn bản thành giọng nói":
    st.header("🗣️ Chuyển đổi Văn bản thành Giọng nói")
    text_input = st.text_area("💬 Nhập văn bản để chuyển đổi thành giọng nói", placeholder="Nhập văn bản ở đây...", height=200)

    # Chọn ngôn ngữ đầu vào
    input_language_name = st.selectbox("🌐 Chọn ngôn ngữ đầu vào:", list(languages.keys()))
    input_language = languages[input_language_name]

    # Chọn ngôn ngữ đầu ra
    output_language_name = st.selectbox("🌐 Chọn ngôn ngữ đầu ra:", list(languages.keys()))
    output_language = languages[output_language_name]

    # Nút chuyển đổi văn bản thành giọng nói với icon
    if st.button("🔊 Chuyển đổi văn bản thành giọng nói"):
        if text_input:
            # Dịch văn bản sang ngôn ngữ đầu ra
            translator = Translator()
            translated_text = translator.translate(text_input, src=input_language, dest=output_language).text
            tts_output_path = text_to_speech(translated_text, output_language)
            st.audio(tts_output_path)

elif option == "Nhận diện giọng nói":
    st.header("📝 Nhận diện Giọng nói")
    st.subheader("🎤 Ghi âm giọng nói trực tiếp")

    st.write("Nhấn để ghi âm giọng nói:")
    audio_data = st_audiorec()

    # Danh sách các ngôn ngữ cho nhận diện giọng nói
    stt_languages = {
        "Tiếng Việt": "vi-VN",
        "Tiếng Anh": "en-US",
        "Tiếng Pháp": "fr-FR",
        "Tiếng Đức": "de-DE",
        "Tiếng Tây Ban Nha": "es-ES",
        "Tiếng Ý": "it-IT",
        "Tiếng Bồ Đào Nha": "pt-PT",
        "Tiếng Nga": "ru-RU",
        "Tiếng Nhật": "ja-JP",
        "Tiếng Hàn": "ko-KR"
    }

    # Chọn ngôn ngữ đầu vào
    input_language_name = st.selectbox("🌐 Chọn ngôn ngữ đầu vào:", list(stt_languages.keys()))
    input_language = stt_languages[input_language_name]

    # Chọn ngôn ngữ dịch sang (sử dụng từ điển languages ở trên)
    output_language_name = st.selectbox("🌐 Chọn ngôn ngữ dịch sang:", list(languages.keys()))
    output_language = languages[output_language_name]

    if st.button("🌟 Nhận diện và Dịch thuật"):
        if audio_data is not None:
            # Lưu tệp âm thanh tạm thời
            with open("temp_audio.wav", "wb") as f:
                f.write(audio_data)

            # Nhận diện giọng nói
            stt_result = speech_to_text("temp_audio.wav", language=input_language)
            # Hiển thị văn bản nhận diện
            st.text_area("📝 Văn bản từ giọng nói", value=stt_result, height=200)

            # Dịch văn bản
            translator = Translator()
            # Lấy mã ngôn ngữ gốc từ input_language (ví dụ: 'vi-VN' -> 'vi')
            src_language_code = input_language.split("-")[0]
            translated_text = translator.translate(stt_result, src=src_language_code, dest=output_language).text
            st.text_area("🌐 Văn bản sau khi dịch", value=translated_text, height=200)

# Hàm cleanup
def cleanup():
    temp_files = ["temp_audio.wav", "speed_adjusted_audio.wav"]
    for file in temp_files:
        try:
            if os.path.exists(file):
                os.remove(file)
        except Exception as e:
            st.error(f"Lỗi khi xóa file tạm thời: {e}")

# Thêm nút cleanup trong sidebar với icon
if st.sidebar.button("🧹 Dọn dẹp file tạm"):
    cleanup()
    st.sidebar.success("✅ Đã xóa các file tạm thời!")
