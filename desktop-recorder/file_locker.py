import fcntl

class FileLocker:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.lock_file = None

    def lock(self):
        self.lock_file = open(self.file_path, 'w')
        fcntl.flock(self.lock_file, fcntl.LOCK_EX)

    def unlock(self):
        fcntl.flock(self.lock_file, fcntl.LOCK_UN)

    def __enter__(self):
        self.lock()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unlock()
        self.lock_file.close()
        self.lock_file = None