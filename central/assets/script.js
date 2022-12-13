document.getElementById('central-server-header').innerText += ` (${window.location.host})`

refreshRateElement = document.getElementById('refresh-rate-input')

reportPollingInterval = null;

runReportPolling();

function setRefreshRate(value) {
    refreshRateElement.value = value;
    runReportPolling();
}

function runReportPolling() {
    if (reportPollingInterval) {
        clearInterval(reportPollingInterval)
    }

    reportPollingInterval = setInterval(() => {
        loadReport()
    }, Number(refreshRateElement.value) * 1000);
}

function loadReport() {
    fetch('http://localhost:10720/api/reports')
        .then(r => r.json())
        .then(data => {
            fillGeneralData(data.general);
            fillRoomsData(data.rooms)
        })
}

function fillGeneralData(generalData) {
    document.getElementById('general-temperature').textContent = `${generalData.temperature}ºC`;
    document.getElementById('general-alarm-system').textContent = getOnOffText(generalData.alarmSystem);
}

function fillRoomsData(roomsData) {
    const rooms = document.getElementById('rooms');

    roomsData.sort(roomsComparator);

    rooms.innerHTML = roomsData
        .reduce((html, room) => html + getRoomHtml(room), "");
}

function roomsComparator(a, b) {
    if (a.online === b.online) {
        return a.name.localeCompare(b.name);
    }
    return b.online - a.online;
}

function getRoomHtml(room) {
    console.log(room);
    return `
        <div class="card-container text-center">
            <h1>${room.name}</h1>
            <div class="card-elem-container">
                <div class="card-elem">
                    <img class="icon" src="temperature.png">
                    <p>${room.online ? 'Online' : 'Offline'}</p>
                </div>
                <div class="card-elem">
                    <img class="icon" src="temperature.png">
                    <p>${room.temperature}ºC</p>
                </div>
                <div class="card-elem">
                    <img class="icon" src="alarm.png">
                    <p>${room.persons}</p>
                </div>
                <div class="card-elem">
                    <img class="icon" src="alarm.png">
                    <p>${getOnOffText(room.smoke)}</p>
                </div>
                <div class="card-elem">
                    <img class="icon" src="alarm.png">
                    <p>${getOnOffText(room.projector)}</p>
                </div>
                <div class="card-elem">
                    <img class="icon" src="alarm.png">
                    <p>${getOnOffText(room.airConditioning)}</p>
                </div>
                <div class="card-elem">
                    <img class="icon" src="alarm.png">
                    <p>${getOnOffText(room.presence)}</p>
                </div>
                <div class="card-elem">
                    <img class="icon" src="alarm.png">
                    <p>${getOnOffText(room.window)}</p>
                </div>
                <div class="card-elem">
                    <img class="icon" src="alarm.png">
                    <p>${getOnOffText(room.lamp01)}</p>
                </div>
                <div class="card-elem">
                    <img class="icon" src="alarm.png">
                    <p>${getOnOffText(room.lamp02)}</p>
                </div>
            </div>
        </div>\n
    `
}

function getOnOffText(value) {
    return value ? 'Ligado' : 'Desligado';
}