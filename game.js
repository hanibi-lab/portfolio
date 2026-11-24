'use strict';
// 게임 상태 및 진행 관리
let state;
const $ = id => document.getElementById(id);
let toastTimer;
function newGame() { state = { index: 0, gold: 30, rep: 50, stock: Object.fromEntries(ING.map(i => [i.id, 5])), selected: [], results: [], finished: false }; $('overlay').classList.remove('show'); render(); }
function current() { return CUSTOMERS[state.index]; }
function choose(id) { if (state.finished || state.selected.length >= 3 || state.stock[id] <= state.selected.filter(x => x === id).length)
    return; state.selected.push(id); render(); }
function skip() { if (state.finished)
    return; const c = current(); state.rep = Math.max(0, state.rep - 5); state.results.push({ name: c.name, grade: '거절', pay: 0 }); journal(`${c.name}의 의뢰를 거절했습니다. 평판 -5.`); advance(); }
function advance() { state.index++; if (state.index >= CUSTOMERS.length) {
    finish();
    return;
} render(); if (state.index % 3 === 0) {
    showModal('🌙 하루가 저물었습니다', `${state.index / 3}일차 영업 종료!<br>내일은 새로운 손님들이 찾아옵니다.<br>현재 골드 <b>${state.gold}G</b> · 평판 <b>${state.rep}</b>`, '다음 날 시작', () => { $('overlay').classList.remove('show'); render(); });
}
else
    toast('새로운 손님이 찾아왔습니다!'); }
function finish() { state.finished = true; render(); const wins = state.results.filter(r => r.grade.includes('성공')).length; const rank = state.rep >= 85 && state.gold >= 100 ? '왕국 최고의 연금술사 🏆' : state.rep >= 60 ? '믿음직한 마을 연금술사 🌟' : '수습 연금술사 🌱'; showModal('🎉 5일간의 영업 종료', `<b>${rank}</b><br>성공 의뢰 ${wins}/15 · 최종 평판 ${state.rep} · 골드 ${state.gold}G<br><br>손님에게 필요한 효과를 읽고 재료를 조합하는 것이 핵심입니다.`, '다시 플레이', newGame); }
