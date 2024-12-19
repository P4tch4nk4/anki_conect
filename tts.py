#!/usr/bin/env python3

import os
import openai
from pathlib import Path
from random import choice

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

voices = ("alloy", "echo", "onyx", "shimmer")

file_path = Path(__file__).parent / 'audios'

os.makedirs(file_path, exist_ok=True)


def text_to_speech(text: str, voice=None):
    speech_file_path = text.replace('?', '')
    speech_file_path = speech_file_path.replace(' ', '_')
    speech_file_path = file_path / f"{speech_file_path}.mp3"
    with openai.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice=voice if voice else choice(voices),
        input=text,
    ) as response:
        response.stream_to_file(speech_file_path)
    return speech_file_path
