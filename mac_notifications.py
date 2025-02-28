import subprocess
from flask import Flask, request

app = Flask(__name__)

def show_applescript_dialog(title, message):
    """
    Displays a blocking AppleScript dialog in the center of the Mac screen
    with "Yes" and "No" buttons. Returns the clicked button as a string.
    """
    # This AppleScript displays a dialog with title at top, and the text in body,
    # plus Yes/No buttons (with Yes as the default).
    script = f'''
    display dialog "{message}" with title "{title}" buttons {{"No", "Yes"}} default button 2
    '''
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    output = result.stdout.strip()
    
    # If user clicked "Yes" or "No", the output will contain "button returned:Yes" or "button returned:No"
    if "Yes" in output:
        return "Yes"
    elif "No" in output:
        return "No"
    else:
        return ""

@app.route("/notify", methods=["POST"])
def notify():
    """
    An endpoint that receives a JSON payload:
    {
      "title": "some title",
      "message": "some message"
    }
    Then shows the AppleScript dialog and returns JSON like: {"clicked": "Yes"} or {"clicked": "No"}
    """
    data = request.json or {}
    title = data.get("title", "Notification")
    message = data.get("message", "You have a new event.")
    
    clicked = show_applescript_dialog(title, message)
    return {"clicked": clicked}

if __name__ == "__main__":
    # Run on port 5000 by default
    app.run(host="0.0.0.0", port=8000, debug=True)
