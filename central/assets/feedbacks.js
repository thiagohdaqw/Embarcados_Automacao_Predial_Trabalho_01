feedbacks = [];


function clearFeedbacks() {
    feedbacks = [];
    renderFeedbacks(0);
}

function renderFeedbacks(new_count) {
    container = document.getElementById('notifications');
    container.innerHTML = feedbacks.reverse().reduce((html, feedback, index) => html + `
        <div class="notification ${index < new_count ? 'notification-animation' : ''}">
            ${feedback}
        </div>
    `, '');
}

function addFeedbacks(new_feedbacks) {
    feedbacks = feedbacks.slice(feedbacks.length-10, feedbacks.length);
    feedbacks.push(...new_feedbacks);

    renderFeedbacks(new_feedbacks.length);
}