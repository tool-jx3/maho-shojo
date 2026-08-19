import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { extractTerms, loadTerms } from './load-terms.mjs';

test('取出 approved 詞條的 zh 譯名', () => {
	const glossary = {
		_meta: { description: '術語表', updated: '' },
		Movimiento: { zh: '動作', status: 'approved', is_term: true },
		Libreto: { zh: '扮演書', status: 'approved', is_term: true },
	};
	assert.deepEqual(extractTerms(glossary), ['動作', '扮演書']);
});

test('candidate 與 deprecated 詞條不進入斷詞字典', () => {
	const glossary = {
		Approved: { zh: '原型', status: 'approved' },
		Candidate: { zh: '待定詞', status: 'candidate' },
		Deprecated: { zh: '棄用詞', status: 'deprecated' },
	};
	assert.deepEqual(extractTerms(glossary), ['原型']);
});

test('缺 status 欄位的詞條視為在用而收錄（本專案早期詞條只帶 is_term）', () => {
	const glossary = {
		NoStatus: { zh: '反應', is_term: true },
		NotTerm: { zh: '星之城堡', is_term: false },
		Ok: { zh: '場景', status: 'approved' },
	};
	assert.deepEqual(extractTerms(glossary), ['反應', '星之城堡', '場景']);
});

test('單字、含英數與空白的 zh 排除；zh 先 trim 再判斷', () => {
	const glossary = {
		Single: { zh: '靈', status: 'approved' },
		Latin: { zh: '附錄 A', status: 'approved' },
		Spaced: { zh: '  颶光  ', status: 'approved' },
		Empty: { zh: '', status: 'approved' },
		NotString: { zh: 42, status: 'approved' },
	};
	assert.deepEqual(extractTerms(glossary), ['颶光']);
});

test('零可用詞條回傳空陣列而非拋錯（新專案的合法狀態）', () => {
	assert.deepEqual(extractTerms({ _meta: { description: '', updated: '' } }), []);
	assert.deepEqual(extractTerms({}), []);
});

test('loadTerms：合法檔案回傳詞條', async () => {
	const dir = await fs.mkdtemp(path.join(os.tmpdir(), 'load-terms-'));
	const file = path.join(dir, 'glossary.json');
	await fs.writeFile(file, JSON.stringify({ Term: { zh: '颶光', status: 'approved' } }), 'utf8');
	assert.deepEqual(await loadTerms(file), ['颶光']);
	await fs.rm(dir, { recursive: true, force: true });
});

test('loadTerms：檔案不存在時拋出含路徑的錯誤', async () => {
	const missing = path.join(os.tmpdir(), 'load-terms-missing', 'glossary.json');
	await assert.rejects(() => loadTerms(missing), (err) => err.message.includes(missing));
});

test('loadTerms：JSON 損壞時拋錯', async () => {
	const dir = await fs.mkdtemp(path.join(os.tmpdir(), 'load-terms-'));
	const file = path.join(dir, 'glossary.json');
	await fs.writeFile(file, '{ broken', 'utf8');
	await assert.rejects(() => loadTerms(file), (err) => err.message.includes(file));
	await fs.rm(dir, { recursive: true, force: true });
});
