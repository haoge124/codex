import assert from 'node:assert/strict';
import { buildPrompt, buildChatGPTUrl } from '../src/translator.js';

{
  const prompt = buildPrompt('  Hello   world\n', '翻译成中文');
  assert.equal(prompt, '翻译成中文\n\n待翻译文本：\n"""Hello world"""');
}

{
  const url = buildChatGPTUrl('a b');
  assert.equal(url, 'https://chatgpt.com/?q=a%20b');
}

console.log('translator tests passed');
