const BOT_ICON = 'https://placehold.jp/30x30.png';
const MY_ICON = 'https://placehold.jp/50x50.png';
const API = 'http://localhost:8080';

function showBotMessage(message) {
  const chatWrapper = document.querySelector('.chat-wrapper');
  chatWrapper.insertAdjacentHTML('beforeend', `
    <div class="chat__message chat__message--received">
      <img src="${BOT_ICON}" alt="相手のアイコン">
      <div class="chat__message-text">
        ${message}
      </div>
    </div>
  `);
  chatWrapper.scrollTop = chatWrapper.scrollHeight;
}

function showMyMessage(message) {
  const chatWrapper = document.querySelector('.chat-wrapper');
  chatWrapper.insertAdjacentHTML('beforeend', `
    <div class="chat__message chat__message--sent">
      <div class="chat__message-text">
        ${message}
      </div>
      <img src="${MY_ICON}" alt="自分のアイコン">
    </div>
  `);
  chatWrapper.scrollTop = chatWrapper.scrollHeight;
}

const sendButton = document.querySelector('.input-wrapper button');
const input = document.querySelector('.input-wrapper input[type="text"]');

sendButton.addEventListener('click', () => {
  const message = input.value;
  showMyMessage(message);
  input.value = '';

  fetch(API + '/question', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      question: message,
    })
  })
  .then(response => response.text())
  .then(answer => {
    showBotMessage(answer);
  })

})

fetch(API + '/crawl', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    url: location.href,
  })
})
.then(() => {
  showBotMessage('こんにちは！');
})

