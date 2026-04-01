function calculator(n1, op, n2) {
    if (op === '+') return n1 + n2;
    if (op === '-') return n1 - n2;
    if (op === '*') return n1 * n2;
    if (op === '/') return n2 !== 0 ? n1 / n2 : "0 불가";
    return "오류";
}

console.log(calculator(10, '+', 5));
console.log(calculator(20, '*', 3));