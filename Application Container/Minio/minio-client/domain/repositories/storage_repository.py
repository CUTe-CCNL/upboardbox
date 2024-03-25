from abc import ABC, abstractmethod
from domain.models.file import File

class StorageRepository(ABC):
    @abstractmethod
    def upload_file(self, destination_file: File, source_file: File) -> None:
        pass

    @abstractmethod
    def download_file(self, file_name: str, file_path: str) -> File:
        pass

    @abstractmethod
    def list_files(self) -> list[str]:
        pass

    @abstractmethod
    def delete_file(self, file_name: str) -> None:
        pass