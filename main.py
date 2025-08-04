import os
import json
import requests
from datetime import datetime, timedelta
from tkinter import Tk, Label, Button, StringVar, messagebox, simpledialog, font as tkFont
from ttkbootstrap import Style

# Load config
with open("config.json") as f:
    config = json.load(f)

GITHUB_TOKEN = config["github_token"]
GITHUB_REPO = config["github_repo"]
DEADLINE_HOURS = config["deadline_hours"]
LAST_WORDS = config["last_words"]

PAYLOAD_DIR = "payload"
FONT_PATH = "fonts/digital-7.ttf"

last_checkin = datetime.now()
triggered = False

def reset_timer():
    global last_checkin, triggered
    last_checkin = datetime.now()
    triggered = False
    log("Checked in at: " + last_checkin.isoformat())

def get_time_left():
    deadline = last_checkin + timedelta(hours=DEADLINE_HOURS)
    return deadline - datetime.now()

def countdown_loop():
    if not triggered:
        delta = get_time_left()
        if delta.total_seconds() <= 0:
            trigger_release()
        else:
            update_clock_display(delta)
    root.after(1000, countdown_loop)

def update_clock_display(delta):
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    clock_var.set(f"{hours:02}:{minutes:02}:{seconds:02}")

def trigger_release():
    global triggered
    if triggered:
        return
    triggered = True
    log("Triggering data release...")
    try:
        github_upload()
    except Exception as e:
        log(f"Upload failed: {e}")
        messagebox.showerror("Upload Failed", str(e))

def github_upload():
    now = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    branch = "main"
    api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/released/{now}/"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    for filename in os.listdir(PAYLOAD_DIR):
        file_path = os.path.join(PAYLOAD_DIR, filename)
        with open(file_path, "rb") as f:
            content = f.read()
        encoded = base64_encode(content)
        upload_url = api_url + filename
        data = {
            "message": f"Auto-release from dead man's switch at {now}",
            "content": encoded,
            "branch": branch
        }
        response = requests.put(upload_url, headers=headers, json=data)
        if not response.ok:
            raise Exception(f"GitHub upload failed for {filename}: {response.text}")
    # Add last words
    if LAST_WORDS:
        data = {
            "message": f"Auto-release last words at {now}",
            "content": base64_encode(LAST_WORDS.encode("utf-8")),
            "branch": branch
        }
        response = requests.put(api_url + "last_words.txt", headers=headers, json=data)
        if not response.ok:
            raise Exception("Failed to upload last words.")

    messagebox.showinfo("RELEASED", "Payload successfully uploaded to GitHub.")
    log("Upload complete.")

def base64_encode(content):
    import base64
    return base64.b64encode(content).decode("utf-8")

def nuke_now():
    global LAST_WORDS
    if messagebox.askyesno("Confirm", "Are you sure you want to NUKE it now?"):
        custom_msg = simpledialog.askstring("Last Words", "Enter a final message to attach:")
        if custom_msg:
            config["last_words"] = custom_msg
            LAST_WORDS = custom_msg
            with open("config.json", "w") as f:
                json.dump(config, f)
        trigger_release()

def log(msg):
    print("[*]", msg)

# === GUI Setup ===
root = Tk()
root.title("Dead Man's Switch")
style = Style("darkly")
root.geometry("420x250")
clock_var = StringVar()

# Load Digital-7 font
try:
    if os.path.exists(FONT_PATH):
        root.tk.call("font", "create", "Digital7", "-family", "Digital-7", "-size", "48")
        digital_font = tkFont.Font(name="Digital7", exists=True)
    else:
        raise FileNotFoundError("Font file not found.")
except Exception as e:
    print(f"[!] Font load failed: {e}")
    digital_font = ("Helvetica", 48)

clock_label = Label(
    root,
    textvariable=clock_var,
    font=digital_font,
    fg="#FFA500",
    bg="black"
)
clock_label.pack(pady=20, fill="x")

Button(root, text="✔ CHECK IN", command=reset_timer, width=20).pack(pady=5)
Button(root, text="☢ NUKE IT", command=nuke_now, width=20).pack(pady=5)

reset_timer()
countdown_loop()
root.mainloop()