from transformers import pipeline

def summarize_text(text, api_key=None):  # api_key parameter kept for compatibility
    # Initialize the summarization pipeline
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    
    # Split text into chunks if it's too long (BART has a max length of 1024 tokens)
    max_chunk_length = 1000
    chunks = [text[i:i + max_chunk_length] for i in range(0, len(text), max_chunk_length)]
    
    # Summarize each chunk
    summaries = []
    for chunk in chunks:
        if not chunk.strip():
            continue
        summary = summarizer(chunk, max_length=100, min_length=30, do_sample=False)
        summaries.append(summary[0]['summary_text'])
    
    # Combine all summaries
    final_summary = " ".join(summaries)
    
    return final_summary

if __name__ == "__main__":
    text_to_summarize = input("Enter the text to summarize: ")
    summary = summarize_text(text_to_summarize)
    print("Summary:")
    print(summary)