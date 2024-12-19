#!/usr/bin/env python3

import requests
from tts import text_to_speech
from argparse import ArgumentParser
from translator import translate
import base64

parser = ArgumentParser()

parser.add_argument('-d', '--deck')
parser.add_argument('-t', '--text')
parser.add_argument('-v', '--voice')
args = parser.parse_args()


def add_note(deck_name, model,  fields):
    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck_name,
                "modelName": model,
                "fields": fields,
                "tags": []
            }
        }
    }

    response = requests.post('http://localhost:8765', json=payload)
    if response.status_code == 200:
        resultado = response.json()
        if resultado['error'] is None:
            print("Carta adicionada com sucesso!")
        else:
            print(f"Erro ao adicionar a carta: {resultado['error']}")
    else:
        print(f"Falha na requisição: {response.status_code}")


def add_midia(path):
    audio = base64.b64encode(path.read_bytes()).decode('utf-8')
    payload = {
        "action": "storeMediaFile",
        "version": 6,
        "params": {
            "filename": path.name,
            "data": audio
        }
    }

    response = requests.post('http://localhost:8765', json=payload)
    if response.status_code == 200:
        resultado = response.json()
        if resultado['error'] is None:
            print(f"Arquivo de áudio '{path.name}' subido com sucesso!")
            return path.name
        else:
            print(f"Erro ao subir o arquivo de áudio: {resultado['error']}")
    else:
        print(f"Falha na requisição: {response.status_code}")


if __name__ == '__main__':
    answer = args.text
    translation = translate(args.text)
    audio_path = text_to_speech(answer)
    add_midia(audio_path)
    add_note(args.deck,
             "Modelo de Áudio resporsta",
             {'Answer': answer, 'Translation': translation,
              'Audio': f"[sound:{audio_path.name}]"})
