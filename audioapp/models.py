from django.db import models

class Recording(models.Model):
    title = models.CharField(max_length=255, blank=True)  
    audio_file = models.FileField(upload_to='recordings/')  
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.title or f"Recording - {self.created_at}"

class Transcription(models.Model):
    recording = models.ForeignKey(Recording, on_delete=models.CASCADE)
    transcription_text = models.TextField()

    def __str__(self):
        return f"Transcription for {self.recording.title}"
