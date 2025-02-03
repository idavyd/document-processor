import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import subprocess


main_script_path = r'C:\Users\IDavydenko\PycharmProjects\newproject\Testing\main_copy.py'


class CustomEventHandler(LoggingEventHandler):
    def on_created(self, event):
        super().on_created(event)
        if not event.is_directory:
            logging.info(f"File created: {event.src_path}")
            subprocess.run([sys.executable, main_script_path])

    def on_modified(self, event):
        super().on_modified(event)
        if not event.is_directory:
            logging.info(f"File modified: {event.src_path}")
            subprocess.run([sys.executable, main_script_path])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = r'C:\Users\IDavydenko\Downloads\Python'
    event_handler = CustomEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
