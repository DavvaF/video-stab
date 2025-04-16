
import streamlit as st
import tempfile
import os
from vidstab import VidStab

def stabilize_video(input_path, output_path):
    stabilizer = VidStab()
    stabilizer.stabilize(input_path=input_path, output_path=output_path)

st.title("AI-baserad Videostabilisering (Beta)")

st.write("Ladda upp en skakig .mp4 eller .mov-video nedan. Vi stabiliserar den automatiskt med AI och du får en ny version att ladda ner.")

uploaded_file = st.file_uploader("Ladda upp din video (.mp4, .mov)", type=["mp4", "mov"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_input:
        temp_input.write(uploaded_file.read())
        temp_input_path = temp_input.name

    st.video(temp_input_path)

    if st.button("Stabilisera video"):
        with st.spinner("Stabiliserar videon... detta kan ta en stund beroende på längd."):
            temp_output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
            stabilize_video(temp_input_path, temp_output_path)

            st.success("Färdig! Klicka nedan för att ladda ner den stabiliserade videon.")
            with open(temp_output_path, "rb") as file:
                st.download_button(
                    label="Ladda ner stabiliserad video",
                    data=file,
                    file_name="stabiliserad_video.mp4",
                    mime="video/mp4"
                )

        os.remove(temp_input_path)
        os.remove(temp_output_path)
