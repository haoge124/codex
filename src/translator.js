export function buildPrompt(text, instruction) {
  const normalized = text.replace(/\s+/g, ' ').trim();
  return `${instruction}\n\n待翻译文本：\n"""${normalized}"""`;
}

export function buildChatGPTUrl(prompt) {
  const encoded = encodeURIComponent(prompt);
  return `https://chatgpt.com/?q=${encoded}`;
}
