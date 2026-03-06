import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

home = os.path.expanduser("~")
download_dir = os.path.join(home,"Downloads")
target_base = os.path.join(home, "Desktop", "다운로드 정리")

file_rules = {
    "documents": (".pdf", ".docx", ".hwp", ".txt"),
    "images": (".jpg", ".jpeg", ".png", ".gif"),
    "videos": (".mp4", ".mkv", ".avi"),
    "archives": (".zip", ".rar", ".7z"),
    "modeling": (".stl",),
    "exefiles": (".exe",)
}

temp_exts = (".crdownload", ".part", ".tmp")
processed_files = set()

def wait_download_complete(path, interval=1, stable=3):
    last_size = -1
    same_count = 0

    while True:
        if not os.path.exists(path):
            return False
        
        size = os.path.getsize(path)

        if size == last_size:
            same_count += 1
        else:
            same_count = 0

        if same_count >= stable:
            return True
        
        last_size = size
        time.sleep(interval)

def organize_file(filepath):
    if not os.path.exists(filepath):
        return
    if filepath in processed_files:
        return

    processed_files.add(filepath)

    filename = os.path.basename(filepath)
    ext = os.path.splitext(filename)[1].lower()     #어떤자료.pdf   ("어떤자료", ".pdf")

    for folder, exts in file_rules.items(): #딕셔너리의 모든 쌍을 꺼내는 함수
        if ext in exts:
            target_dir = os.path.join(target_base, folder)
            break
    else:
        target_dir = os.path.join(target_base, "Others")

    os.makedirs(target_dir, exist_ok=True) 
    target_path = os.path.join(target_dir, filename)

    try:
        shutil.move(filepath, target_path)
        print(f"이동 완료: {filename}")
    except Exception as e:
        print(f"이동 실패: {filename} / {e}")


class DownloadHandler(FileSystemEventHandler):

    def handle(self, path):
        if path.endswith(temp_exts):
            return
        if path in processed_files:   
            return

        print("다운로드 감지:", os.path.basename(path))

        if wait_download_complete(path):
            organize_file(path)

    def on_moved(self, event):  
        
        if not event.is_directory: 
            self.handle(event.dest_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.handle(event.src_path) 


if __name__ == "__main__":
    print("다운로드 자동 정리기 실행 중...")

    handler = DownloadHandler()
    observer = Observer()
    observer.schedule(handler, download_dir, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()