from domain.models.file import File
from domain.repositories.storage_repository import StorageRepository

class DownloadFile:
    def __init__(self, storage_repository: StorageRepository):
        self.storage_repository = storage_repository

    def execute(self, file_name: str, file_path: str) -> File:
        return self.storage_repository.download_file(file_name, file_path)
