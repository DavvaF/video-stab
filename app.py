
import streamlit as st
import tempfile
import os
import cv2
from vidstab import VidStab
import subprocess

st.set_page_config(page_title="AI Video Stabilizer", layout="centered")
st.title("🎥 AI Video Stabilizer")

def save_uploaded_file(uploadedfile):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
        tmp.write(uploadedfile.read())
        return tmp.name

def convert_to_h264(input_path, output_path):
    command = [
        "ffmpeg",
        "-i", input_path,
        "-vcodec", "libx264",
        "-acodec", "aac",
        "-b:a", "128k",
        output_path
    ]
    subprocess.run(command, check=True)

uploaded_file = st.file_uploader("Ladda upp en video (.mp4)", type=["mp4"])

if uploaded_file is not None:
    input_path = save_uploaded_file(uploaded_file)
    st.video(input_path)

    st.write("⏳ Stabiliserar video...")

    stab = VidStab()
    stabilized_path = input_path.replace(".mp4", "_stab.avi")

    stab.stabilize(input_path=input_path, output_path=stabilized_path)

    # Konvertera till H.264 efter stabilisering
    final_output_path = stabilized_path.replace(".avi", "_final.mp4")
    convert_to_h264(stabilized_path, final_output_path)

    st.success("✅ Färdig!")
    st.video(final_output_path)

    with open(final_output_path, "rb") as file:
        st.download_button(
            label="Ladda ner stabiliserad video",
            data=file,
            file_name="stabiliserad_video.mp4",
            mime="video/mp4"
        )
