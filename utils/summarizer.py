from transformers import pipeline
from utils.text_chunker import chunk_text

summarizer = pipeline(
    task="summarization",
    model="sshleifer/distilbart-cnn-12-6"
)

def summarize_long_text(text, max_len, min_len):

    chunks = chunk_text(text)

    summaries = []

    for chunk in chunks:

        result = summarizer(
            chunk,
            max_length=max_len,
            min_length=min_len,
            num_beams=6,
            length_penalty=2.0,
            early_stopping=True,
            do_sample=False
        )

        summaries.append(
            result[0]["summary_text"]
        )

    return "\n\n".join(summaries)