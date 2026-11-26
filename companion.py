"""Open a problem and copy its Python solution from a local Markdown report."""
import argparse
import re
import subprocess
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from urllib.parse import urlsplit
import webbrowser


def read_solutions(path):
    heading = ""
    link = None
    code = None
    solutions = []
    seen = set()
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if code is not None:
            if line.strip() == "```":
                if code and link not in seen:
                    solutions.append((heading, link, "\n".join(code) + "\n"))
                    seen.add(link)
                code = None
            else:
                code.append(line)
            continue
        if line.startswith("## "):
            heading = line[3:].strip()
            link = None
        match = re.search(r"\]\((https://leetcode\.com/problems/[a-z0-9-]+/[^\s)]*)\)", line)
        if match:
            candidate = match[1]
            if re.fullmatch(r"/problems/[a-z0-9-]+/(?:description/)?",
                            urlsplit(candidate).path):
                link = candidate
        if heading and link and line.strip() in ("```python", "```python3", "```py"):
            code = []
    return solutions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", nargs="?", type=Path)
    parser.add_argument("--repo", type=Path, help="Local clone of your private report repo")
    args = parser.parse_args()

    root = tk.Tk()
    root.title("LeetCode Practice Companion")
    root.geometry("650x320")
    frame = ttk.Frame(root, padding=16)
    frame.pack(fill="both", expand=True)
    problems = ttk.Combobox(frame, state="readonly")
    problems.pack(fill="x", pady=10)
    status = tk.StringVar(value="Open a daily Markdown report to get started.")
    ttk.Label(frame, textvariable=status, wraplength=600).pack(fill="x")
    solutions = []

    def load(path):
        try:
            entries = read_solutions(path)
        except (OSError, UnicodeError) as exc:
            messagebox.showerror("Could not read report", str(exc))
            return
        solutions[:] = entries
        problems.configure(values=[title for title, _, _ in entries])
        if entries:
            problems.current(0)
        else:
            problems.set("")
        status.set(f"{path.name} | {len(entries)} Python solutions found.")

    def pick():
        filename = filedialog.askopenfilename(filetypes=[("Markdown reports", "*.md")])
        if filename:
            load(Path(filename))

    def latest():
        reports = sorted((args.repo / "reports").glob("????-??-??.md"))
        if reports:
            load(reports[-1])
        else:
            status.set("No dated Markdown reports found in the clone.")

    def sync():
        try:
            subprocess.run(["git", "-C", str(args.repo), "pull", "--ff-only"],
                           check=True, timeout=20, capture_output=True)
        except (OSError, subprocess.SubprocessError):
            messagebox.showerror("Sync unavailable",
                                 "Run git pull in your private clone and reopen the report.")
            return
        latest()

    def open_and_copy():
        index = problems.current()
        if index < 0:
            status.set("Open a report and select a problem first.")
            return
        _, url, code = solutions[index]
        root.clipboard_clear()
        root.clipboard_append(code)
        if webbrowser.open(url, new=2):
            status.set("Code copied. Paste it into the Python3 editor, review it, and click Submit.")
        else:
            status.set(f"Code copied. Open this problem manually: {url}")

    ttk.Button(frame, text="Open report", command=pick).pack(anchor="w", pady=4)
    if args.repo:
        ttk.Button(frame, text="Sync and open latest report", command=sync).pack(anchor="w", pady=4)
    ttk.Button(frame, text="Open problem and copy Python", command=open_and_copy).pack(anchor="w", pady=4)
    if args.report:
        load(args.report)
    elif args.repo:
        latest()
    root.mainloop()


if __name__ == "__main__":
    main()
