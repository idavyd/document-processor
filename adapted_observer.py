import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import subprocess

main_script_path = r'C:\Users\IDavydenko\PycharmProjects\newproject\Testing\main_copy.py'


class CustomEventHandler(LoggingEventHandler):
    def __init__(self):
        super().__init__()
        self.last_triggered = 0

    def process_event(self, event):
        current_time = time.time()
        # Only process if more than 1 second has passed since the last event
        if current_time - self.last_triggered > 1:
            logging.info(f"File {event.event_type}: {event.src_path}")
            subprocess.run([sys.executable, main_script_path])
            self.last_triggered = current_time

    def on_created(self, event):
        super().on_created(event)
        if not event.is_directory:
            self.process_event(event)

    def on_modified(self, event):
        super().on_modified(event)
        if not event.is_directory:
            self.process_event(event)


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
