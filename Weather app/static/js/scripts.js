document.getElementById('weather-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // Clear previous results
    document.getElementById('weather-result').innerHTML = '';
    document.getElementById('error-message').style.display = 'none';

    // Get the location input
    const location = document.getElementById('location').value;

    // Send AJAX request to Flask server
    fetch('/weather', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'location': location
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            // Display error message
            document.getElementById('error-message').innerText = data.error;
            document.getElementById('error-message').style.display = 'block';
        } else {
            // Display weather data
            const weatherHtml = `
                <h1 class="text-center">Weather in ${data.location}</h1>
                <div class="text-center">
                    <img src="http://openweathermap.org/img/wn/${data.icon}@2x.png" alt="Weather Icon">
                    <h2>${data.temperature}°C</h2>
                    <p>${data.description}</p>
                    <p>Wind Speed: ${data.wind_speed} m/s</p>
                </div>
            `;
            document.getElementById('weather-result').innerHTML = weatherHtml;
        }
    })
    .catch(error => {
        // Display error message
        document.getElementById('error-message').innerText = 'An error occurred: ' + error.message;
        document.getElementById('error-message').style.display = 'block';
    });
});
