Dead Man's Switch GUI (Local Version)
======================================

This application is a local dead man's switch. If you fail to check in before the countdown ends,
it will automatically upload your payload data to the configured GitHub repository.

--------------------------------------
📂 Folder Structure:
--------------------------------------
/assets/         -> Holds UI icon images (radiation_icon.png, add_icon.png)
/fonts/          -> Holds the Digital-7 font (digital-7.ttf)
/payload/        -> Drop any files you want released if triggered
/triggered/      -> Output files when countdown expires
config.json      -> Your GitHub token and repository info
main.py          -> Main program file

--------------------------------------
📌 Required Files:
--------------------------------------
assets/radiation_icon.png   -> Icon for NUKE IT button
assets/add_icon.png         -> Orange plus icon for "+ Add File" button
fonts/digital-7.ttf         -> Clock font
config.json                 -> Contains:
{
  "github_token": "your_token_here",
  "repo": "username/repository",
  "deadline_hours": 24,
  "last_words": "final message here"
}

--------------------------------------
🛠️ How to Run (Windows):
--------------------------------------
1. Install Python: https://www.python.org/downloads/
2. Install dependencies (from CMD):
   pip install -r requirements.txt
   (Or manually: `pip install tk requests`)

3. Run the app:
   python main.py

--------------------------------------
❗ Notes:
--------------------------------------
- All folders contain a .keep file to stay visible.
- The "+" button allows you to select files and adds them to /payload/
- The NUKE IT button uploads the payload immediately.
- Files are uploaded to your GitHub repo on trigger or manual execution.

Stay safe.

Can also run as EXE!! exe is more polished 
