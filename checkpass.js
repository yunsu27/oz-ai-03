function checkPass(score) {
    if (score >= 60) return "합격";
    return "불합격";
}

// 테스트 데이터 (for문으로 한꺼번에 판정)
const scores = [89, 40, 71, 22];
for (let s of scores) {
    console.log(`점수: ${s}, 결과: ${checkPass(s)}`);
}