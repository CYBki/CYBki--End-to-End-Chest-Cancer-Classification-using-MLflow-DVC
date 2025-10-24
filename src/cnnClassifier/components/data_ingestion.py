import os
from pathlib import Path
import zipfile

import gdown

from cnnClassifier import logger
from cnnClassifier.entity.config_entity import DataIngestionConfig
from cnnClassifier.utils.common import get_size, create_directories


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self) -> None:
        """Download the dataset zip from the configured source if needed."""
        local_data_file = Path(self.config.local_data_file)

        if local_data_file.exists():
            file_size = get_size(local_data_file)
            logger.info(f"Skipping download; file already present at {local_data_file} ({file_size}).")
            return

        create_directories([local_data_file.parent], verbose=False)
        logger.info(f"Downloading data from {self.config.source_URL} to {local_data_file}.")

        gdown.download(
            url=self.config.source_URL,
            output=str(local_data_file),
            quiet=False,
            fuzzy=True,
        )

        file_size = get_size(local_data_file)
        logger.info(f"Download completed; file stored at {local_data_file} ({file_size}).")

    def extract_zip_file(self) -> None:
        """Extract the downloaded zip archive into the configured directory."""
        local_data_file = Path(self.config.local_data_file)
        unzip_dir = Path(self.config.unzip_dir)

        if not local_data_file.exists():
            raise FileNotFoundError(f"Cannot extract; archive not found at {local_data_file}.")

        create_directories([unzip_dir], verbose=False)

        extracted_contents = [item for item in unzip_dir.iterdir() if item.name != local_data_file.name]
        if extracted_contents:
            logger.info(f"Extraction skipped; target directory {unzip_dir} already has extracted data.")
            return

        logger.info(f"Extracting {local_data_file} to {unzip_dir}.")
        with zipfile.ZipFile(local_data_file, "r") as zip_ref:
            zip_ref.extractall(unzip_dir)

        logger.info(f"Extraction completed; contents available in {unzip_dir}.")
