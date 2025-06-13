import typer
from datetime import timedelta
import whisper
from rich import print

app = typer.Typer(help="🎬 Submind: Smart Subtitle Generator (Whisper-based)")

def format_timestamp(seconds):
    milliseconds = int((seconds - int(seconds)) * 1000)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"

def write_srt(transcription, output_path, single_speaker: bool = False):
    with open(output_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(transcription["segments"], 1):
            f.write(f"{i}\n")
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"].strip()
            line = text if single_speaker else f"[Speaker ?]: {text}"
            f.write(f"{start} --> {end}\n")
            f.write(f"{line}\n\n")

@app.command()
def transcribe(
    input: str = typer.Argument(..., help="Input audio/video file path"),
    output: str = typer.Option("submind_output.srt", help="Path to output .srt file"),
    model_size: str = typer.Option("base", help="Whisper model size (tiny, base, small, medium, large)"),
    single: bool = typer.Option(False, "--single", help="Assume single speaker (omit speaker tags)"),
):

    print("[cyan]🔊 Loading Whisper model...[/cyan]")
    model = whisper.load_model(model_size)

    print("[yellow]🧠 Transcribing audio...[/yellow]")
    result = model.transcribe(input)

    print("[green]📄 Writing SRT file...[/green]")
    write_srt(result, output, single)

    print(f"[bold green]✅ Done! Subtitle saved to:[/bold green] [underline]{output}[/underline]")

if __name__ == "__main__":
    app()
