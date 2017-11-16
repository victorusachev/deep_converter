from io import BytesIO
from pathlib import Path

import magic


def get_mime_type(obj):
    mime = magic.Magic(mime=True)
    if isinstance(obj, (str, Path)):
        return mime.from_file(str(obj))
    elif isinstance(obj, bytes):
        return mime.from_buffer(obj)
    elif isinstance(obj, BytesIO):
        return mime.from_buffer(obj.getvalue())
    else:
        raise TypeError
