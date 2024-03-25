from domain.models.file import File
from domain.repositories.storage_repository import StorageRepository

class ListFile:
    def __init__(self, storage_repository: StorageRepository):
        self.storage_repository = storage_repository

    def execute(self) -> None:
        self.storage_repository.list_files()