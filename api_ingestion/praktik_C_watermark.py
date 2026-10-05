import json
from pathlib import Path

DEFAULT_WATERMARK = "1970-01-01T00:00:00+00:00"

def load_watermark(file_path="state/watermark.json"):
    path = Path(file_path)
    
    # Syarat: Jika file belum ada, gunakan default
    if not path.exists():
        return DEFAULT_WATERMARK

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
        
    return data.get("watermark", DEFAULT_WATERMARK)

def save_watermark(watermark, file_path="state/watermark.json"):
    path = Path(file_path)
    
    # Syarat: Folder dibuat otomatis
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        # Syarat: Format JSON yang spesifik
        json.dump({"watermark": watermark}, file, indent=2)