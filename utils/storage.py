import unicodedata

from django.core.files.storage import FileSystemStorage
from django.utils.http import urlquote 

class ASCIIFileSystemStorage(FileSystemStorage):
    """
    Convert unicode characters in name to ASCII characters.
    """
    def get_valid_name(self, name):
        name = urlquote(name)
        return super(ASCIIFileSystemStorage, self).get_valid_name(name)
