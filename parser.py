from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from database import SessionLocal
from websocket_manager import websocket_manager
import csv
import time
import json
import asyncio
import models
import os


def process_csv_file(file_path: str, loop):
    db = SessionLocal()
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                try:
                    ts = datetime.fromisoformat(row['timestamp'])
                    price_val = float(row['price'])
                    
                    # Dublicate check
                    exists = db.query(models.DBBTCPrice).filter(models.DBBTCPrice.timestamp == ts).first()
                    if not exists:
                        new_record = models.DBBTCPrice(timestamp=ts, price=price_val)
                        db.add(new_record)

                except Exception as e:
                    print(f"Error in a row {row}: {e}")           
            
            db.commit()
            print(f"File {file_path} added to DB")
    except Exception as e:
        print(f"Cannot read a file {file_path}: {e}")
    finally:
        db.close()


class CSVHandler(FileSystemEventHandler):
    def __init__(self, loop):
        self.loop = loop

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.csv'):
            time.sleep(0.5)
            
            filename = os.path.basename(event.src_path)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            label = f"📅 {now})"

            print(f"New file: {filename}")
            
            msg = json.dumps({
                "type": "new_file", 
                "filename": filename,
                "label": label
            })
            
            asyncio.run_coroutine_threadsafe(websocket_manager.broadcast(msg), self.loop)
            process_csv_file(event.src_path, self.loop)


def start_watcher(path_to_watch: str = "./data_lake", loop=None):
    event_handler = CSVHandler(loop)
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=False)
    observer.start()
    print(f"Watcher started")
    return observer
