
function onAlarmSystemClick() {
    fetch('/api/buildings/alarm-system', {
        method: 'POST',
    })
    .then(r => r.json())
    .then(data => addFeedbacks([data.message]))
}

function turnOnLamps() {
    fetch('/api/buildings/lamps', {
        method: 'POST',
        body: JSON.stringify({
            value: true
        })
    })
    .then(r => r.json())
    .then(data => addFeedbacks([data.message]))
}

function turnOffRelays() {
    fetch('/api/buildings/relays', {
        method: 'POST',
        body: JSON.stringify({
            value: false
        })
    })
    .then(r => r.json())
    .then(data => addFeedbacks([data.message]))
}

function toggleRelay(online, rooom_name, relay_name) {
    if (!online) {
        return;
    }

    fetch('/api/rooms/relays', {
        method: 'POST',
        body: JSON.stringify({
            rooom_name,
            relay_name
        })
    })
    .then(r => r.json())
    .then(data => addFeedbacks([data.message]))
}