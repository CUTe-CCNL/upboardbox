from domain.models.file import File
from domain.repositories.storage_repository import StorageRepository

class UploadFile:
    def __init__(self, storage_repository: StorageRepository):
        self.storage_repository = storage_repository

    def execute(self, destination_file: File, source_file: File) -> None:
        self.storage_repository.upload_file(destination_file, source_file)
