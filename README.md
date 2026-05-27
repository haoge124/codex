# JLPT 单词配图批量生成

可以，脚本已支持**直接使用 OpenAI 的 gpt-image-2（Image 2）模型**批量出图。

## 功能

1. 读取你下载好的 `jlpt_vocab.html`。
2. 自动尝试提取页面里的单词列表。
3. 每个单词生成 1 张图，并按“单词名.png”保存。

## 用法

```bash
python -m pip install -U openai
python generate_vocab_images.py --html jlpt_vocab.html --out output/vocab_images
```

默认模型是 `gpt-image-2`，可选参数如下：

- `--model gpt-image-2`（默认）
- `--quality auto|low|medium|high`（默认 `auto`）
- `--limit 50` 先生成前 50 个词测试
- `--style "flat icon style"` 改图片风格
- `--size 1024x1024` 改分辨率

示例（明确指定 image2 + 中等质量）：

```bash
python generate_vocab_images.py \
  --html jlpt_vocab.html \
  --out output/vocab_images \
  --model gpt-image-2 \
  --quality medium
```

## 说明

- 输出目录默认是 `output/vocab_images/`。
- 会额外生成 `words.json`（提取到的单词清单）。
- 运行前需先设置 `OPENAI_API_KEY`。
