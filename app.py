
import streamlit as st
from vidstab import VidStab
import tempfile
import os
import subprocess

def stabilize_video(input_path, output_path):
    stabilizer = VidStab()
    stabilizer.stabilize(input_path=input_path, output_path=output_path, border_type='black')

def convert_to_h264(input_path, output_path):
    # Konverterar till H.264 codec med mp4-container via ffmpeg
    command = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        output_path
    ]
    subprocess.run(command, check=True)

st.set_page_config(page_title="AI Video Stabilizer", layout="centered")
st.title("🎥 AI Video Stabilizer")
st.markdown("Ladda upp ett skakigt videoklipp så stabiliserar vi det automatiskt med AI.")

uploaded_file = st.file_uploader("Ladda upp video (.mp4 eller .mov)", type=["mp4", "mov"])

if uploaded_file is not None:
    st.video(uploaded_file)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_input:
        temp_input.write(uploaded_file.read())
        temp_input_path = temp_input.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".avi") as temp_output:
        stabilized_path = temp_output.name

    with st.spinner("Stabiliserar videon..."):
        stabilize_video(temp_input_path, stabilized_path)

        # Konvertera till H.264 efter stabilisering
        final_output_path = stabilized_path.replace(".avi", "_final.mp4")
        convert_to_h264(stabilized_path, final_output_path)

    st.success("✅ Färdig!")
    st.video(final_output_path)

    with open(final_output_path, "rb") as f:
        st.download_button(
            label="📥 Ladda ner stabiliserad video (H.264, mp4)",
            data=f,
            file_name="stabilized_video.mp4",
            mime="video/mp4"
        )

    # Rensa temporära filer efteråt (valfritt)
    try:
        os.remove(temp_input_path)
        os.remove(stabilized_path)
        os.remove(final_output_path)
    except Exception:
        pass
