'use strict';
// 재료 및 효과 데이터
const ING = [{ id: 'flower', name: '붉은 꽃', icon: '🌺', desc: '회복 +3 · 활력 +1', v: [3, 1, 0, 0] }, { id: 'mushroom', name: '달빛 버섯', icon: '🍄', desc: '안정 +3 · 집중 +1', v: [0, 0, 3, 1] }, { id: 'herb', name: '은빛 허브', icon: '🌿', desc: '회복 +1 · 안정 +2', v: [1, 0, 2, 0] }, { id: 'spark', name: '번개 가루', icon: '⚡', desc: '활력 +3 · 집중 +1', v: [0, 3, 0, 1] }, { id: 'crystal', name: '수정 조각', icon: '💎', desc: '집중 +3 · 안정 +1', v: [0, 0, 1, 3] }, { id: 'honey', name: '황금 꿀', icon: '🍯', desc: '회복 +2 · 활력 +2', v: [2, 2, 0, 0] }];
const EFFECT = ['회복', '활력', '안정', '집중'];
