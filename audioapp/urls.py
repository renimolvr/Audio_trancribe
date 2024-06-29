from django.urls import path
from .views import record, play_recording, transcribe_recording

urlpatterns = [
    path('', record, name='record'),  # URL for recording page
    path('play/<int:recording_id>/', play_recording, name='play_recording'), 
    path('transcribe/<int:recording_id>/', transcribe_recording, name='transcribe_recording'),
    path('save-transcription/<int:recording_id>/', transcribe_recording, name='save_transcription'),
]
