const $ = document.querySelector.bind(document),
      $control = $('#chat'),
      $status = $('#status'),
      $connect = $('#connect');

let conn = null;

const showMessage = msg => {
    $control.innerHTML = $control.innerHTML + msg + '<br/>';
    $control.scrollTop = $control.scrollTop + 1000;
}

const processData = ({type, data}) => {
  switch (type) {
    case 'join':
      showMessage(`[${data}] joined`)
      break;

    case 'disconnect':
      showMessage(`[${data}] disconnect`)
      break;

    case 'msg':
      showMessage(`${new Date(data.created).toLocaleString()} [${data.user && data.user.email || 'anonymous'}] said: ${data.content}`);
      break;
  }
}

const updateUI = () => {
    if (conn == null) {
        $status.innerHTML = 'disconnected';
        $connect.innerHTML = 'Connect';
        $connect.classList.remove('btn-danger')
        $connect.classList.add('btn-success')
    } else {
        $status.innerHTML = 'connected (' + conn.url + ')';
        $connect.innerHTML = 'Disconnect';
        $connect.classList.remove('btn-success')
        $connect.classList.add('btn-danger')
    }
}

const connect = () => {
    disconnect();
    var wsUri = (globalThis.location.protocol=='https:'&&'wss://'||'ws://')+globalThis.location.host+'/ws';
    conn = new WebSocket(wsUri);
    showMessage('Connecting...');

    conn.onopen = function() {
        showMessage('Connected.');
        updateUI();
    };
    conn.onmessage = function(e) {
      e.data.text().then(str => {
        processData(JSON.parse(str));
      })
    };
    conn.onclose = function() {
        showMessage('Disconnected.');
        conn = null;
        updateUI();
    };
}

const disconnect = () => {
    if (conn != null) {
        showMessage('Disconnecting...');
        conn.close();
        conn = null;
        updateUI();
    }
}

$connect.addEventListener('click', function () {
    if (conn == null) {
        connect();
    } else {
        disconnect();
    }
    return updateUI();
})

$('#send').addEventListener('click', function () {
    var text = $('#text').value;
    fetch('/api/messages', {
        method: 'POST',
        headers: {'content-type': 'application/json'},
        body: JSON.stringify({'content': text}),
    })
    $('#text').value = ''
    $('#text').focus()
    return false;
});

$('#text').addEventListener('keyup', function (e) {
    if (e.keyCode === 13) {
        $('#send').click();
        return false;
    }
})

fetch('/api/messages')
  .then( response => response.json() )
  .then( data => {
      data.forEach(m => {
          showMessage(`${new Date(m.created).toLocaleString()} [${m.user && m.user.email || 'anonymous'}] said: ${m.content}`);
      });
      connect();
});
