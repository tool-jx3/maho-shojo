import test from 'node:test';
import assert from 'node:assert/strict';
import { buildCcfolia } from './ccfolia.mjs';

const ATTRS = ['挑戰', '保護', '思慮', '情感', '奉獻'];
const POWERS = ['護甲', '昇華', '摧毀', '懲罰', '堅韌'];
const BASIC = [
	{ name: '懲戒黑暗', attribute: '挑戰' },
	{ name: '真理之光', attribute: '思慮' },
	{ name: '克服危險', attribute: '屬性' },
	{ name: '變身', attribute: '' },
	{ name: '失去光明', attribute: '屬性' },
	{ name: '抵抗黑暗', attribute: '奉獻' },
];

// 頁面算好、交給轉換模組的資料：測試以這份為底，各自覆寫需要的欄位
function sample(over) {
	return Object.assign(
		{
			name: '星野光',
			title: '黎明的守護者',
			playbook: '勇者',
			pact: '光明子女',
			friendship: '大姐頭',
			romance: '',
			profile: { life: '學生', age: '15', zodiac: '獅子座', blood: 'O 型', theme: '光', color: '金色', talisman: '戒指', treasure: '' },
			attributeKeys: ATTRS,
			attrs: { 挑戰: 2, 保護: 0, 思慮: -1, 情感: 1, 奉獻: 1 },
			ascension: {},
			powerKeys: POWERS,
			powers: { 護甲: 0, 昇華: 0, 摧毀: 1, 懲罰: 2, 堅韌: 0 },
			heartsUnlocked: ['A'],
			finalem: false,
			hearts: [{ name: '聖光斬', cat: 'A', effect: '造成懲罰點數', rule: '' }],
			forms: { super: true, triumph: false, extra: null, replaced: null },
			resources: { power: 2, light: 3, tenebrae: 0, amity: 5, dark: 1, darkLv: 0, shine: 2, shineMax: 6 },
			consequences: [],
			moves: [
				{ group: '受眷顧者', names: ['出場宣言', '以正義之力', '神聖優雅'] },
				{ group: '光明子女・盟約優勢', names: ['光之祝福'] },
			],
			advancesDone: 2,
			bonds: '與小雪是青梅竹馬。',
			basicMoves: BASIC,
		},
		over || {}
	);
}

test('輸出 ccfolia 的 character 結構，名稱取角色名', () => {
	const out = buildCcfolia(sample());
	assert.equal(out.kind, 'character');
	assert.equal(out.data.name, '星野光');
	assert.equal(out.data.initiative, 0);
	assert.ok(Array.isArray(out.data.status));
	assert.ok(Array.isArray(out.data.params));
	assert.equal(typeof out.data.commands, 'string');
	assert.equal(typeof out.data.memo, 'string');
});

test('未命名時名稱用預設值', () => {
	assert.equal(buildCcfolia(sample({ name: '' })).data.name, '未命名魔法少女');
});

test('params 依序列出五項屬性與五項力量，值為字串', () => {
	const { params } = buildCcfolia(sample()).data;
	assert.deepEqual(
		params.map((p) => p.label),
		ATTRS.concat(POWERS)
	);
	assert.deepEqual(
		params.map((p) => p.value),
		['2', '0', '-1', '1', '1', '0', '0', '1', '2', '0']
	);
});

test('status 列出能力等級與各項點數，並附上規則上限', () => {
	const { status } = buildCcfolia(sample()).data;
	const by = Object.fromEntries(status.map((s) => [s.label, s]));
	assert.deepEqual(status.map((s) => s.label), ['能力等級', '光點', '闇點', '友情點數', '黑暗點數', '黑暗等級', '閃耀點數']);
	assert.deepEqual(by['能力等級'], { label: '能力等級', value: 2, max: 5 });
	assert.deepEqual(by['闇點'], { label: '闇點', value: 0, max: 5 });
	assert.deepEqual(by['友情點數'], { label: '友情點數', value: 5, max: 10 });
	assert.deepEqual(by['黑暗等級'], { label: '黑暗等級', value: 0, max: 5 });
	assert.deepEqual(by['閃耀點數'], { label: '閃耀點數', value: 2, max: 6 });
	assert.equal(by['光點'].value, 3);
	assert.equal(by['黑暗點數'].value, 1);
	for (const s of status) {
		assert.equal(typeof s.value, 'number', s.label + ' 的 value 必須是數字');
		assert.equal(typeof s.max, 'number', s.label + ' 的 max 必須是數字');
	}
});

