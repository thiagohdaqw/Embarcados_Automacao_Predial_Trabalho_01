
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

function onToogleRelayClick(rooom_name, sensor_name) {
    fetch('/api/rooms/relay/toggle', {
        method: 'POST',
        body: JSON.stringify({
            rooom_name,
            sensor_name
        })
    })
    .then(r => r.json())
    .then(data => window.alert(data.message))
}