import sounddevice as sd
import soundfile as sf
import openai
import config

# Set your OpenAI API key
openai.api_key = config.OPENAI_API_KEY

# Parameters
duration = 10  # Recording duration in seconds
sample_rate = 44100  # Sample rate in Hertz
channels = 1  # Mono recording

# Filename for the recorded audio
audio_filename = 'recording.wav'

# Filename for the transcription output
transcript_filename = 'transcription.txt'

def record_audio(duration, sample_rate, channels):
    print("Recording started...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels)
    sd.wait()
    print("Recording finished.")
    return recording

def save_audio(filename, data, sample_rate):
    sf.write(filename, data, sample_rate)
    print(f"Audio saved to {filename}")

def transcribe_audio(filename):
    with open(filename, 'rb') as audio_file:
        transcript = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
        )
    return transcript.text

def save_transcript(filename, text):
    with open(filename, 'w') as f:
        f.write(text)
    print(f"Transcript saved to {filename}")

def main():
    # Record audio from the microphone
    audio_data = record_audio(duration, sample_rate, channels)
    
    # Save the recorded audio to a file
    save_audio(audio_filename, audio_data, sample_rate)
    
    # Transcribe the audio file using OpenAI's Whisper API
    transcription = transcribe_audio(audio_filename)
    
    # Save the transcription to a text file
    save_transcript(transcript_filename, transcription)

if __name__ == '__main__':
    main()
