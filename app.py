import streamlit as st
from dotenv import load_dotenv

load_dotenv()
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi


genai.configure(api_key=os.getenv("GOGGLE_API_KEY"))

prompt = """You are a Youtube video summarizer. You will be taking the transcript 
text and summarizing the entire video and providing the important summary in points 
within 200 or 250 words. Please provide the summary of text given here :  """

##getting th etranscript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        print(video_id)
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)
        print(transcript_text)
        
        transcript = ""
        for i in transcript_text:
            transcript += i["text"]
        return transcript_text
    
    except Exception as e:
        raise e
    

## getting the summary based on prompt Google Gemini
def generate_gemini_content(transcript_text,prompt):
    model=genai.GenerativeModel("gemini-pro")
    transcript_text_str = ' '.join([item['text'] for item in transcript_text if isinstance(item, dict) and 'text' in item])
    response=model.generate_content(prompt+transcript_text_str)
    return response.text

st.title("""Youtube Video Summarizer""")    
youtube_link = st.text_input("Enter the Youtube video URL")

if youtube_link:
    video_id=youtube_link.split("=")[1]
    st.image("https://img.youtube.com/vi/"+video_id+"/0.jpg", use_column_width=True)

if st.button("Get detailed notes"):
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
            summary=generate_gemini_content(transcript_text,prompt)
            st.markdown("## Detailed Notes:")
            st.write(summary)
            
            
