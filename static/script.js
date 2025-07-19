// Chart.js 초기화
const ctx = document.getElementById('ear-graph').getContext('2d');
const earChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: [],
    datasets: [{
      label: 'EAR 값',
      data: [],
      borderColor: '#3B82F6', // 파란색
      fill: false,
      tension: 0.1
    }]
  },
  options: {
    responsive: true,
    animation: false,
    scales: {
      y: { suggestedMin: 0.15, suggestedMax: 0.35 }
    }
  }
});

const wrapper = document.querySelector(".max-w-2xl");

// 그래프 갱신
function updateGraph(ear) {
  const now = new Date().toLocaleTimeString();
  if (earChart.data.labels.length >= 10) {
    earChart.data.labels.shift();
    earChart.data.datasets[0].data.shift();
  }
  earChart.data.labels.push(now);
  earChart.data.datasets[0].data.push(ear);
  earChart.update();
}

// 로그에 메시지 추가
function logEvent(message) {
  const log = document.getElementById("log");
  const p = document.createElement("p");
  p.innerText = `${new Date().toLocaleTimeString()} ${message}`;
  log.prepend(p);
}

// 1초마다 서버에 EAR 요청
setInterval(async () => {
  const res = await fetch('/ear');
  const data = await res.json();

  document.getElementById("ear-value").innerText = data.ear.toFixed(2);

  const statusText = document.getElementById("status-text");
  const statusIcon = document.getElementById("status-icon");

  if (data.status === "위험") {
    statusText.innerText = "위험";
    statusText.className = "font-semibold text-red-600";
    statusIcon.innerText = "❌";
    logEvent(`위험 상태! EAR=${data.ear.toFixed(2)} 지속시간=${data.risk_duration}s`);
  
    // 깜빡임 효과 추가
    if (data.risk_duration >= 3) {
      wrapper.classList.add("alert-blink");
    } else {
      wrapper.classList.remove("alert-blink");
    }
  } else {
    wrapper.classList.remove("alert-blink"); // 안전 상태면 깜빡임 제거
  
    if (data.status === "주의") {
      statusText.innerText = "주의";
      statusText.className = "font-semibold text-yellow-500";
      statusIcon.innerText = "⚠️";
      logEvent(`주의 상태. EAR=${data.ear.toFixed(2)}`);
    } else {
      statusText.innerText = "정상";
      statusText.className = "font-semibold text-green-600";
      statusIcon.innerText = "✅";
    }
  }
  
  updateGraph(data.ear);
}, 1000);
