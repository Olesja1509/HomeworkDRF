from rest_framework import serializers


class VideoUrlValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        youtube_url = 'youtube.com'
        tap_val = dict(value).get(self.field)
        if youtube_url not in tap_val:
            raise serializers.ValidationError("Нельзя использовать ссылки на сторонние ресурсы, кроме 'youtube.com")
