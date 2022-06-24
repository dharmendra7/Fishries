import os
from django.utils import timezone


def media_upload_to(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    milliseconds = now.microsecond // 1000
    return f"{instance.MEDIA_UPLOAD_PREFIX}/{instance.pk}/{now:%Y%m%d%H%M%S}{milliseconds}{extension}"

