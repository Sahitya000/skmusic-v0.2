const apiKey = 'AIzaSyAz3LnhWy_Ciz6I74NvUVfb3J4XSj8Jw_M'; // 🔁 Replace with your real YouTube API key
let myPlaylist = JSON.parse(localStorage.getItem('playlist')) || [];
let currentIndex = -1;

// Load saved playlist
renderPlaylist();

// Search songs using YouTube API
async function searchSongs() {
  const query = document.getElementById('searchInput').value;
  const response = await fetch(`https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=8&q=${query}&key=${apiKey}`);
  const data = await response.json();
  showResults(data.items);
}

function showResults(videos) {
  const grid = document.getElementById('songsGrid');
  grid.innerHTML = '';

  videos.forEach(video => {
    const videoId = video.id.videoId;
    const title = video.snippet.title;
    const thumb = video.snippet.thumbnails.medium.url;

    const card = document.createElement('div');
    card.className = 'song-card';
    card.innerHTML = `
      <img src="${thumb}" />
      <h4>${title}</h4>
    `;
    card.onclick = () => playSong(videoId, title, thumb);
    grid.appendChild(card);
  });
}

function playSong(videoId, title, thumb) {
  document.getElementById('currentTitle').innerText = title;
  document.getElementById('currentThumb').src = thumb;

  const audio = document.getElementById('audioPlayer');
  audio.src = `https://yt-mp3-api.vercel.app/play?videoId=${videoId}`;
  audio.play();

  const exists = myPlaylist.some(song => song.videoId === videoId);
  if (!exists) {
    myPlaylist.push({ videoId, title, thumb });
    localStorage.setItem('playlist', JSON.stringify(myPlaylist));
    renderPlaylist();
  }

  currentIndex = myPlaylist.findIndex(song => song.videoId === videoId);
}

function renderPlaylist() {
  const ul = document.getElementById('playlist');
  ul.innerHTML = '';

  myPlaylist.forEach((song, index) => {
    const li = document.createElement('li');
    li.innerText = song.title;
    li.onclick = () => {
      currentIndex = index;
      playSong(song.videoId, song.title, song.thumb);
    };
    ul.appendChild(li);
  });
}

function nextSong() {
  if (currentIndex < myPlaylist.length - 1) {
    const song = myPlaylist[++currentIndex];
    playSong(song.videoId, song.title, song.thumb);
  }
}

function prevSong() {
  if (currentIndex > 0) {
    const song = myPlaylist[--currentIndex];
    playSong(song.videoId, song.title, song.thumb);
  }
}

function rewind() {
  const audio = document.getElementById('audioPlayer');
  audio.currentTime = 0;
}

// Vertical swipe detection (up/down)
let touchStartY = 0;

document.addEventListener('touchstart', e => {
  touchStartY = e.changedTouches[0].screenY;
});

document.addEventListener('touchend', e => {
  const diffY = e.changedTouches[0].screenY - touchStartY;
  if (diffY < -50) {
    nextSong();
  } else if (diffY > 50) {
    prevSong();
  }
});
