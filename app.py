import streamlit as st
from scrape import extract_video_id, get_transcript, extract_metadata
from summarize import summarize_text
import os

def set_custom_style():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* Dark theme colors */
        :root {
            --bg-primary: #0F172A;
            --bg-secondary: #1E293B;
            --text-primary: #E2E8F0;
            --text-secondary: #94A3B8;
            --accent-primary: #EF4444;
            --accent-secondary: #DC2626;
            --accent-gradient: linear-gradient(135deg, #EF4444 0%, #B91C1C 100%);
            --error-bg: #7F1D1D;
            --error-border: #DC2626;
            --warning-bg: #78350F;
            --warning-border: #D97706;
        }
        
        .stApp {
            background: linear-gradient(135deg, var(--bg-primary) 0%, #1A237E 100%);
            font-family: 'Inter', sans-serif;
        }
        
        /* Hide Streamlit branding */
        #MainMenu, footer, header {
            visibility: hidden;
        }
        
        .result-container {
            background: rgba(30, 41, 59, 0.7);
            padding: 2.5rem;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin: 2rem 1rem;
            max-width: 1200px;
        }
        
        .title-container {
            background: var(--accent-gradient);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            margin-bottom: 2.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 8px 32px rgba(239, 68, 68, 0.3);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .title-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, transparent 0%, rgba(255,255,255,0.1) 50%, transparent 100%);
            transform: translateX(-100%);
            transition: transform 0.5s ease;
        }
        
        .title-container:hover::before {
            transform: translateX(100%);
        }
        
        .url-input {
            background: var(--bg-secondary);
            border: 2px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            transition: all 0.3s ease;
        }
        
        .url-input:hover {
            border-color: var(--accent-primary);
            box-shadow: 0 0 20px rgba(239, 68, 68, 0.2);
        }
        
        /* Override Streamlit's default input styling */
        .stTextInput > div > div > input {
            background-color: rgba(30, 41, 59, 0.7) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: var(--text-primary) !important;
            border-radius: 8px !important;
            padding: 0.75rem 1rem !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: var(--accent-primary) !important;
            box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.2) !important;
        }
        
        .summary-container {
            background: rgba(30, 41, 59, 0.7);
            padding: 2rem;
            border-radius: 15px;
            margin-top: 2rem;
            border-left: 5px solid var(--accent-primary);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
            color: var(--text-primary);
        }
        
        .summary-container:hover {
            transform: translateX(5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        }
        
        .video-info {
            background: rgba(30, 41, 59, 0.7);
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1.5rem 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
            color: var(--text-primary);
        }
        
        .video-info:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        }
        
        .stButton > button {
            background: var(--accent-gradient) !important;
            color: white !important;
            padding: 0.8rem 2rem !important;
            border-radius: 10px !important;
            border: none !important;
            box-shadow: 0 5px 15px rgba(239, 68, 68, 0.3) !important;
            transition: all 0.3s ease !important;
            font-weight: 600 !important;
            letter-spacing: 0.5px !important;
            width: 100% !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(239, 68, 68, 0.4) !important;
        }
        
        .stats-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin: 2.5rem 0;
        }
        
        .stat-card {
            background: rgba(30, 41, 59, 0.7);
            padding: 1.8rem;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
            border-color: var(--accent-primary);
        }
        
        .error-message {
            background-color: var(--error-bg);
            color: #FCA5A5;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid var(--error-border);
            margin: 1rem 0;
        }
        
        .warning-message {
            background-color: var(--warning-bg);
            color: #FCD34D;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid var(--warning-border);
            margin: 1rem 0;
        }
        
        /* Loading spinner color */
        .stSpinner > div {
            border-top-color: var(--accent-primary) !important;
        }
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--bg-secondary);
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--accent-primary);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--accent-secondary);
        }
        </style>
    """, unsafe_allow_html=True)

def get_transcript_from_url(url):
    video_id = extract_video_id(url)
    transcript = get_transcript(video_id)
    return transcript

def summarize_transcript(transcript):
    summary = summarize_text(transcript)
    return summary

def main():
    set_custom_style()
    
    # Title Section with animation
    st.markdown("""
        <div class="title-container">
            <img src="https://i.pinimg.com/originals/3a/36/20/3a36206f35352b4230d5fc9f17fcea92.png" 
                 style="width: 60px; height: 60px; margin-right: 20px;">
            <div>
                <h1 style="margin: 0; font-size: 2.5em; font-weight: 700;">YouTube AI Video Summarizer App</h1>
                <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Created by Vijay Shrivarshan Vijayaraja</p>
                <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Powered by Facebook's BART Large Model</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Description with features
    st.markdown("""
        <div style="text-align: center; margin: 2rem 0 3rem 0;">
            <p style="font-size: 1.2em; color: #E2E8F0; margin-bottom: 1.5rem;">
                Transform lengthy YouTube videos into concise, actionable summaries with AI
            </p>
            <div class="stats-container">
                <div class="stat-card">
                    <h3 style="color: #EF4444; margin: 0;">⚡️ Fast</h3>
                    <p style="color: #94A3B8; margin: 0.5rem 0;">Get summaries in seconds</p>
                </div>
                <div class="stat-card">
                    <h3 style="color: #EF4444; margin: 0;">🎯 Accurate</h3>
                    <p style="color: #94A3B8; margin: 0.5rem 0;">AI-powered precision</p>
                </div>
                <div class="stat-card">
                    <h3 style="color: #EF4444; margin: 0;">✨ Simple</h3>
                    <p style="color: #94A3B8; margin: 0.5rem 0;">Just paste and click</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # URL Input with icon
    st.markdown("""
        <div class="url-input">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="color: #EF4444; margin-right: 0.5rem;">🔗</span>
                <span style="font-weight: 500; color: #E2E8F0;">Enter YouTube URL</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    url = st.text_input("", placeholder="https://www.youtube.com/watch?v=...", label_visibility="collapsed")

    # Generate Summary Button
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    summarize_button = st.button("✨ Generate Summary", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if summarize_button:
        if url:
            try:
                with st.spinner("🎥 Fetching video details..."):
                    title, channel = extract_metadata(url)
                    st.markdown("""<div class="result-container">""", unsafe_allow_html=True)
                    st.markdown(f"""
                        <div class="video-info">
                            <h4 style="color: #EF4444; margin: 0; font-size: 1.2em;">Video Details</h4>
                            <div style="margin-top: 1rem;">
                                <p style="font-weight: 600; margin: 0.5rem 0; font-size: 1.1em; color: #E2E8F0;">📺 {title}</p>
                                <p style="color: #94A3B8; margin: 0.5rem 0;">👤 {channel}</p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with st.spinner("🤖 Generating summary... This may take a minute..."):
                    transcript = get_transcript_from_url(url)
                    summary = summarize_transcript(transcript)
                    st.markdown(f"""
                        <div class="summary-container">
                            <h4 style="color: #EF4444; margin: 0 0 1.5rem 0; font-size: 1.2em;">
                                <span style="margin-right: 0.5rem;">📝</span>Summary
                            </h4>
                            <p style="line-height: 1.8; color: #E2E8F0; font-size: 1.1em;">{summary}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                    <div class="error-message">
                        <strong>❌ Error:</strong> {str(e)}
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="warning-message">
                    <strong>⚠️ Warning:</strong> Please enter a valid YouTube URL.
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
