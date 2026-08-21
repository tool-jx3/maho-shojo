// 改完題庫後跑這支，看看有沒有寫壞、平衡有沒有跑掉：
//   npm run quiz-report
import {
	QUESTIONS, ATTR_KEYS, attributeWeights, validate,
	playbookDistribution, pactDistribution, friendshipDistribution, spread,
} from './lib.mjs';

const bar = (pct) => '█'.repeat(Math.round(pct));
const line = (name, c, total, width = 6) =>
	`  ${name.padEnd(width, '　')} ${String(c).padStart(6)}  ${((c * 100) / total).toFixed(1).padStart(5)}%  ${bar((c * 100) / total)}`;

const errs = validate();
if (errs.length) {
	console.log('✗ 題庫有問題：');
	for (const e of errs) console.log('  -', e);
	process.exitCode = 1;
} else {
	console.log('✓ 題庫檢查通過');
}

const nq = QUESTIONS.pact.length + QUESTIONS.attribute.length + QUESTIONS.friendship.questions.length;
console.log(`\n題數 ${nq}（盟約 ${QUESTIONS.pact.length}／屬性 ${QUESTIONS.attribute.length}／友情 ${QUESTIONS.friendship.questions.length}）`);
console.log('屬性權重合計:', Object.entries(attributeWeights()).map(([k, v]) => `${k} ${v}`).join('　'));

const pb = playbookDistribution();
const s1 = spread(pb.win, pb.total);
console.log(`\n扮演書出線率（窮舉 ${pb.total} 種作答${pb.calib.sampled ? '，校準改用抽樣' : ''}）`);
for (const [n, c] of Object.entries(pb.win)) console.log(line(n, c, pb.total, 4));
console.log(`  極差 ${s1.min.toFixed(1)}–${s1.max.toFixed(1)}%（${s1.ratio.toFixed(2)} 倍）`);

const pa = pactDistribution();
const s2 = spread(pa.win, pa.total - pa.tie);
console.log(`\n盟約出線率（窮舉 ${pa.total} 種作答；同分 ${((pa.tie * 100) / pa.total).toFixed(1)}%，頁面會並列）`);
for (const [n, c] of Object.entries(pa.win)) console.log(line(n, c, pa.total - pa.tie, 5));
console.log(`  極差 ${s2.min.toFixed(1)}–${s2.max.toFixed(1)}%（${s2.ratio.toFixed(2)} 倍）`);

const f = friendshipDistribution();
const s3 = spread(f.win, f.total);
console.log(`\n友情扮演書出線率（窮舉 ${f.total} 種作答）`);
for (const [n, c] of Object.entries(f.win)) console.log(line(n, c, f.total, 5));
console.log(`  極差 ${s3.min.toFixed(1)}–${s3.max.toFixed(1)}%（${s3.ratio.toFixed(2)} 倍）`);
