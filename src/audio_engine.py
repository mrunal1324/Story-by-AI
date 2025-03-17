import pyttsx3
import os
import tempfile
import re

def text_to_speech(text, voice_gender='female', rate=150):
    """
    Convert text to speech and save as an audio file.
    
    Args:
        text (str): The text to convert to speech
        voice_gender (str): 'male' or 'female'
        rate (int): Speech rate (words per minute)
        
    Returns:
        str: Path to the generated audio file
    """
    engine = pyttsx3.init()
    
    # Get available voices
    voices = engine.getProperty('voices')
    
    # Select voice based on gender preference
    if voice_gender.lower() == 'female' and len(voices) > 1:
        engine.setProperty('voice', voices[1].id)
    else:
        engine.setProperty('voice', voices[0].id)
    
    # Adjust rate based on content length
    # Slower for shorter content, faster for longer content
    text_length = len(text.split())
    if text_length < 100:
        adjusted_rate = rate - 20  # Slower for short stories
    elif text_length > 500:
        adjusted_rate = rate + 20  # Faster for long stories
    else:
        adjusted_rate = rate
    
    engine.setProperty('rate', adjusted_rate)
    
    # Improve speech by adding pauses at punctuation
    text = re.sub(r'\.', '.\n', text)  # Add newlines after periods
    text = re.sub(r'\!', '!\n', text)  # Add newlines after exclamation marks
    text = re.sub(r'\?', '?\n', text)  # Add newlines after question marks
    
    # Create a unique temp file name to avoid conflicts
    temp_audio_path = os.path.join(tempfile.gettempdir(), f"story_audio_{os.getpid()}.wav")
    
    # Generate and save the audio
    engine.save_to_file(text, temp_audio_path)
    engine.runAndWait()
    
    return temp_audio_path