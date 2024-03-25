from domain.repositories.storage_repository import StorageRepository

class DeleteFile:
    def __init__(self, storage_repository: StorageRepository):
        self.storage_repository = storage_repository

    def execute(self, file_name: str) -> None:
        self.storage_repository.delete_file(file_name)