from pathlib import Path
import base64

root = Path(__file__).resolve().parent / 'docs' / 'screenshots'
root.mkdir(parents=True, exist_ok=True)

png_base64 = (
    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAFc5SdAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJ0UkGAAAAAAgIY8WgAAAAASUVORK5CYII='
)

for name in ['dashboard.png', 'analysis.png', 'admin.png']:
    (root / name).write_bytes(base64.b64decode(png_base64))

print('Created screenshot placeholders:')
for path in sorted(root.iterdir()):
    print(path.name)
