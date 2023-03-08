import streamlit as st
from helper import *
import time

# Define Streamlit app
st.title("WPM Speaking Calculator")

# File Upload Section
file_object = st.file_uploader(label="Please upload your file")
if file_object:
    token, t_id = upload_file(file_object)

    # Polling Section
    result = {}
    sleep_duration = 1
    percent_complete = 0
    progress_bar = st.progress(percent_complete)
    st.text("Currently in queue")

    # Wait until the transcription process starts
    while result.get("status") != "processing":
        percent_complete += sleep_duration
        time.sleep(sleep_duration)
        progress_bar.progress(percent_complete / 10)
        result = get_text(token, t_id)

    # Wait until the transcription process completes
    sleep_duration = 0.01
    for percent in range(percent_complete, 101):
        time.sleep(sleep_duration)
        progress_bar.progress(percent)

    with st.spinner("Processing....."):
        while result.get("status") != 'completed':
            result = get_text(token, t_id)

    # Calculate WPM Section
    transcript = result['text']
    duration = result['audio_duration']
    wpm = calculate_words_per_minute(transcript, duration)

    # Display Results
    st.header("Calculate WPM")
    if wpm > 160:
        st.write(f'You are speaking too fast {wpm:.2f} wpm. Slow down!')
    elif wpm < 120:
        st.write(f'You are speaking too slow {wpm:.2f} wpm. Speed up!')
    else:
        st.write(f'Your speaking rate is good {wpm:.2f} wpm. Keep it up!')

    st.header("Transcribed Text")
    st.write(transcript)

