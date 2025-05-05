import os
import asyncio
from tqdm import tqdm
import PyPDF2
from bs4 import BeautifulSoup
import edge_tts
import re

# ========== CONFIGURATION ==========
INPUT_FILE = "the_flat_share.txt"
OUTPUT_DIR = "the_flat_share"
OUTPUT_AUDIO_DIR = "the_flat_share_audio"
CHAPTER_PATTERN = r"^\s*(?:chapter\s+)?(\d{1,3})\s*$"
SECTION_KEYWORDS = ["Tiffy", "Leon"]

# ========== FUNCTIONS ==========


def read_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def read_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    return soup.get_text(separator='\n', strip=True)


def read_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text


def split_into_chapters(text):
    lines = text.splitlines()
    chapters = []
    current_chapter = []
    current_chapter_number = None

    for line in lines:
        match = re.match(CHAPTER_PATTERN, line.strip(), re.IGNORECASE)
        if match:
            chapter_title = match.group(0).strip()
            if current_chapter:
                chapters.append((current_chapter_number, current_chapter))
                current_chapter = []
            current_chapter_number = chapter_title
        elif current_chapter_number:
            current_chapter.append(line)

    if current_chapter:
        chapters.append((current_chapter_number, current_chapter))

    return chapters

# ========== MAIN (testing chapter parsing only) ==========


def main():
    ext = os.path.splitext(INPUT_FILE)[1].lower()

    if ext == ".txt":
        text = read_txt(INPUT_FILE)
    elif ext == ".html":
        text = read_html(INPUT_FILE)
    elif ext == ".pdf":
        text = read_pdf(INPUT_FILE)
    else:
        print("❌ Unsupported file type.")
        return

    chapters = split_into_chapters(text)
    import shutil
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    for idx, (chapter_title, chapter_lines) in enumerate(chapters):
        chapter_num = str(idx + 1).zfill(3)

        detected_speaker = ""
        for line in chapter_lines[:5]:  # Look deeper into the first 5 lines
            if line.strip() == "Tiffy":
                detected_speaker = "_Tiffy"
                break
            elif line.strip() == "Leon":
                detected_speaker = "_Leon"
                break
        output_txt_path = os.path.join(OUTPUT_DIR, f"chapter_{chapter_num}{detected_speaker}.txt")
        with open(output_txt_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(chapter_lines))
        # print(f"✅ Saved {output_txt_path}")

    print(f"\n📚 Total chapters found: {len(chapters)}")

    VOICE_SETTINGS = {
        "Tiffy": {"voice": "en-GB-SoniaNeural", "speed": "+40%"},
        "Leon": {"voice": "en-GB-RyanNeural", "speed": "+40%"},
        "default": {"voice": "en-GB-SoniaNeural", "speed": "+50%"},
    }

    async def convert_to_mp3():
        converted = 0
        skipped = 0

        if not os.path.exists(OUTPUT_AUDIO_DIR):
            os.makedirs(OUTPUT_AUDIO_DIR)

        text_files = sorted(f for f in os.listdir(OUTPUT_DIR) if f.endswith(".txt"))

        # Optional: convert only specific chapters
        TARGET_CHAPTERS = ['011', '012', '013', '014', '015']  # Example: ['009', '010'] — leave empty to convert all

        if TARGET_CHAPTERS:
            text_files = [f for f in text_files if any(f"chapter_{chap}" in f for chap in TARGET_CHAPTERS)]

        for txt_file in tqdm(text_files, desc="Converting to MP3", unit="file"):
            base_name = os.path.splitext(txt_file)[0]
            output_path = os.path.join(OUTPUT_AUDIO_DIR, f"{base_name}.mp3")

            if os.path.exists(output_path):
                skipped += 1
                tqdm.write(f"⏭️ Skipping already converted file: {output_path}")
                continue

            if "_Tiffy" in base_name:
                speaker = "Tiffy"
            elif "_Leon" in base_name:
                speaker = "Leon"
            else:
                speaker = "default"

            voice_cfg = VOICE_SETTINGS[speaker]
            voice = voice_cfg["voice"]
            speed = voice_cfg["speed"]

            input_path = os.path.join(OUTPUT_DIR, txt_file)

            with open(input_path, 'r', encoding='utf-8') as f:
                text = f.read().strip()
                if not text:
                    print(f"⚠️ Skipped empty file: {txt_file}")
                    continue

            communicate = edge_tts.Communicate(text=text, voice=voice, rate=speed)
            await communicate.save(output_path)
            converted += 1
            tqdm.write(f"🎧 Saved: {output_path}")

        tqdm.write(f"✅ Conversion complete. {converted} file(s) converted, {skipped} skipped.")

    asyncio.run(convert_to_mp3())

if __name__ == "__main__":
    main()
