from googletrans import Translator  # Add this if not already

def format_timestamp(seconds):
    milliseconds = int((seconds - int(seconds)) * 1000)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"

def write_srt(transcription, output_path, translate_to=None):
    translator = Translator()

    with open(output_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(transcription["segments"], 1):
            f.write(f"{i}\n")
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"].strip()

            if translate_to:
                try:
                    text = translator.translate(text, dest=translate_to).text
                except Exception as e:
                    print(f"Translation failed on segment {i}: {e}")

            f.write(f"{start} --> {end}\n")
            f.write(f"{text}\n\n")
