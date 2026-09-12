// 把角色卡建立頁算好的角色資料，轉成 ccfolia（ココフォリア）Clipboard API 的角色格式。
// 只有這一份實作：頁面（src/pages/character.astro）在建置時去掉 export 後內嵌，
// ccfolia.test.mjs 直接 import 同一個檔案驗證。
//
// 輸入 view 由頁面整理（屬性、力量、資源都已依規則算好），本模組不碰 DOM、不讀規則檔。
// 輸出貼進 ccfolia 房間（Ctrl+V）即成為一顆角色駒：
//   status  ── 遊戲中會增減的點數（有上限的照規則，沒上限的照建立頁的輸入範圍）
//   params  ── 五項屬性與五項光之裝束力量，值為字串（ccfolia 規格）
//   commands ── 聊天面板：每個基礎動作一行，以 {屬性} 引用 params，屬性改了擲骰就跟著變
//   memo    ── 角色摘要與已選動作

const UNCAPPED_MAX = 20; // 光點、黑暗點數、活力沒有規則上限，沿用建立頁的輸入上限
const SITUATIONAL = '屬性'; // 規則抽取檔裡「視情況決定的屬性」的標記

export function buildCcfolia(view) {
	return {
		kind: 'character',
		data: {
			name: view.name || '未命名魔法少女',
			memo: buildMemo(view),
			initiative: 0,
			status: buildStatus(view),
			params: buildParams(view),
			commands: buildCommands(view),
		},
	};
}

function buildStatus(view) {
	const r = view.resources || {};
	const n = (v) => Number(v) || 0;
	const out = [
		{ label: '能力等級', value: n(r.power), max: 5 },
		{ label: '光點', value: n(r.light), max: UNCAPPED_MAX },
		{ label: '闇點', value: n(r.tenebrae), max: 5 },
		{ label: '友情點數', value: n(r.amity), max: 10 },
		{ label: '黑暗點數', value: n(r.dark), max: UNCAPPED_MAX },
		{ label: '黑暗等級', value: n(r.darkLv), max: 5 },
		{ label: '閃耀點數', value: n(r.shine), max: n(r.shineMax) },
	];
	if (r.romLv != null) out.push({ label: '戀愛等級', value: n(r.romLv), max: 5 });
	if (r.impetus != null) out.push({ label: '活力', value: n(r.impetus), max: UNCAPPED_MAX });
	if (r.popularity != null) out.push({ label: '人氣值', value: n(r.popularity), max: n(r.popularityMax) });
	return out;
}

function buildParams(view) {
	const attrs = view.attrs || {};
	const powers = view.powers || {};
	return []
		.concat((view.attributeKeys || []).map((k) => ({ label: k, value: String(attrs[k] || 0) })))
		.concat((view.powerKeys || []).map((k) => ({ label: k, value: String(powers[k] || 0) })));
}

function buildCommands(view) {
	const asc = view.ascension || {};
	// 昇華是「使用該屬性的動作 +1」的擲骰加值，不是屬性值，所以寫進指令而非 params
	const dice = (k) => '2D6+{' + k + '}' + (asc[k] ? '+' + asc[k] : '');
	const suffix = (k) => (asc[k] ? '（昇華 +' + asc[k] + '）' : '');
	const named = [];
	const situational = [];
	(view.basicMoves || []).forEach((m) => {
		if (!m.attribute) return; // 變身、心之力、閃耀時刻：沒有擲骰
		if (m.attribute === SITUATIONAL) situational.push(m.name);
		else named.push(dice(m.attribute) + ' 【' + m.name + '】' + suffix(m.attribute));
	});
	const generic = situational.length
		? (view.attributeKeys || []).map((k) => dice(k) + ' 【' + situational.join('／') + '】＋' + k + suffix(k))
		: [];
	return named.concat(generic).join('\n');
}

function buildMemo(view) {
	const p = view.profile || {};
	const f = view.forms || {};
	const lines = [];
	const pair = (label, v) => (v ? label + '：' + v : '');
	const row = (items) => items.filter(Boolean).join('　');

	lines.push(row([pair('扮演書', view.playbook), '盟約：' + (view.pact || '未定')]));
	lines.push(pair('稱號', view.title));
	lines.push(row([pair('生活型態', p.life), pair('年齡', p.age), pair('星座', p.zodiac), pair('血型', p.blood)]));
	lines.push(row([pair('主題', p.theme), pair('色彩', p.color), pair('護符', p.talisman), pair('最珍貴的寶物', p.treasure)]));
	lines.push(row([pair('友情扮演書', view.friendship), pair('戀愛扮演書', view.romance)]));

	const forms = ['基礎形態'];
	if (f.super) forms.push('超級形態');
	if (f.triumph) forms.push('凱旋形態');
	if (f.extra) forms.push(f.extra);
	const r = view.resources || {};
	lines.push(
		row([
			'能力等級 ' + (Number(r.power) || 0),
			'形態：' + forms.join('、'),
			f.replaced ? '（能力量表已由「' + f.replaced + '」取代，以闇點計算等級）' : '',
			'成長 ' + (Number(view.advancesDone) || 0) + ' 次',
		])
	);
	const hearts = view.heartsUnlocked || [];
	lines.push(row([hearts.length ? '心之力：' + hearts.join('／') : '', view.finalem ? '終曲：可用' : '']));

	const blocks = [];
	(view.moves || []).forEach((g) => {
		if ((g.names || []).length) blocks.push('■' + g.group + '：' + g.names.join('、'));
	});
	const hm = (view.hearts || []).filter((h) => h.name || h.effect || h.rule);
	if (hm.length) {
		blocks.push(
			'■心之力\n' +
				hm
					.map((h) => '（' + h.cat + '）' + (h.name || '未命名') + '：' + [h.rule, h.effect].filter(Boolean).join(' '))
					.join('\n')
		);
	}
	const cons = view.consequences || [];
	if (cons.length) {
		blocks.push('■已標記後果：' + cons.map((c) => c.name + (c.attribute ? '（' + c.attribute + ' -2）' : '')).join('、'));
	}
	if (view.bonds) blocks.push('■羈絆／備註\n' + view.bonds);

	return lines
		.filter(Boolean)
		.concat(blocks.length ? [''].concat(blocks) : [])
		.join('\n');
}
