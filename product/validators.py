from django.core.exceptions import ValidationError

def validate_size(file):
    
    max_size = 50
    max_size_in_byte = max_size * 1024
    
    if file.size > max_size_in_byte:
        raise ValidationError(f"file size cannot be more than {max_size} kb")