import os
from dotenv import load_dotenv
import requests


def get_url(token, file_obj):
    '''
    Uploads a file to AssemblyAI and returns the temporary URL to the uploaded file.

    Parameters:
    token (str): The API key.
    file_obj (file): The file object to upload.

    Returns:
    str: The URL to the uploaded file.
    '''
    headers = {'authorization': token}
    response = requests.post(
        'https://api.assemblyai.com/v2/upload',
        headers=headers,
        data=file_obj
    )
    url = response.json()["upload_url"]
    print("Uploaded file and got temporary URL to file")
    return url


def get_transcribe_id(token, url):
    '''
    Sends a request to AssemblyAI to transcribe the file at the given URL and returns the ID of the transcription job.

    Parameters:
    token (str): The API key.
    url (str): The URL to the uploaded file.

    Returns:
    str: The ID of the transcription job.
    '''
    endpoint = "https://api.assemblyai.com/v2/transcript"
    json = {
        "audio_url": url
    }
    headers = {
        "authorization": token,
        "content-type": "application/json"
    }
    response = requests.post(endpoint, json=json, headers=headers)
    transcribe_id = response.json()['id']
    print("Made request and file is currently queued")
    return transcribe_id


def upload_file(file_obj):
    '''
    Uploads a file to AssemblyAI for transcription and returns the API key and transcription job ID.

    Parameters:
    file_obj (file): The file object to transcribe.

    Returns:
    tuple: A tuple containing the API key and transcription job ID.
    '''
    load_dotenv()
    token = os.getenv("API_TOKEN")
    file_url = get_url(token, file_obj)
    transcribe_id = get_transcribe_id(token, file_url)
    return token, transcribe_id


def get_text(token, transcribe_id):
    '''
    Retrieves the transcription result for the given transcription job ID.

    Parameters:
    token (str): The API key.
    transcribe_id (str): The ID of the transcription job.

    Returns:
    dict: The transcription result.
    '''
    endpoint = f"https://api.assemblyai.com/v2/transcript/{transcribe_id}"
    headers = {
        "authorization": token
    }
    result = requests.get(endpoint, headers=headers).json()
    return result

def calculate_words_per_minute(transcript, duration_in_seconds):
    '''
    Calculate the speaker's rate of speaking in words per minute (wpm).

    Args:
        transcript (str): The transcript of the speech.
        duration_in_seconds (float): The duration of the speech in seconds.

    Returns:
        wpm (float): The speaker's rate of speaking in wpm.
    '''
    # Count number of words in transcript
    num_words = len(transcript.split())

    # Calculate speaker's rate of speaking in wpm
    wpm = num_words / (duration_in_seconds / 60)

    return wpm