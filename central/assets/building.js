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
        loadBuildingReport()
    }, Number(refreshRateElement.value) * 1000);
}

function loadBuildingReport() {
    fetch('/api/buildings')
        .then(r => r.json())
        .then(data => {
            fillGeneralData(data);
            fillRoomsData(data.rooms)
        })
}

function fillGeneralData(generalData) {
    document.getElementById('general-temperature').textContent = `${generalData.temperature}ºC`;
    document.getElementById('general-humidity').textContent = `${generalData.humidity}%`;
    document.getElementById('general-persons').textContent = generalData.persons;
    document.getElementById('general-alarm-system').textContent = getOnOffText(generalData.alarm_system);
    document.getElementById('general-alarm').textContent = getOnOffText(generalData.alarm);

    const alarmContainer = document.getElementById('alarm-container');
    if (generalData.alarm) {
        alarmContainer.classList.add('alarm-animation');
    } else {
        alarmContainer.classList.remove('alarm-animation');
    }
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
    return `
        <div class="card-container text-center">
            <h1>${room.name} - (${room.online ? 'online' : 'offline'})</h1>
            <div class="card-elem-container">
                <div class="card-elem">
                    <div class="card-elem-title">Temperatura</div>
                    <img class="icon" src="icons/temperature.png">
                    <p>${room.temperature}ºC</p>
                </div>
                <div class="card-elem">
                    <div class="card-elem-title">Humidade</div>
                    <img class="icon" src="icons/humidity.png">
                    <p>${room.humidity}%</p>
                </div>
                <div class="card-elem">
                    <div class="card-elem-title">Pessoas</div>
                    <img class="icon" src="icons/persons.png">
                    <p>${room.persons}</p>
                </div>
                <div class="card-elem">
                    <div class="card-elem-title">Fumaça</div>
                    <img class="icon" src="icons/smoke.png">
                    <p>${getOnOffText(room.smoke)}</p>
                </div>
                <div class="card-elem">
                    <div class="card-elem-title">Projetor</div>
                    <img class="icon" src="icons/projector.png">
                    <p>${getOnOffText(room.projector)}</p>
                </div>
                <div class="card-elem">
                    <div class="card-elem-title">Ar-condicionado</div>
                    <img class="icon" src="icons/ice.png">
                    <p>${getOnOffText(room.air_conditioning)}</p>
                </div>
                <div class="card-elem">
                    <div class="card-elem-title">Presença</div>
                    <img class="icon" src="icons/presence.png">
                    <p>${getOnOffText(room.presence)}</p>
                </div>
                <div class="card-elem">
                    <div class="card-elem-title">Porta</div>
                    <img class="icon" src="icons/door.png">
                    <p>${getOnOffText(room.door)}</p>
                </div>
                <div class="card-elem">
                    <div class="card-elem-title">Janela</div>
                    <img class="icon" src="icons/window.png">
                    <p>${room.window ? 'Aberta' : 'Fechada'}</p>
                </div>
                <div class="card-elem">
                    <div class="card-elem-title">Lâmpada 01</div>
                    <img class="icon" src="icons/lamp.png">
                    <p>${getOnOffText(room.lamp01)}</p>
                </div>
                <div class="card-elem">
                    <div class="card-elem-title">Lâmpada 02</div>
                    <img class="icon" src="icons/lamp.png">
                    <p>${getOnOffText(room.lamp02)}</p>
                </div>
                <div class="card-elem">
                    <div class="card-elem-title ${room.alarm ? 'alarm-animation' : ''}">Alarme</div>
                    <img class="icon" src="icons/buzzer.png">
                    <p>${room.alarm}</p>
                </div>
            </div>
        </div>\n
    `
}

function getOnOffText(value) {
    return value ? 'Ligado' : 'Desligado';
}