test('status 只在適用時加入戀愛等級、活力、人氣值', () => {
	const base = buildCcfolia(sample()).data.status.map((s) => s.label);
	assert.ok(!base.includes('戀愛等級') && !base.includes('活力') && !base.includes('人氣值'));

	const rom = buildCcfolia(sample({ romance: '初戀', resources: Object.assign(sample().resources, { romLv: 1 }) })).data.status;
	assert.deepEqual(rom.find((s) => s.label === '戀愛等級'), { label: '戀愛等級', value: 1, max: 5 });

	const fighter = buildCcfolia(sample({ playbook: '鬥士', resources: Object.assign(sample().resources, { impetus: 3 }) })).data.status;
	assert.equal(fighter.find((s) => s.label === '活力').value, 3);

	const idol = buildCcfolia(sample({ playbook: '偶像', resources: Object.assign(sample().resources, { popularity: 1, popularityMax: 3 }) })).data.status;
	assert.deepEqual(idol.find((s) => s.label === '人氣值'), { label: '人氣值', value: 1, max: 3 });
});

test('commands：每個有指定屬性的基礎動作一行，以 {屬性} 引用 params', () => {
	const lines = buildCcfolia(sample()).data.commands.split('\n');
	assert.ok(lines.includes('2D6+{挑戰} 【懲戒黑暗】'), lines.join('\n'));
	assert.ok(lines.includes('2D6+{思慮} 【真理之光】'));
	assert.ok(lines.includes('2D6+{奉獻} 【抵抗黑暗】'));
});

test('commands：「視情況決定屬性」的動作展開成五種屬性各一行，無擲骰的動作不出現', () => {
	const lines = buildCcfolia(sample()).data.commands.split('\n');
	for (const k of ATTRS) {
		assert.ok(lines.includes('2D6+{' + k + '} 【克服危險／失去光明】＋' + k), '缺少 ' + k + ' 的通用擲骰');
	}
	assert.ok(!lines.some((l) => l.includes('變身')), '變身沒有擲骰，不該出現');
	assert.equal(lines.length, 3 + 5);
	assert.ok(lines.every((l) => l.trim().length), '不該有空行');
});

test('commands：昇華指定的屬性，擲骰加值直接寫進指令', () => {
	const lines = buildCcfolia(sample({ ascension: { 挑戰: 1 } })).data.commands.split('\n');
	assert.ok(lines.includes('2D6+{挑戰}+1 【懲戒黑暗】（昇華 +1）'), lines.join('\n'));
	assert.ok(lines.includes('2D6+{挑戰}+1 【克服危險／失去光明】＋挑戰（昇華 +1）'));
	assert.ok(lines.includes('2D6+{思慮} 【真理之光】'), '未指定昇華的屬性維持原樣');
});

test('memo 摘要扮演書、盟約、稱號、個人資料與扮演書', () => {
	const memo = buildCcfolia(sample()).data.memo;
	assert.ok(memo.includes('扮演書：勇者'));
	assert.ok(memo.includes('盟約：光明子女'));
	assert.ok(memo.includes('稱號：黎明的守護者'));
	assert.ok(memo.includes('生活型態：學生'));
	assert.ok(memo.includes('護符：戒指'));
	assert.ok(!memo.includes('最珍貴的寶物'), '空欄位不列出');
	assert.ok(memo.includes('友情扮演書：大姐頭'));
	assert.ok(!memo.includes('戀愛扮演書'), '沒選戀愛扮演書就不列');
});

test('memo 列出形態、心之力、已選動作、後果與羈絆', () => {
	const memo = buildCcfolia(
		sample({
			consequences: [{ name: '疲憊', attribute: '挑戰' }, { name: '落敗', attribute: '' }],
			forms: { super: true, triumph: false, extra: '契約形態', replaced: null },
		})
	).data.memo;
	assert.ok(memo.includes('能力等級 2'));
	assert.ok(memo.includes('超級形態'));
	assert.ok(!memo.includes('凱旋形態'), '未解鎖的形態不列');
	assert.ok(memo.includes('契約形態'));
	assert.ok(memo.includes('心之力：A'));
	assert.ok(memo.includes('■受眷顧者：出場宣言、以正義之力、神聖優雅'));
	assert.ok(memo.includes('■光明子女・盟約優勢：光之祝福'));
	assert.ok(memo.includes('（A）聖光斬：造成懲罰點數'));
	assert.ok(memo.includes('疲憊（挑戰 -2）'));
	assert.ok(memo.includes('落敗'));
	assert.ok(memo.includes('成長 2 次'));
	assert.ok(memo.includes('與小雪是青梅竹馬。'));
});

test('memo 略過沒有內容的區塊，且能力量表被取代時註明', () => {
	const memo = buildCcfolia(
		sample({
			hearts: [],
			moves: [{ group: '受眷顧者', names: [] }],
			bonds: '',
			consequences: [],
			forms: { super: false, triumph: false, extra: null, replaced: '黑暗女神' },
		})
	).data.memo;
	assert.ok(!memo.includes('■受眷顧者'), '沒選任何動作的群組不列');
	assert.ok(!memo.includes('羈絆'));
	assert.ok(!memo.includes('後果'));
	assert.ok(memo.includes('黑暗女神'));
});

test('整份輸出可以 JSON 序列化，沒有 undefined', () => {
	const out = buildCcfolia(sample({ romance: '', bonds: '' }));
	const json = JSON.stringify(out);
	assert.deepEqual(JSON.parse(json), out);
	assert.ok(!json.includes('undefined'));
});
