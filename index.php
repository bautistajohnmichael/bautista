<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Weather App</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to bottom, #83a4d4, #b6fbff);
            color: #333;
            text-align: center;
            padding-top: 100px;
            min-height: 100vh;
            margin: 0;
        }

        input, button {
            padding: 10px;
            margin: 5px;
            border: none;
            border-radius: 5px;
        }

        input {
            width: 200px;
        }

        button {
            background-color: #0077ff;
            color: white;
            cursor: pointer;
        }

        button:hover {
            background-color: #005fcc;
        }

        .weather {
            margin-top: 20px;
        }

        .weather-box {
            background: rgba(255, 255, 255, 0.8);
            padding: 20px;
            border-radius: 10px;
            max-width: 400px;
            margin: 20px auto;
        }
    </style>
</head>

<body>

    <h1>🌤️ Weather App (PHP)</h1>

    <form method="POST">
        <input
            type="text"
            name="city"
            placeholder="Enter city name"
            required
        >

        <button type="submit">Get Weather</button>
    </form>

    <div class="weather">

        <?php

        if ($_SERVER["REQUEST_METHOD"] === "POST") {

            $city = trim($_POST["city"]);

            // Your OpenWeatherMap API Key
            $apiKey = "9d100d06f26dd077742f36434fe6ad97";

            // Check if city is empty
            if (empty($city)) {

                echo '<div class="weather-box">';
                echo "<p>⚠️ Please enter a city name.</p>";
                echo "</div>";

            } elseif (empty($apiKey)) {

                echo '<div class="weather-box">';
                echo "<p>⚠️ API key is missing.</p>";
                echo "</div>";

            } elseif (!function_exists("curl_init")) {

                echo '<div class="weather-box">';
                echo "<p>❌ Error: cURL is not enabled on this server.</p>";
                echo "</div>";

            } else {

                // OpenWeatherMap API URL
                $url = "https://api.openweathermap.org/data/2.5/weather?q="
                    . urlencode($city)
                    . "&appid="
                    . urlencode($apiKey)
                    . "&units=metric";

                // Initialize cURL
                $ch = curl_init();

                curl_setopt($ch, CURLOPT_URL, $url);
                curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
                curl_setopt($ch, CURLOPT_TIMEOUT, 15);

                // Execute request
                $response = curl_exec($ch);

                // Get cURL error
                $curlError = curl_error($ch);

                // Get HTTP status code
                $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

                // Close cURL
                curl_close($ch);

                echo '<div class="weather-box">';

                // Check connection error
                if ($response === false) {

                    echo "<p>⚠️ Connection Error: "
                        . htmlspecialchars($curlError)
                        . "</p>";

                } else {

                    // Convert JSON response to PHP array
                    $data = json_decode($response, true);

                    // Check successful response
                    if ($httpCode === 200 && isset($data["main"])) {

                        echo "<h2>"
                            . htmlspecialchars($data["name"])
                            . ", "
                            . htmlspecialchars($data["sys"]["country"])
                            . "</h2>";

                        echo "<h3>"
                            . htmlspecialchars(
                                ucfirst($data["weather"][0]["description"])
                            )
                            . "</h3>";

                        echo "<p>🌡️ Temperature: "
                            . htmlspecialchars($data["main"]["temp"])
                            . "°C</p>";

                        echo "<p>💧 Humidity: "
                            . htmlspecialchars($data["main"]["humidity"])
                            . "%</p>";

                        echo "<p>💨 Wind: "
                            . htmlspecialchars($data["wind"]["speed"])
                            . " m/s</p>";

                    } else {

                        // API error message
                        $message = isset($data["message"])
                            ? $data["message"]
                            : "Unable to retrieve weather data.";

                        echo "<p>❌ Error: "
                            . htmlspecialchars(ucfirst($message))
                            . "</p>";

                        echo "<p>HTTP Status: "
                            . htmlspecialchars((string)$httpCode)
                            . "</p>";
                    }
                }

                echo "</div>";
            }
        }

        ?>

    </div>

</body>
</html>