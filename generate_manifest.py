import os
import json
import urllib.parse

ROOT_DIR = "free_playlists"
OUTPUT_FILE = "playlists.json"

def scan_playlists():
    if not os.path.exists(ROOT_DIR):
        print(f"Error: Folder '{ROOT_DIR}' not found.")
        return

    data = []
    # ลิสต์โฟลเดอร์และจัดเรียงชื่อ
    folders = sorted([f for f in os.listdir(ROOT_DIR) if os.path.isdir(os.path.join(ROOT_DIR, f))])

    for folder in folders:
        folder_path = os.path.join(ROOT_DIR, folder)
        # กรองเอาเฉพาะไฟล์เพลง (mp3, m4a, wav, flac)
        files = sorted([
            f for f in os.listdir(folder_path) 
            if f.lower().endswith(('.mp3', '.m4a', '.wav', '.flac')) and not f.startswith('.')
        ])
        
        # จัดรูปแบบชื่อแสดงผล (เช่น 01_Kids_Lullaby_Bedtime -> 01 Kids Lullaby Bedtime)
        display_name = folder.replace('_', ' ')

        data.append({
            "id": folder,
            "title": display_name,
            "folder": folder,
            "count": len(files),
            "files": [
                {
                    "name": file_name,
                    # Relative path ที่ encode ช่องว่างและเครื่องหมายพิเศษเรียบร้อยแล้ว
                    "relativePath": f"{ROOT_DIR}/{urllib.parse.quote(folder)}/{urllib.parse.quote(file_name)}"
                }
                for file_name in files
            ]
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Generated {OUTPUT_FILE} successfully with {len(data)} playlists.")

if __name__ == "__main__":
    scan_playlists()