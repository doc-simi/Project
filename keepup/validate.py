from django.core.exceptions import ValidationError
from django.core.files import uploadedfile
from django.db.utils import Error




# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_UPLOAD_SIZE = 2621440


CONTENT_TYPES = ['jpg', 'jpeg', 'png']


def validate_image_size(image):
    if image:
        file_size = image.size
        file_name = image.name
        content_type = file_name.split('.')[1]
        if file_size > MAX_UPLOAD_SIZE:
            raise ValidationError("Max size of file is  2.5MB")

        if not content_type in CONTENT_TYPES:
            raise ValidationError("This file is not supported. Only upload jpg, jpeg or png")
        
    return image
