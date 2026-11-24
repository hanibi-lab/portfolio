'use strict';
// 물약 효과 계산 및 제조 판정
function scorePotion() { let values = [0, 0, 0, 0]; state.selected.forEach(id => { const v = ING.find(i => i.id === id).v; v.forEach((n, j) => values[j] += n); }); return values; }
function brew() { if (state.finished || !state.selected.length)
    return; const c = current(), v = scorePotion(), value = v[c.target], other = Math.max(...v.filter((_, j) => j !== c.target)); let grade, pay, repDelta; if (value >= c.need && value >= other) {
    grade = '대성공 ✨';
    pay = 18;
    repDelta = 8;
}
else if (value >= Math.ceil(c.need * .6) && value >= other - 1) {
    grade = '성공 🌟';
    pay = 11;
    repDelta = 4;
}
else {
    grade = '실패 💧';
    pay = 2;
    repDelta = -8;
} state.selected.forEach(id => state.stock[id]--); state.gold += pay; state.rep = Math.max(0, Math.min(100, state.rep + repDelta)); state.results.push({ name: c.name, grade, pay }); journal(`${c.name}: ${grade}! ${EFFECT[c.target]} ${value}/${c.need}, 보상 ${pay}G, 평판 ${repDelta >= 0 ? '+' : ''}${repDelta}.`); state.selected = []; advance(); }
