from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas

from deep_converter.utils.images import get_mime_type

SUPPORTED_ARCHIVE_TYPES = ('application/zip',)
SUPPORTED_IMAGE_TYPES = ('image/gif', 'image/jpeg', 'image/png')


class FileWrapper(object):
    def __init__(self, path, data=None):
        self._data = data
        self._path = Path(path)
        self._mime_type = None

    @property
    def data(self):
        if not self._data:
            with open(self._path, 'rb') as fp:
                self._data = fp.read()
        return self._data

    @property
    def path(self):
        return self._path

    @property
    def mime_type(self):
        if not self._mime_type:
            self._mime_type = get_mime_type(self.data)
        return self._mime_type

    def __str__(self):
        return str(self.path)

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self}>'


def files_from_archive(file):
    with BytesIO(file.data) as in_memory:
        with ZipFile(in_memory) as archive:
            for info in archive.infolist():
                if info.is_dir():
                    continue
                with archive.open(info) as fp:
                    filename = Path(info.filename)
                    if file.path:
                        filename = file.path / info.filename
                    inner_file = FileWrapper(filename, fp.read())
                    yield inner_file


def convert_image(file):
    new_filename = file.path.with_suffix('.pdf')
    canvas = Canvas(str(new_filename))
    canvas.setTitle(new_filename.stem)
    with BytesIO(file.data) as in_memory:
        reader = ImageReader(in_memory)
        size = reader.getSize()
        canvas.setPageSize(size)
        canvas.drawImage(reader, 0, 0, *size, mask='auto')
        canvas.showPage()
    new_file = FileWrapper(path=new_filename, data=canvas.getpdfdata())
    yield new_file


def convert_archive(file):
    for inner in files_from_archive(file):
        yield tuple(convert(inner))


def convert(file):
    if file.mime_type in SUPPORTED_ARCHIVE_TYPES:
        yield from convert_archive(file)
    elif file.mime_type in SUPPORTED_IMAGE_TYPES:
        yield from convert_image(file)
    else:
        yield file


def flatten(iterable):
    rv = []
    if isinstance(iterable, (list, tuple, set)):
        for el in iterable:
            rv.extend(flatten(el))
    else:
        rv.append(iterable)
    return rv
