// 從 glossary.json 取出可進斷詞字典的術語。
// 排除明確標記為 candidate／deprecated 的詞條：尚未定案或已棄用的譯名進入字典，
// 只會讓搜尋字典與正文用詞不一致（Law 7）。
import fs from 'node:fs/promises';
import { HAN_ONLY } from '../client/segment.mjs';

// 本專案與模板（僅收 status === 'approved'）的差異：glossary 有約 200 筆核心詞條
// 建立於 status 欄位導入之前，只帶 is_term，其中包含「動作」「反應」「扮演書」等
// 最常被查詢的術語，一律排除會少掉近四成字典。專案自己的
// scripts/_term_lib.py:is_managed_term 也把 `is_term === true` 與
// `status === 'approved'` 同等視為受管術語，故此處比照：未標 status 者視為已在用。
const EXCLUDED_STATUS = new Set(['candidate', 'deprecated']);

/**
 * @param {object} glossary 解析後的 glossary.json 內容
 * @returns {string[]} 純漢字且長度 > 1 的在用譯名；沒有任何可用詞條時為空陣列
 *   ——新專案的 glossary 只有 _meta，這是合法狀態，由呼叫端決定是否降級為純 ICU 斷詞。
 */
export function extractTerms(glossary) {
	const terms = [];
	for (const value of Object.values(glossary)) {
		if (!value || typeof value !== 'object') continue;
		if (typeof value.status === 'string' && EXCLUDED_STATUS.has(value.status)) continue;
		const zh = typeof value.zh === 'string' ? value.zh.trim() : '';
		if (zh.length > 1 && HAN_ONLY.test(zh)) terms.push(zh);
	}
	return terms;
}

/**
 * @param {string} glossaryPath glossary.json 的絕對路徑
 * @returns {Promise<string[]>}
 * @throws 檔案缺失或 JSON 損壞時——搜尋品質直接取決於術語表，
 *   靜默降級會產出看似正常但品質低落的索引。
 */
export async function loadTerms(glossaryPath) {
	let raw;
	try {
		raw = JSON.parse(await fs.readFile(glossaryPath, 'utf8'));
	} catch (err) {
		throw new Error(`無法讀取 glossary.json（${glossaryPath}）：${err.message}`);
	}
	return extractTerms(raw);
}
