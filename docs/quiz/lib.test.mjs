import test from 'node:test';
import assert from 'node:assert/strict';
import {
	QUESTIONS, ATTR_KEYS, PACT_NAMES, FR_NAMES, validate, attributeWeights,
	playbookDistribution, pactDistribution, friendshipDistribution, spread,
} from './lib.mjs';

test('題庫格式與名稱都正確', () => {
	const errs = validate();
	assert.deepEqual(errs, [], '題庫檢查失敗：\n' + errs.join('\n'));
});

test('題數與各段落的組成', () => {
	assert.equal(QUESTIONS.pact.length, 4);
	assert.ok(QUESTIONS.attribute.length >= 6, '屬性題至少 6 題，否則鑑別度不足');
	assert.equal(QUESTIONS.friendship.questions.length, 4);
});

test('五項屬性的權重不會有一項被冷落', () => {
	const w = attributeWeights();
	const vals = ATTR_KEYS.map((k) => w[k]);
	assert.ok(Math.min(...vals) > 0, '每項屬性都必須有選項給分');
	assert.ok(Math.max(...vals) / Math.min(...vals) <= 2,
		`屬性權重落差過大：${JSON.stringify(w)}`);
});

test('六本扮演書都可能出線，且分佈不偏斜', () => {
	const { win, total } = playbookDistribution();
	for (const [name, c] of Object.entries(win)) {
		assert.ok(c > 0, `${name} 在任何作答下都不會出線`);
	}
	const s = spread(win, total);
	assert.ok(s.ratio <= 2.5, `扮演書出線率落差 ${s.ratio.toFixed(2)} 倍，超過 2.5 倍`);
});

test('三種盟約對稱，且都可能出線', () => {
	const { win, total, tie } = pactDistribution();
	for (const n of PACT_NAMES) assert.ok(win[n] > 0, `${n} 不會單獨出線`);
	const s = spread(win, total - tie);
	assert.ok(s.ratio <= 1.2, `盟約出線率落差 ${s.ratio.toFixed(2)} 倍`);
});

test('十本友情扮演書都可能出線', () => {
	const { win, total } = friendshipDistribution();
	for (const n of FR_NAMES) assert.ok(win[n] > 0, `${n} 在任何作答下都不會出線`);
	const s = spread(win, total);
	assert.ok(s.ratio <= 3, `友情扮演書出線率落差 ${s.ratio.toFixed(2)} 倍`);
});
