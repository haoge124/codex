#!/usr/bin/env python3
import argparse
import base64
import json
import os
import re
from html.parser import HTMLParser
from pathlib import Path

from openai import OpenAI


class ScriptTextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_script = False
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'script':
            self.in_script = True

    def handle_endtag(self, tag):
        if tag.lower() == 'script':
            self.in_script = False

    def handle_data(self, data):
        if self.in_script:
            self.scripts.append(data)


def extract_words_from_html(html: str):
    p = ScriptTextParser()
    p.feed(html)
    joined = '\n'.join(p.scripts)

    patterns = [
        r'(?:words?|vocab(?:List)?|wordList)\s*=\s*(\[[\s\S]*?\])',
        r'(\[[\s\S]*?\])',
    ]

    words = []
    for pat in patterns:
        for m in re.finditer(pat, joined, flags=re.I):
            arr = m.group(1)
            try:
                cand = json.loads(arr)
            except json.JSONDecodeError:
                continue

            if isinstance(cand, list):
                for x in cand:
                    if isinstance(x, str):
                        words.append(x)
                    elif isinstance(x, dict):
                        for k in ('word', 'vocab', 'kana', 'kanji', 'text'):
                            val = x.get(k)
                            if isinstance(val, str):
                                words.append(val)
                                break
                if words:
                    return sorted(set(w.strip() for w in words if w.strip()))

    toks = re.findall(r'"([^"\n]{1,20})"', joined)
    for t in toks:
        if re.search(r'[\u3040-\u30ff\u4e00-\u9fff]', t):
            words.append(t)
    return sorted(set(words))


def safe_name(word: str) -> str:
    cleaned = re.sub(r'[/\\:*?"<>|]+', '_', word.strip())
    return cleaned or 'word'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--html', required=True)
    ap.add_argument('--out', default='output/vocab_images')
    ap.add_argument('--style', default='clean educational illustration')
    ap.add_argument('--size', default='1024x1024')
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--model', default='gpt-image-2')
    ap.add_argument('--quality', default='auto', choices=['auto', 'low', 'medium', 'high'])
    args = ap.parse_args()

    if not os.getenv('OPENAI_API_KEY'):
        raise SystemExit('Set OPENAI_API_KEY first')

    html = Path(args.html).read_text(encoding='utf-8', errors='ignore')
    words = extract_words_from_html(html)
    if args.limit > 0:
        words = words[:args.limit]
    if not words:
        raise SystemExit('No words found. Consider creating a words.txt and adapting parser.')

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'words.json').write_text(json.dumps(words, ensure_ascii=False, indent=2), encoding='utf-8')

    client = OpenAI()
    for i, word in enumerate(words, 1):
        prompt = (
            f"Create an educational image that clearly explains or represents the Japanese vocabulary word '{word}'. "
            f"Style: {args.style}. No watermark. Minimal readable scene."
        )
        image = client.images.generate(
            model=args.model,
            prompt=prompt,
            size=args.size,
            quality=args.quality,
        )
        raw = base64.b64decode(image.data[0].b64_json)
        fp = out / f"{safe_name(word)}.png"
        fp.write_bytes(raw)
        print(f'[{i}/{len(words)}] {word} -> {fp}')


if __name__ == '__main__':
    main()
