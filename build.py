import json
import os
import time
import uuid

PREFABS_DIR = "prefabs"
OUTPUT_FILE = "dist/library.json"

def normalize_element(el):
    """Ensure all required Excalidraw fields exist."""
    defaults = {
        "id": str(uuid.uuid4()),
        "type": "rectangle",
        "x": 0,
        "y": 0,
        "width": 100,
        "height": 40,
        "angle": 0,
        "strokeColor": "#000000",
        "backgroundColor": "transparent",
        "fillStyle": "hachure",
        "strokeWidth": 1,
        "strokeStyle": "solid",
        "roughness": 1,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": None,
        "seed": 12345,
        "version": 1,
        "versionNonce": 123456,
        "isDeleted": False,
        "boundElements": [],
        "updated": int(time.time() * 1000),
        "link": None,
        "locked": False
    }
    for k, v in defaults.items():
        if k not in el:
            el[k] = v
    if "id" not in el or not el["id"]:
        el["id"] = str(uuid.uuid4())
    return el

def load_prefabs():
    """Load all .excalidraw files in prefabs directory."""
    items = []
    for root, _, files in os.walk(PREFABS_DIR):
        for file in files:
            if file.endswith(".excalidraw") or file.endswith(".excalidraw.json"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r") as f:
                        data = json.load(f)
                except json.JSONDecodeError:
                    print(f"❌ Skipping {file}: invalid JSON")
                    continue

                # Handle array-only or full Excalidraw objects
                elements = []
                if isinstance(data, list):
                    elements = data
                elif isinstance(data, dict):
                    elements = data.get("elements", [])
                else:
                    print(f"❌ Skipping {file}: unrecognized format")
                    continue

                # Normalize elements
                elements = [normalize_element(el) for el in elements]

                # Wrap as a library item
                library_item = {
                    "id": str(uuid.uuid4()),
                    "status": "published",
                    "name": os.path.splitext(file)[0],
                    "category": os.path.basename(root),
                    "created": int(time.time() * 1000),
                    "elements": elements,
                    "appState": {
                        "gridSize": 20,
                        "viewBackgroundColor": "#ffffff"
                    },
                    "files": {}
                }

                items.append(library_item)
                print(f"✅ Included {file} ({len(elements)} elements)")

    return items

def build_library(items):
    """Build the combined Excalidraw library JSON."""
    return {
        "type": "excalidrawlib",
        "version": 2,
        "source": "https://excalidraw.com",
        "libraryItems": items
    }

def main():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    items = load_prefabs()
    library = build_library(items)

    with open(OUTPUT_FILE, "w") as out:
        json.dump(library, out, indent=2)

    print(f"\n🎉 Built library with {len(items)} items → {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
