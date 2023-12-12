// フォームがサブミットされたときに選択されたユーザーを取得
document.getElementById('startConversationForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const selectedUserId = document.getElementById('otherUser').value;

    // AJAXを使用して新しい会話を作成
    fetch('{{ url_for(create_conversation) }}', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        },
        body: JSON.stringify({ otherUserId: selectedUserId }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);  // 任意の応答を処理する（成功、失敗メッセージなど）
        // 会話ページにリダイレクトするか、任意のアクションを実行
        window.location.href = '{{ url_for(contact) }}';
    })
    .catch(error => {
        console.error('Error:', error);
    });
});