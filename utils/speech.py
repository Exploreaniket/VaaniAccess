import streamlit.components.v1 as components
import json


def speak_hindi(text):
    """
    Display a browser-based Hindi speech button.

    The button lives inside the HTML component itself,
    so clicking it does not trigger a Streamlit rerun.
    """

    safe_text = json.dumps(text, ensure_ascii=False)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">

        <style>
            body {{
                margin: 0;
                padding: 0;
                background: transparent;
                font-family: Arial, sans-serif;
            }}

            button {{
                background: #1f77b4;
                color: white;
                border: none;
                padding: 10px 18px;
                border-radius: 8px;
                font-size: 15px;
                cursor: pointer;
            }}

            button:hover {{
                opacity: 0.9;
            }}

            #status {{
                margin-left: 10px;
                font-size: 14px;
                color: #888;
            }}
        </style>
    </head>

    <body>

        <button id="speakButton">
            🔊 Listen in Hindi
        </button>

        <span id="status"></span>

        <script>

            const text = {safe_text};

            const button = document.getElementById("speakButton");
            const status = document.getElementById("status");

            button.addEventListener("click", function() {{

                // Stop previous speech
                window.speechSynthesis.cancel();

                const speech = new SpeechSynthesisUtterance(text);

                speech.lang = "hi-IN";
                speech.rate = 0.9;
                speech.pitch = 1.0;
                speech.volume = 1.0;

                speech.onstart = function() {{
                    status.innerText = "🔊 Speaking...";
                }};

                speech.onend = function() {{
                    status.innerText = "✓ Finished";
                }};

                speech.onerror = function() {{
                    status.innerText = "⚠️ Speech unavailable";
                }};

                window.speechSynthesis.speak(speech);
            }});

        </script>

    </body>
    </html>
    """

    components.html(html, height=55)