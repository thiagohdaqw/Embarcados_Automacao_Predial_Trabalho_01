
function onAlarmSystemClick() {
    fetch('/api/buildings/alarm-system', {
        method: 'POST',
    })
    .then(r => r.json())
    .then(data => window.alert(data.message))
}

function turnOnLamps() {
    fetch('/api/buildings/lamps', {
        method: 'POST',
        body: JSON.stringify({
            value: true
        })
    })
    .then(r => r.json())
    .then(data => window.alert(data.message))
}

function turnOffRelays() {
    fetch('/api/buildings/relays', {
        method: 'POST',
        body: JSON.stringify({
            value: false
        })
    })
    .then(r => r.json())
    .then(data => window.alert(data.message))
}

function onToogleRelayClick(rooom_name, relay_name) {
    fetch('/api/rooms/relays/toggle', {
        method: 'POST',
        body: JSON.stringify({
            rooom_name,
            relay_name
        })
    })
    .then(r => r.json())
    .then(data => window.alert(data.message))
}