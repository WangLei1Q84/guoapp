import argparse
import json
from pathlib import Path
import shutil

from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description='从应用图标源文件生成各平台资源；需要 Pillow。')
parser.add_argument('--output', type=Path, default=root)
parser.add_argument('--font', type=Path, default=Path('/System/Library/Fonts/PingFang.ttc'))
options = parser.parse_args()
output = options.output
source = root / 'assets/app_icon.png'
icon = Image.open(source).convert('RGB')

def save(image, name):
    destination = output / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination)

contents = json.loads((root / 'ios/Runner/Assets.xcassets/AppIcon.appiconset/Contents.json').read_text())
for entry in contents['images']:
    if 'filename' in entry:
        size = round(float(entry['size'].split('x')[0]) * float(entry['scale'].rstrip('x')))
        save(icon.resize((size, size), Image.Resampling.LANCZOS),
             'ios/Runner/Assets.xcassets/AppIcon.appiconset/' + entry['filename'])
for directory, size in {
    'mipmap-mdpi': 48,
    'mipmap-hdpi': 72,
    'mipmap-xhdpi': 96,
    'mipmap-xxhdpi': 144,
    'mipmap-xxxhdpi': 192,
}.items():
    save(icon.resize((size, size), Image.Resampling.LANCZOS),
         f'android/app/src/main/res/{directory}/ic_launcher.png')
shutil.copy2(source, output / 'android/app/src/main/res/drawable/app_icon_image.png')
save(icon.resize((256, 256), Image.Resampling.LANCZOS), 'windows/runner/resources/app_icon.ico')
for name, resource in [('เกิดใหม่', 'tv_banner'), ('เกิดใหม่', 'tv_banner_all_sources')]:
    banner = Image.new('RGB', (640, 360), '#101114')
    banner.paste(icon.resize((180, 180), Image.Resampling.LANCZOS), (44, 90))
    draw = ImageDraw.Draw(banner)
    font = ImageFont.truetype(str(options.font), 76)
    draw.text((255, 128), name, font=font, fill='white')
    save(banner, f'android/app/src/main/res/drawable-xhdpi/{resource}.png')
