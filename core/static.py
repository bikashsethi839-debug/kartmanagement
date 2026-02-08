"""Static file utilities."""
import mimetypes


def get_mime_type(path: str) -> str:
    mtype, _ = mimetypes.guess_type(path)
    return mtype or 'application/octet-stream'
