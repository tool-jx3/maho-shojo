// 題庫的檢查與統計。給 lib.test.mjs 與 report.mjs 共用。
import { readFileSync } from 'node:fs';
import {
	attrVector, calibrate, centeredProfiles, correlation, center, norm,
	pactScores, rankFriendship, rankPlaybooks,
} from './scoring.mjs';

const read = (rel) => JSON.parse(readFileSync(new URL(rel, import.meta.url), 'utf8'));
export const QUESTIONS = read('../src/data/quiz-questions.json');
export const RULES = read('../src/data/rules.json');

export const ATTR_KEYS = RULES.attributeKeys;
export const PACT_NAMES = RULES.pacts.map((p) => p.name);
export const FR_NAMES = RULES.friendship.map((f) => f.name);
export const FRIENDSHIP = RULES.friendship.map((f) => ({
	name: f.name, bondsExtra: f.bondsExtra, bondFocus: f.bondFocus, needsPlayer: f.needsPlayer,
}));

// ---- 檢查：回傳問題清單，空陣列代表沒問題 ----
export function validate() {
	const errs = [];
	const checkQ = (q, where, opts) => {
		if (!q.q || typeof q.q !== 'string') errs.push(`${where}：缺少題目文字`);
		if (!Array.isArray(q.o) || q.o.length < 2) errs.push(`${where}：選項少於 2 個`);
		(q.o || []).forEach((o, i) => {
			if (!o.t) errs.push(`${where} 選項 ${i + 1}：缺少選項文字`);
			if (opts) opts(o, `${where} 選項 ${i + 1}`);
		});
	};
	const inSet = (set, label) => (o, where) => {
		const w = o.w;
		if (w == null) return;
		const keys = Array.isArray(w) ? w : Object.keys(w);
		for (const k of keys) {
			if (!set.includes(k)) errs.push(`${where}：「${k}」不是有效的${label}（打錯字的權重會靜默失效）`);
		}
		if (!Array.isArray(w)) {
			for (const [k, v] of Object.entries(w)) {
				if (!Number.isFinite(v) || v <= 0) errs.push(`${where}：「${k}」的權重必須是正數，目前是 ${v}`);
			}
		}
	};

	QUESTIONS.pact.forEach((q, i) => checkQ(q, `盟約第 ${i + 1} 題`, inSet(PACT_NAMES, '盟約名稱')));
	QUESTIONS.attribute.forEach((q, i) => {
		checkQ(q, `屬性第 ${i + 1} 題`, inSet(ATTR_KEYS, '屬性名稱'));
		if (q.o.some((o) => !o.w || !Object.keys(o.w).length)) errs.push(`屬性第 ${i + 1} 題：有選項沒有任何權重`);
	});

	const fr = QUESTIONS.friendship;
	fr.questions.forEach((q, i) => checkQ(q, `友情第 ${i + 1} 題`, i >= 2 ? inSet(FR_NAMES, '友情扮演書名稱') : null));
	if (fr.questions.length !== 4) errs.push('友情題必須剛好 4 題（前兩題對應羈絆數與標籤對象）');
	if (fr.breadth.length !== fr.questions[0].o.length) errs.push('friendship.breadth 的長度必須等於第 1 題的選項數');
	if (fr.focus.length !== fr.questions[1].o.length) errs.push('friendship.focus 的長度必須等於第 2 題的選項數');
	for (const f of fr.focus) {
		if (!['single', 'group', 'none'].includes(f)) errs.push(`friendship.focus 不認得「${f}」`);
	}
	return errs;
}

// ---- 統計 ----
const combos = (qs) => {
	const out = [];
	const idx = new Array(qs.length).fill(0);
	for (;;) {
		out.push(idx.slice());
		let k = qs.length - 1;
		while (k >= 0 && ++idx[k] >= qs[k].o.length) { idx[k] = 0; k--; }
		if (k < 0) break;
	}
	return out;
};

export function attributeWeights() {
	const w = Object.fromEntries(ATTR_KEYS.map((k) => [k, 0]));
	for (const q of QUESTIONS.attribute) {
		for (const o of q.o) for (const [k, v] of Object.entries(o.w || {})) if (k in w) w[k] += v;
	}
	return w;
}

export function playbookDistribution() {
	const profiles = centeredProfiles(RULES.playbooks, ATTR_KEYS);
	const calib = calibrate(QUESTIONS.attribute, ATTR_KEYS, profiles);
	const win = Object.fromEntries(RULES.playbooks.map((p) => [p.name, 0]));
	let total = 0;
	for (const pick of combos(QUESTIONS.attribute)) {
		const rank = rankPlaybooks(RULES.playbooks, profiles, calib,
			attrVector(QUESTIONS.attribute, pick, ATTR_KEYS), ATTR_KEYS);
		if (rank.length) { win[rank[0].pb.name]++; total++; }
	}
	return { win, total, calib };
}

export function pactDistribution() {
	const win = Object.fromEntries(PACT_NAMES.map((n) => [n, 0]));
	let total = 0, tie = 0;
	for (const pick of combos(QUESTIONS.pact)) {
		const s = pactScores(QUESTIONS.pact, pick, PACT_NAMES);
		const max = Math.max(...PACT_NAMES.map((n) => s[n]));
		const top = PACT_NAMES.filter((n) => s[n] === max);
		total++;
		if (top.length > 1) tie++;
		else win[top[0]]++;
	}
	return { win, total, tie };
}

export function friendshipDistribution() {
	const fr = QUESTIONS.friendship;
	const win = Object.fromEntries(FR_NAMES.map((n) => [n, 0]));
	let total = 0;
	for (const pick of combos(fr.questions)) {
		const rank = rankFriendship(fr.questions, pick, FRIENDSHIP, fr.breadth, fr.focus);
		win[rank[0].fr.name]++;
		total++;
	}
	return { win, total };
}

export const spread = (win, total) => {
	const pct = Object.values(win).map((x) => (x * 100) / total);
	return { min: Math.min(...pct), max: Math.max(...pct), ratio: Math.max(...pct) / Math.min(...pct) };
};
export { center, norm, correlation };
