import os
from django.core.exceptions import ValidationError


def validate_file_extension(file):
    ext = os.path.splitext(file.name)[1]
    valid_extensions = ['.doc', '.docx', '.txt']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')