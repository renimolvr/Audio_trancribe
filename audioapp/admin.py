from django.contrib import admin
from .models import Recording, Transcription

@admin.register(Recording)
class RecordingAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'audio_file')
    search_fields = ('created_at',)
    list_filter = ('created_at',)

@admin.register(Transcription)
class TranscriptionAdmin(admin.ModelAdmin):
    list_display = ('recording', 'transcription_text')
    