#!/usr/bin/env python3
import os
from pathlib import Path
import re

ROOT = Path(".")
IMAGE_DIR = ROOT / "images"

def fix_image_case():
    """Opraví img src tagy na správnou velikost písmen podle skutečných souborů."""
    if not IMAGE_DIR.exists():
        print("🖼️  Složka 'images' neexistuje.")
        return

    # Vytvoř mapování: lowercase název → správný název
    real_files = {f.name.lower(): f.name for f in IMAGE_DIR.iterdir() if f.is_file()}

    fixed = 0
    for html_file in ROOT.rglob("*.html"):
        content = html_file.read_text(encoding="utf-8")
        new_content = content

        # Najdi všechny img src
        pattern = r'<img\s+[^>]*src\s*=\s*["\']([^"\']+)["\'][^>]*>'
        matches = re.findall(pattern, content, re.IGNORECASE)

        for src in matches:
            if src.startswith("images/") and not src.startswith("http"):
                filename = src.split("/")[-1]
                lower_filename = filename.lower()
                if lower_filename in real_files and filename != real_files[lower_filename]:
                    correct_path = src.replace(filename, real_files[lower_filename])
                    new_content = new_content.replace(src, correct_path)
                    print(f"🖼️  Opraven obrázek: {src} → {correct_path}")
                    fixed += 1

        if new_content != content:
            html_file.write_text(new_content, encoding="utf-8")

    print(f"✅ Opraveno {fixed} obrázků.")

def add_favicon_and_meta():
    """Přidá favicon a základní meta tagy, pokud chybí."""
    html_file = ROOT / "index.html"
    if not html_file.exists():
        print("📄 index.html neexistuje.")
        return

    content = html_file.read_text(encoding="utf-8")

    # Favicon
    if '<link rel="icon"' not in content:
        insert_after = '<head>'
        favicon_tag = '    <link rel="icon" type="image/png" href="images/favicon.png">\n'
        if (IMAGE_DIR / "favicon.png").exists():
            content = content.replace(insert_after, insert_after + "\n" + favicon_tag)
            print("✅ Přidán favicon tag.")

    # Meta description
    if '<meta name="description"' not in content:
        meta_desc = '    <meta name="description" content="Gem District - Exclusive NFT Art Gallery">\n'
        content = content.replace("<head>", "<head>\n" + meta_desc)
        print("✅ Přidán meta description tag.")

    # Open Graph
    if '<meta property="og:title"' not in content:
        og_tags = '''    <meta property="og:title" content="Gem District">
    <meta property="og:description" content="Exclusive NFT Art Gallery">
    <meta property="og:image" content="images/og-image.jpg">
    <meta property="og:url" content="https://gemdistrict.art">
'''
        content = content.replace("<head>", "<head>\n" + og_tags)
        print("✅ Přidány Open Graph tagy.")

    html_file.write_text(content, encoding="utf-8")

if __name__ == "__main__":
    print("🤖 Spouštím Fix-It Bota pro gemdistrict.art...\n")
    fix_image_case()
    add_favicon_and_meta()
    print("\n🎉 Bot dokončil opravy. Nezapomeň commitnout změny!")
