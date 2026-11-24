'use strict';
// 버튼 이벤트 연결 및 게임 시작
$('brewBtn').onclick = brew;
$('skipBtn').onclick = skip;
$('clearBtn').onclick = () => { state.selected = []; render(); };
$('hintBtn').onclick = () => { const c = current(); toast(`의뢰 분석: 필요한 효과는 '${EFFECT[c.target]}', 목표 수치 ${c.need} 이상입니다.`); journal(`🔎 의뢰 분석 결과: ${c.name}에게는 '${EFFECT[c.target]}' 효과 ${c.need} 이상이 필요합니다. 다른 효과보다 주요 효과가 높으면 유리합니다.`); };
$('buyBtn').onclick = () => { if (state.gold < 12)
    return; state.gold -= 12; ING.forEach(i => state.stock[i.id] += 2); journal('재료 보충 완료! 12G를 지불하고 모든 재료를 2개씩 받았습니다.'); render(); };
newGame();
showModal('🌙 마녀의 작은 연금술 공방', '작은 공방을 운영하며 <b>5일 동안 15명의 손님</b>에게 물약을 만들어 주세요.<br><br>손님의 고민을 읽고 재료를 <b>최대 3개</b> 조합합니다. 재료를 클릭해 가마솥에 넣고 <b>물약 제조하기</b>를 누르세요.<br><br>골드와 평판을 높여 왕국 최고의 연금술사가 되어 보세요!', '공방 문 열기', () => $('overlay').classList.remove('show'));
