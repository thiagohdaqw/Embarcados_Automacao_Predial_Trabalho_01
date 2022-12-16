
onAlarmSystemClick() {
    fetch('/api/building/alarm-system', {
        method: 'POST',
    })
    .then(r => r.json())
    .then(data => window.alert(data.message))
}
