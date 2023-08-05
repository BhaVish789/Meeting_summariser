import os
import streamlit as st
from gpt import get_meeting_summary, get_action_items
from transcripts import save_and_clean_file, count_tokens


st.markdown("# Welcome to MoM GPT! 🤗")
st.markdown(
    "##### This app lets you create minutes of the meetings (MoMs) with summary, discussion points, and action times in real time using ChatGPT."
)
st.markdown(
    "##### And guess what, you can also use the meeting transcripts to do the same. 😉"
)

st.markdown("")
uploaded_file = st.file_uploader('Upload a .vtt, .docx or .mp4 file', type=['vtt', 'docx', 'mp4'])

if uploaded_file is not None:
    latest_iteration = st.empty()
    bar = st.progress(0)

    status = st.text("Uploading and Cleaning file...")

    if uploaded_file.type == 'video/mp4':
        # get the file path
        file_path = os.path.join(os.getcwd(), uploaded_file.name)

        # save the file to disk
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.read())

        # update the uploaded file to the vtt file
        uploaded_file = open(vtt_file_path, 'rb')

    filepath = save_and_clean_file(uploaded_file)
    status.text("Uploading and Cleaning file... Done")
    bar.progress(10)

    #token_count = count_tokens(filepath)
    #st.write(f"Number of tokens: {token_count}")

    status.text("Creating a summary...")
    meeting_summary = get_meeting_summary(filepath)
    status.text("Creating a summary... Done")
    st.markdown("#### Meeting Summary")
    st.markdown(meeting_summary)
    bar.progress(50)

    status.text("Extracting action items...")
    action_items = get_action_items(filepath)
    status.text("")
    st.markdown("#### Action Items")
    st.markdown(action_items)
    bar.progress(100)

    st.markdown("#### Hope it helped!")
    st.balloons()

    # delete the uploaded file and vtt file from disk (if it exists)
    uploaded_file.close()
    if 'vtt_file_path' in locals():
        os.remove(vtt_file_path)

else:
    st.write("Please upload a file.")

footer = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    text-align: center;
}
</style>
"""
st.markdown(footer, unsafe_allow_html=True)
