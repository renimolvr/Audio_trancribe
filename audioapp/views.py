import requests
import time
import sounddevice as sd

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Recording, Transcription 
from .forms import RecordingForm
from scipy.io.wavfile import write
from django.core.files.base import ContentFile
from django.http import JsonResponse


API_URL = "https://api-inference.huggingface.co/models/thennal/whisper-medium-ml"
headers = {"Authorization": "Bearer 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"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    
    # Retry logic
    max_retries = 5
    retry_delay = 5  # seconds
    retries = 0
    
    while retries < max_retries:
        response = requests.post(API_URL, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            retries += 1
            print(f"Retrying... Attempt {retries} out of {max_retries}")
            time.sleep(retry_delay)
    
    return {'error': 'Failed to transcribe audio'}

def record(request):
    if request.method == 'POST':
        audio_data = request.FILES.get('audio')
        if audio_data:
            recording = Recording()
            recording.audio_file.save('recording.wav', audio_data)
            recording.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'No audio data received'}, status=400)
    else:
        form = RecordingForm()

    recordings = Recording.objects.all().order_by('-created_at')
    return render(request, 'record.html', {'form': form, 'recordings': recordings})

def play_recording(request, recording_id):
    try:
        recording = Recording.objects.get(pk=recording_id)
        audio_url = recording.audio_file.url
        return render(request, 'play_recording.html', {'audio_url': audio_url, 'recording': recording})
    except Recording.DoesNotExist:
        messages.error(request, 'Recording not found.')
        return redirect('record')

def transcribe_recording(request, recording_id):
    try:
        recording = Recording.objects.get(pk=recording_id)
        audio_file_path = recording.audio_file.path
        response = query(audio_file_path)
        initial_transcription = response.get('text', 'Transcription failed.')
        
        if request.method == 'POST':
            transcription_text = request.POST.get('transcription', '')
            if transcription_text.strip():
                # Save transcription to another database with foreign key
                new_transcription = Transcription.objects.create(
                    recording=recording,
                    transcription_text=transcription_text
                )
                new_transcription.save()
                messages.success(request, 'Transcription saved successfully.')
                return redirect('record')

        return render(request, 'transcription.html', {
            'transcription': initial_transcription,
            'recording': recording
        })

    except Recording.DoesNotExist:
        messages.error(request, 'Recording not found.')
        return redirect('record')

