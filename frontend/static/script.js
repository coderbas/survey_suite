 // Fetch survey statistics
 async function fetchSurveyStatistics() {
    try {
        const response = await fetch('http://localhost:5000/api/survey_stats');
        const data = await response.json();
        displaySurveyStats(data);
    } catch (error) {
        console.error('Error fetching survey statistics:', error);
    }
}

// Display survey statistics on the dashboard
function displaySurveyStats(surveyStats) {
    const container = document.getElementById('survey-container');
    // Update DOM with survey data
    surveyStats.forEach(stat => {
        // Create elements dynamically for each survey
        const surveyCard = document.createElement('div');
        surveyCard.className = 'survey-card';
        surveyCard.innerHTML = `
            <h4>${stat.title}</h4>
            <p>Responses: ${stat.response_count}</p>
        `;
        container.appendChild(surveyCard);
    });
}

// Initialize on page load
fetchSurveyStatistics();