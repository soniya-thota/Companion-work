# LeetCode Practice Companion

A local Python desktop app for daily Markdown reports. Select a problem and the
app opens it in your default browser and copies the Python solution. Use your
existing LeetCode login, paste into the Python3 editor, review, and click Submit.

## Run on Windows

Install Python 3.10 or newer with Tkinter, then run:

    python companion.py

Choose Open report and select a downloaded Markdown report. To use a private
GitHub clone instead, authenticate Git with your usual credential manager and run:

    git clone https://github.com/YOUR-ACCOUNT/YOUR-PRIVATE-REPO.git
    python companion.py --repo PATH-TO-CLONE

The Sync button pulls updates without creating merge commits and loads the newest
dated report. The app reads Markdown under reports/YYYY-MM-DD.md. Each solution
needs a level-two heading, a Markdown link to the LeetCode problem, and a fenced
Python code block.

Only publish the app and its documentation. Keep reports and private clones
outside the public repository. The app never asks for LeetCode credentials.
Code is copied to your system clipboard and can be visible in clipboard history.
