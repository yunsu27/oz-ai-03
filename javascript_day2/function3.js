// 지금까지 배운 JS 문법(조건문, 반복문, 함수 등)을 활용하는 실습

function getAverage(scores) {
    if (scores.length === 0) {
        return 0;
    };
    
    let sum = 0;
    for (const score of scores) {
        sum += score
    }
    return sum / scores.length;
};

const scores = [80, 85, 92, 27];
const average = getAverage(scores);
console.log(average);