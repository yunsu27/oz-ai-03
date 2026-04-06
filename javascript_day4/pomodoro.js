const timeInput = document.querySelector("#time-input");
const startBtn = document.querySelector("#start-timer");
const stopBtn = document.querySelector("#stop-timer");
const display = document.querySelector("#timer-display");


let timerId = null;
let remainingSeconds = 0;

// 현재 남은 시간(초)를 {분:초} 형태로 출력
function updateDisplay() {
    const min = Math.floor(remainingSeconds / 60);
    const sec = remainingSeconds % 60;

    // min=1 & sec=9 -> 01:09로 변환
    display.textContent = 
        String(min).padStart(2, "0") + ":" + String(sec).padStart(2, "0");
    display.className = "fs-3";
};


// Timer 시작
startBtn.addEventListener("click", () => {
    // 이미 타이머가 동작 중이면, 무시
    if (timerId !== null) {
        alert("이미 동작 중인 타이머가 있습니다!");
        return;
    };

    // 유효한 값: 15
    // 유효하지 않은 값: 15분, 십오분
    const minutes = Number(timeInput.value);
    if (!minutes || isNaN(minutes) || minutes <= 0) {
        alert("시간을 분 단위(숫자)로 입력하세요.");
        return;
    };

    remainingSeconds = minutes * 60;
    updateDisplay();

    // 1초마다 반복적으로 동작하는 함수를 추가
    timerId = setInterval(() => {
        remainingSeconds--;

        // 남은 시간이 없으면, 타이멎 종료
        if (remainingSeconds <= 0) {
            resetTimer();
        } else {
            updateDisplay();
        };
    }, 1000);
});

stopBtn.addEventListener("click", resetTimer);

function resetTimer() {
    clearInterval(timerId);
    timerId = null;
};
