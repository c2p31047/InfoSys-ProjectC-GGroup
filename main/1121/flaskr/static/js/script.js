// script.js

document.addEventListener('DOMContentLoaded', function() {
    // FullCalendarの初期化
    var calendar = $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        defaultView: 'month',
        selectable: true,
        selectHelper: true,
        events: '/events', // イベントデータを取得するエンドポイント
        // カレンダー内でイベントがクリックされたときの処理
        eventClick: function(event) {
            // 予約詳細を表示する処理を実装する
            showReservationDetail(event);
        }
    });

    // 予約詳細のモーダルを表示する関数
    function showReservationDetail(event) {
        // ここでモーダルを表示し、予約詳細を取得して表示する処理を実装する
        // モーダルの表示方法や詳細データの取得はプロジェクトに合わせて調整する
        $('#reservationModal').modal('show');
    }
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

document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'agendaWeek,agendaDay'
        },
        defaultView: 'agendaWeek',
        height: 'auto',
        allDaySlot: false,
        slotDuration: '00:30:00',
        slotLabelFormat: 'h:mm a',
        minTime: '08:00:00',
        maxTime: '18:00:00',
        weekends: false,
        editable: false,
        events: '/events', // Your endpoint to fetch events
        eventClick: function(info) {
            showReservationDetail(info.event);
        }
    });

    calendar.render();

    function showReservationDetail(event) {
        // Implement the logic to show reservation details using the 'event' object
        // Ensure that you have included jQuery before this script
        $('#reservationModal').modal('show');
    }
});


