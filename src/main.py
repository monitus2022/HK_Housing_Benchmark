from cloud_storage import StorageManager

def main():
    storage_manager = StorageManager()
    storage_manager.download_all_from_datahub()

if __name__ == "__main__":
    main()