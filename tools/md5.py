import hashlib
from fastapi import UploadFile


async def get_file_md5(file: UploadFile):
    hash_md5 = hashlib.md5()
    for chunk in iter(lambda: file.file.read(4096), b""):
        hash_md5.update(chunk)
    return hash_md5.hexdigest()
