import { buildPrompt, buildChatGPTUrl } from './src/translator.js';

const MENU_ID = 'translate_to_zh_cn';

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: MENU_ID,
    title: '翻译为中文（ChatGPT）',
    contexts: ['selection']
  });
});

chrome.contextMenus.onClicked.addListener(async (info) => {
  if (info.menuItemId !== MENU_ID) return;

  const selectedText = (info.selectionText || '').trim();
  if (!selectedText) {
    console.warn('No selected text to translate.');
    return;
  }

  const { customInstruction } = await chrome.storage.sync.get({
    customInstruction: '请准确翻译为简体中文，保留专有名词与格式。'
  });

  const prompt = buildPrompt(selectedText, customInstruction);
  const targetUrl = buildChatGPTUrl(prompt);

  await chrome.tabs.create({
    url: targetUrl,
    active: true
  });
});
