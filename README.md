# YouTube AI Video Summarizer
A modern web application that automatically generates concise summaries from YouTube videos using Facebook's BART Large Model.

Click here for live demo : https://drive.google.com/file/d/1WryCgvnBL_dzH4BYgYOKFrhjnrcyFM4h/view?usp=sharing

## Table of Contents
* [General Info](#general-information)
* [Features](#features)
* [Tools and Technologies](#tools-and-technologies)
* [Setup](#setup)
* [Usage](#usage)
* [Credits](#credits)


## General Information
This project provides an efficient solution for extracting and summarizing content from YouTube videos. Instead of watching entire videos to understand their content, this tool automatically generates concise summaries using advanced AI technology. It features a modern, dark-themed interface with glass morphism effects for an enhanced user experience.

![Screenshot 2024-11-29 at 10 30 30 PM](https://github.com/user-attachments/assets/7d76e069-52fd-45c5-8e6f-7b74222678fb)

## Features
* AI-Powered Summarization: Utilizes Facebook's BART Large Model for accurate content summarization
* Automatic Transcript Extraction: Seamlessly extracts transcripts from YouTube videos
* Modern UI Design: Features a sleek dark theme with glass morphism effects
* Fast Processing: Generates summaries within seconds
* Error Handling: Provides clear error messages for invalid URLs or unavailable transcripts
* Responsive Design: Adapts to different screen sizes for optimal viewing
* User-Friendly Interface: Simple "paste and click" functionality


## Tools and Technologies
* **Frontend Framework:**
  - Streamlit (Python web framework)
  - Custom CSS for styling and glass morphism effects

* **AI/ML Technologies:**
  - Facebook's BART Large Model (for text summarization)
  - Hugging Face Transformers library
  - PyTorch

* **APIs and Libraries:**
  - YouTube Transcript API (for extracting video transcripts)
  - BeautifulSoup4 (for web scraping)
  - Requests (for HTTP requests)
  - SentencePiece (for text tokenization)


## Setup

1. **Install Python:**
   - If you haven't already, install Python 3.8 or higher on your local machine. You can download it from the [Python official website](https://www.python.org/).

2. **Install Required Modules:**
   - Open a terminal or command prompt
   - Run the following commands to install the necessary modules using pip:

   ```bash
   pip install streamlit
   pip install transformers
   pip install youtube_transcript_api
   pip install torch


## Usage

To use the YouTube AI Video Summarizer, follow these steps:

1. **Clone the Repository:**
   - Clone this repository to your local machine using Git:
     ```bash
     git clone https://github.com/yourusername/youtube-ai-summarizer.git
     ```

2. **Run the Application:**
   - Start the Streamlit application by running:
     ```bash
     streamlit run app.py
     ```

3. **Using the App:**
   - Copy a YouTube video URL
   - Paste it into the input field
   - Click "✨ Generate Summary"
   - View the video details and AI-generated summary

4. **Important Notes:**
   - Ensure the YouTube video has closed captions available
   - For longer videos, the summarization process might take a few moments
   - The summary quality depends on the transcript clarity

## Additional Notes:
* The app requires an active internet connection
* Make sure all dependencies are properly installed
* Some videos might not have available transcripts
* The app works best with English language videos


<div align="center">
Made by Vijay Shrivarshan Vijayaraja
</div>

