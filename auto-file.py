from os import scandir, rename, makedirs
from os.path import splitext, exists , join
from shutil import move
from time import sleep 

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#folders to be used 
#Choose the folder dir path you want to.
source_dir=''
dest_dir_music = ""
dest_dir_video = ""
dest_dir_image = ""
dest_dir_documents = ""
dest_dir_compressed= ""


# ? supported image types
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
# ? supported Video types
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
# ? supported Audio types
audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]
# ? supported Document types
document_extensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]
# ? supported Document types
compressed_extensions=[".ZIP", ".RAR", ".ARJ", ".TAR",".GZ", ".TGZ", ".7z"]



def make_unqiue(dest, name):
    filename, extension= splitext(name)
    counter=1 
    
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter +=1
        
    return name 

def move_file(dest, entry, name):
    if not exists(dest):
        makedirs(dest)
        logging.info(f"Created directory: {dest}")
        
        
    if exists(f"{dest}/{name}"):
        unique_name=make_unqiue(dest,name)
        oldName=join(dest, name)
        newName=join(dest, unique_name)
        rename(oldName,newName)
    move(entry, dest)
    
    

class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for entry in entries:
                name= entry.name
                self.check_audio_files(entry, name)
                self.check_compressed_files(entry, name)
                self.check_document_files(entry, name)
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                
                
                
            
    def check_audio_files(self,entry, name):
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                move_file(dest_dir_music,entry, name)
                logging.info(f"Moved audio file:{name}")
                
                
    def check_compressed_files(self, entry, name):
        for compressed_extension in compressed_extensions:
            if name.endswith(compressed_extension) or name.endswith(compressed_extension.upper()):
                move_file(dest_dir_compressed, entry, name)
                logging.info(f"Moved compressed file:{name}")
    
    def check_document_files(self, entry,name):
        for document_extension in document_extensions:
            if name.endswith(document_extension) or name.endswith(document_extension.upper()):
                move_file(dest_dir_documents, entry, name)
                logging.info(f"Moved document file:{name}")
                
                
    def check_video_files(self, entry, name):
        for video_extension in video_extensions:
            if name.endswith(video_extension)or name.endswith(video_extension.upper()):
                move_file(dest_dir_video, entry, name)
                logging.info(f"Moved video file:{name}")
                
    def check_image_files(self, entry, name):
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_file(dest_dir_image,entry, name)
                logging.info(f"Moved image file:{name}")
                
                
                
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s-%(message)s",
                        datefmt='%Y-%m-%d')
    path= source_dir
    event_handler = MoverHandler()
    observer=Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()