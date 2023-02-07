from django.core.files.storage import FileSystemStorage
class CustomFileStorage(FileSystemStorage):
    def get_valid_name(self, name):
        import time
        timestamp = str(int(time.time()))
        name = timestamp + '_' + name
        return name

custom_file_storage = CustomFileStorage()