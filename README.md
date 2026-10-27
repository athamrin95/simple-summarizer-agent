A simple summarizer agent using OpenRouter API.

Note:<br>
This project has been tested with Python 3.15<br>
Dependencies required can be found in the file "requirements.txt"<br>
Rename the file ".env.example" to ".env" and fill in OPENROUTER_API_KEY with your actual api key<br>
You may change the AI model with a different one that's available in OpenRouter by changing the value of OPENROUTER_MODEL

This script will summarize a given .txt file. The summary will be filled with 5 main bullet-points from the given .txt file (Could be less than 5 points if necessary, but it cannot/not allowed to exceed 5). The summary is written in Bahasa Indonesia and is written to a file called "ringkasan.md" in the same directory as the script. Currently the script will only summarize a .txt file with a maximum word count of 800 words.<br>
This current version of the script do not remember your previously sent messages (But it doesn't matter anyway since we are only making 1 api call to summarize 1 text file only).