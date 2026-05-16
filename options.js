const DEFAULT_INSTRUCTION = '请准确翻译为简体中文，保留专有名词与格式。';

async function load() {
  const { customInstruction } = await chrome.storage.sync.get({
    customInstruction: DEFAULT_INSTRUCTION
  });
  document.getElementById('instruction').value = customInstruction;
}

async function save() {
  const value = document.getElementById('instruction').value.trim() || DEFAULT_INSTRUCTION;
  await chrome.storage.sync.set({ customInstruction: value });
  const status = document.getElementById('status');
  status.textContent = '已保存';
  setTimeout(() => { status.textContent = ''; }, 1500);
}

document.getElementById('save').addEventListener('click', save);
load();
