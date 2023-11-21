document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');
  var calendar = new FullCalendar.Calendar(calendarEl, {
    headerToolbar: {
      left: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek',
      center: 'title',
      right: 'prev,next today'
    },
    initialView: 'timeGridWeek',
    events: '/events',
    locale: 'ja',
    buttonText: {
        prev:     '<',
        next:     '>',
        prevYear: '<<',
        nextYear: '>>',
        today:    '今日',
        month:    '月',
        week:     '週',
        day:      '日',
        list:     '一覧'
    },
    slotMinTime: "07:00:00",
    slotMaxTime: "20:00:00",
    allDaySlot: false,
    nowIndicator: true,
    editable: true,
  });
  calendar.render();
});

// 時間の選択肢を生成
const time_optionsData = [
    { value: '', text: '選択肢から選んでください' },
    { value: '朝', text: '朝' },
    { value: '1時間目', text: '1時間目' },
    { value: '2時間目', text: '2時間目' },
    { value: '3時間目', text: '3時間目' },
    { value: '昼', text: '昼' },
    { value: '4時間目', text: '3時間目' },
    { value: '5時間目', text: '4時間目' },
    { value: '6時間目', text: '5時間目' },
    { value: '放課後', text: '放課後' },
];
  
// time_select要素を取得
const time_selectElement = document.getElementById('time');
time_optionsData.forEach(option => {
    const time_optionElement = document.createElement('option');
    time_optionElement.value = option.value;
    time_optionElement.textContent = option.text;
    time_selectElement.appendChild(time_optionElement);
});


// 場所の選択肢を生成
const place_optionsData = [
  { value: '', text: '選択肢から選んでください' },
  { value: '体育館', text: '体育館' },
  { value: '音楽室', text: '音楽室' },
  { value: '選択肢A', text: '選択肢A' },
  { value: '選択肢B', text: '選択肢B' },
];
// select要素を取得
const place_selectElement = document.getElementById('place');
place_optionsData.forEach(option => {
  const place_optionElement = document.createElement('option');
  place_optionElement.value = option.value;
  place_optionElement.textContent = option.text;
  place_selectElement.appendChild(place_optionElement);
});

// 入力されていなかったらアラート
// ボタン要素を取得
const submitButton = document.getElementById('form');
// ボタンがクリックされたときの処理
submitButton.addEventListener('submit', function (event) {
  event.preventDefault(); // フォームの実際の送信を防止
  const elementsWithClass = document.querySelectorAll('.touroku');
  let isEmpty = false;
  elementsWithClass.forEach(element => {
    if (element.value.trim() === '') {
      isEmpty = true;
    }
  });
  if (isEmpty) {
      alert('空欄があります。');
    } 
  else {
      // フォームが正常に送信できる処理をここに追加
      form.submit(); // フォームを送信
  }
});
