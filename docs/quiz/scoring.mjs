// 測驗的計分邏輯（純計算，沒有 DOM）。
//
// 這個檔案是唯一的來源：
//   - src/pages/quiz.astro 在建置時把它去掉 export 後直接內嵌
//   - quiz/lib.test.mjs 直接 import 它做驗證
// 因此頁面上跑的和測試驗的必然是同一份程式碼。
//
// 題庫在 src/data/quiz-questions.json，改題目不需要動這裡。

export const center = (v) => {
	const m = v.reduce((a, b) => a + b, 0) / v.length;
	return v.map((x) => x - m);
};
export const dot = (a, b) => a.reduce((n, x, i) => n + x * b[i], 0);
export const norm = (a) => Math.sqrt(dot(a, a));
export function cos(a, b) {
	const n = norm(a) * norm(b);
	return n ? dot(a, b) / n : 0;
}

// 標準常態累積分布，把 z 分數換成好讀的百分位
export function erf(x) {
	const sign = x < 0 ? -1 : 1;
	x = Math.abs(x);
	const t = 1 / (1 + 0.3275911 * x);
	const y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x);
	return sign * y;
}
export const normalCdf = (z) => 0.5 * (1 + erf(z / Math.SQRT2));

// 各扮演書的屬性組合 → 置中向量（衛士三組、鬥士兩組）
export function centeredProfiles(playbooks, keys) {
	return playbooks.map((p) => {
		const a = p.attributes;
		const sets = a.mode === 'sets' ? a.sets.map((s) => s.values) : [a.values];
		return sets.map((v) => center(keys.map((k) => v[k])));
	});
}

// 使用者側寫與某本扮演書的相關：多組屬性取最合適的一組
export function correlation(centeredUser, profiles, i) {
	let best = -2;
	for (const v of profiles[i]) {
		const c = cos(centeredUser, v);
		if (c > best) best = c;
	}
	return best;
}

export function attrVector(attrQ, picks, keys) {
	const v = Object.fromEntries(keys.map((k) => [k, 0]));
	attrQ.forEach((q, i) => {
		const p = picks[i];
		if (p == null) return;
		for (const [k, n] of Object.entries(q.o[p].w || {})) if (k in v) v[k] += n;
	});
	return v;
}

// 題數多時全列舉會太慢（成本是「每題選項數」的乘積），超過上限就改抽樣。
// 用固定種子的 PRNG，同一份題庫每次得到的校準值都一樣。
export const CALIBRATION_LIMIT = 500000;
function mulberry32(seed) {
	return function () {
		seed |= 0;
		seed = (seed + 0x6d2b79f5) | 0;
		let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
		t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
		return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
	};
}

// 各扮演書在「所有可能作答」下的平均與標準差。
// 沒有這一步，屬性組合較多或側寫較平的扮演書會佔掉大半的結果。
export function calibrate(attrQ, keys, profiles) {
	const delta = attrQ.map((q) => q.o.map((o) => keys.map((k) => (o.w || {})[k] || 0)));
	const total = delta.reduce((n, d) => n * d.length, 1);
	const n = profiles.length;
	const sum = new Array(n).fill(0);
	const sum2 = new Array(n).fill(0);
	const u = new Array(keys.length);
	let count = 0;
	const accumulate = (idx) => {
		u.fill(0);
		for (let q = 0; q < delta.length; q++) {
			const dl = delta[q][idx[q]];
			for (let i = 0; i < keys.length; i++) u[i] += dl[i];
		}
		const cu = center(u);
		for (let p = 0; p < n; p++) {
			const r = correlation(cu, profiles, p);
			sum[p] += r;
			sum2[p] += r * r;
		}
		count++;
	};
	if (total <= CALIBRATION_LIMIT) {
		const idx = new Array(delta.length).fill(0);
		for (;;) {
			accumulate(idx);
			let k = delta.length - 1;
			while (k >= 0 && ++idx[k] >= delta[k].length) { idx[k] = 0; k--; }
			if (k < 0) break;
		}
	} else {
		const rnd = mulberry32(20260820);
		const idx = new Array(delta.length).fill(0);
		for (let s = 0; s < CALIBRATION_LIMIT; s++) {
			for (let q = 0; q < delta.length; q++) idx[q] = Math.floor(rnd() * delta[q].length);
			accumulate(idx);
		}
	}
	const mean = sum.map((x) => x / count);
	const std = sum2.map((x, i) => Math.sqrt(Math.max(0, x / count - mean[i] * mean[i])));
	return { mean, std, sampled: total > CALIBRATION_LIMIT, count };
}

// 扮演書排名：換算成各自的 z 分數，顯示值為 z 的常態百分位
export function rankPlaybooks(playbooks, profiles, calib, vector, keys) {
	const u = keys.map((k) => vector[k]);
	const cu = center(u);
	if (!norm(cu)) return [];
	return playbooks
		.map((p, i) => {
			const z = (correlation(cu, profiles, i) - calib.mean[i]) / (calib.std[i] || 1);
			return { pb: p, z, fit: normalCdf(z) };
		})
		.sort((a, b) => b.z - a.z);
}

export function pactScores(pactQ, picks, names) {
	const s = Object.fromEntries(names.map((n) => [n, 0]));
	pactQ.forEach((q, i) => {
		const p = picks[i];
		if (p == null) return;
		for (const [k, n] of Object.entries(q.o[p].w || {})) if (k in s) s[k] += n;
	});
	return s;
}

// 友情扮演書：羈絆數接近程度（最多 3 分）＋標籤對象相符（3 分）
// ＋兩題風味題（位置 3 分、心聲 2 分）。回傳完整排名，頁面只呈現前幾名。
export function rankFriendship(frQ, picks, friendship, breadth, focus) {
	if (picks.some((x) => x == null)) return [];
	const target = breadth[picks[0]];
	const want = focus[picks[1]];
	const w3 = frQ[2].o[picks[2]].w || [];
	const w4 = frQ[3].o[picks[3]].w || [];
	return friendship
		.map((f) => {
			let s = 3 - Math.min(3, Math.abs(f.bondsExtra - target));
			if (f.bondFocus === want) s += 3;
			if (w3.includes(f.name)) s += 3;
			if (w4.includes(f.name)) s += 2;
			return { fr: f, score: s };
		})
		.sort((x, y) => y.score - x.score);
}
