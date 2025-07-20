import tkinter as tk
from tkinter import ttk, messagebox
import os
import re
import subprocess

# ====== Config =======
GIT_BRANCH = "main"   # git branch name (adjust if your branch is different)
# git commit message template
COMMIT_MESSAGE_TEMPLATE = "Add solution {filename} and update README"

# ===== Difficulty and Tags options =======
DIFFICULTY_OPTIONS = ["Easy", "Medium", "Hard"]
TAGS_OPTIONS = [
    "Math", "Geometry", "DP", "Greedy", "Graphs",
    "Implementation", "Strings", "Data Structures",
    "Sorting", "Brute Force", "Constructive"
]

# ============ GUI and File creation =============

def create_cpp_file():
    problem_name = entry_problem_name.get().strip()
    difficulty = combo_difficulty.get()
    tags_selected = [listbox_tags.get(i) for i in listbox_tags.curselection()]

    if not problem_name:
        messagebox.showerror("Error", "Problem name cannot be empty!")
        return

    filename = problem_name
    if not filename.endswith(".cpp"):
        filename += ".cpp"

    metadata_lines = [
        f"// Language: C++\n",
        f"// Difficulty: {difficulty}\n",
        f"// Tags: {', '.join(tags_selected) if tags_selected else 'None'}\n\n"
    ]

    template_code = [
        "#include<iostream>\n",
        "using namespace std;\n\n",
        "int main() {\n",
        "    \n",
        "    return 0;\n",
        "}\n"
    ]

    if os.path.exists(filename):
        res = messagebox.askyesno("Overwrite?", f"'{filename}' already exists. Overwrite?")
        if not res:
            return

    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(metadata_lines + template_code)

    messagebox.showinfo("Success", f"File '{filename}' created successfully!")

    # Now run README generator and git commit+push
    generate_readme()
    git_commit_and_push(filename)

# ======== README generator ==============

def extract_problem_info(filename):
    match = re.match(r"(\d+[A-Z]*)_(.+)\.cpp", filename)
    if match:
        code = match.group(1)
        title = match.group(2).replace('_', ' ')
        contest_id = re.sub(r'[A-Z]$', '', code)
        problem_letter_match = re.findall(r'[A-Z]$', code)
        problem_letter = problem_letter_match[0] if problem_letter_match else ''
        link = f"https://codeforces.com/problemset/problem/{contest_id}/{problem_letter}"
        return {
            "code": code,
            "title": title,
            "link": link,
            "filename": filename
        }
    return None

def extract_metadata(filepath):
    metadata = {
        "language": "Unknown",
        "difficulty": "Unknown",
        "tags": "None"
    }
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for _ in range(5):
                line = file.readline()
                if "// Language:" in line:
                    metadata["language"] = line.split(":", 1)[1].strip()
                elif "// Difficulty:" in line:
                    metadata["difficulty"] = line.split(":", 1)[1].strip()
                elif "// Tags:" in line:
                    metadata["tags"] = line.split(":", 1)[1].strip()
    except:
        pass
    return metadata

def generate_readme():
    cpp_files = [f for f in os.listdir() if f.endswith(".cpp")]
    problems = []

    for file in sorted(cpp_files):
        info = extract_problem_info(file)
        if info:
            meta = extract_metadata(file)
            info.update(meta)
            problems.append(info)

    with open("README.md", "w", encoding='utf-8') as f:
        f.write("# 🧠 Codeforces Problem Solutions\n\n")
        f.write("This repository contains my solutions to Codeforces problems. Each solution includes a direct link to the original problem.\n\n")
        f.write("| Code | Title | Language | Difficulty | Tags | Link | File |\n")
        f.write("|------|-------|----------|------------|------|------|------|\n")
        for p in problems:
            f.write(f"| {p['code']} | {p['title']} | {p['language']} | {p['difficulty']} | {p['tags']} | [Link]({p['link']}) | [{p['filename']}]({p['filename']}) |\n")

    print("✅ README.md generated successfully!")

# ====== Git Commit & Push ===========

def git_commit_and_push(filename):
    try:
        subprocess.run(["git", "add", "."], check=True)
        commit_msg = COMMIT_MESSAGE_TEMPLATE.format(filename=filename)
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", GIT_BRANCH], check=True)
        messagebox.showinfo("Git Push", f"Git push successful!\nCommit message:\n{commit_msg}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Git Error", f"Git command failed:\n{e}")

# ===== GUI Setup ======

root = tk.Tk()
root.title("Create C++ File with Metadata & Auto Push")
root.geometry("400x450")
root.resizable(False, False)

tk.Label(root, text="Problem Name (e.g. 123A_Watermelon):").pack(pady=5)
entry_problem_name = tk.Entry(root, width=40)
entry_problem_name.pack()

tk.Label(root, text="Select Difficulty:").pack(pady=5)
combo_difficulty = ttk.Combobox(root, values=DIFFICULTY_OPTIONS, state="readonly")
combo_difficulty.current(0)
combo_difficulty.pack()

tk.Label(root, text="Select Tags (Ctrl+Click for multiple):").pack(pady=5)
listbox_tags = tk.Listbox(root, selectmode=tk.MULTIPLE, height=8)
for tag in TAGS_OPTIONS:
    listbox_tags.insert(tk.END, tag)
listbox_tags.pack()

btn_create = tk.Button(root, text="Create C++ File & Push to GitHub", command=create_cpp_file)
btn_create.pack(pady=20)

root.mainloop()
