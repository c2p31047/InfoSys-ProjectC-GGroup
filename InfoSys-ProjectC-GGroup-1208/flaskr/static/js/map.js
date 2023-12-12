let map;
let marker;
let user_id = null;
let markers = []; 

window.addEventListener('load', function() {
    fetch('/get_user_info')
        .then(response => response.json())
        .then(data => {
            if (data && data.user_id) {
                user_id = data.user_id;
                fetch('/get_user_locations')
                    .then(response => response.json())
                    .then(userLocations => {
                        userLocations.forEach(user => {
                            createMarker(user);
                        });
                    })
                    .catch(error => console.error('Error fetching user locations:', error));
            } else {
                console.log('Not logged in.');
            }
        })
        .catch(error => console.error('Error fetching user info:', error));
});

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 0, lng: 0 },
        zoom: 13
    });

    marker = new google.maps.Marker({
        map: map,
        position: { lat: 0, lng: 0 },
        title: '現在の位置',
        icon: 'static/img/custom-icon-self.png'
    });

    document.getElementById('getLocation').addEventListener('click', getLocation);

    setInterval(getLocation, 5000);
}

function getLocation() {
    if (user_id !== null) {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (position) {
                const location = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };

                marker.setPosition(location);
                map.setCenter(location);
                document.getElementById('locationText').textContent = `緯度: ${location.lat}, 経度: ${location.lng}`;
                sendLocationToServer(location.lat, location.lng);
            }, function (error) {
                handleLocationError(error);
            });
        } else {
            alert('ブラウザが位置情報をサポートしていません。');
        }
    } else {
        console.log('ユーザーがログインしていません。');
    }
}

function createMarker(user) {
    fetch(`/get_users/${user.user_id}`)
        .then(response => response.json())
        .then(userData => {
            const userName = userData.username;

            const userMarker = new google.maps.Marker({
                position: { lat: user.lat, lng: user.lng },
                map: map,
                icon: user.id === user_id ? 'static/img/custom-icon-self.png' : 'static/img/custom-icon-other.png'
            });

            const userNameDiv = document.createElement('div');
            userNameDiv.innerHTML = `<b>${userName}</b>`;

            const infowindow = new google.maps.InfoWindow({
                content: userNameDiv,
            });

            userMarker.addListener('click', () => {
                infowindow.open(map, userMarker);
            });

            markers.push(userMarker);
        })
        .catch(error => console.error('Error fetching user data:', error));
}

function sendLocationToServer(latitude, longitude) {
    fetch('/save_location', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            user_id: user_id,
            latitude: latitude,
            longitude: longitude,
        }),
    })
    .then(response => response.json())
    .catch(error => console.error('エラー:', error));
}

function handleLocationError(error) {
    console.error('位置情報の取得中にエラーが発生しました:', error.message);
}

// Google Maps APIの非同期読み込み
function loadScript() {
    const script = document.createElement('script');
    script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyCx2f7Bq73BOeoU6aihH77xKKxUo_a-a0U&callback=initMap';
    script.defer = true;
    document.head.appendChild(script);
}

window.addEventListener('load', loadScript);

// ログイン機能がある場合、ログイン時にユーザーIDを設定する
function loginUser(userID) {
    user_id = userID;
    getLocation();
}
