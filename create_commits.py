import os
import subprocess
from datetime import datetime

# Your commit history timeline
commits = [
    ("2025-10-18 12:00:00", "initial commit"),
    ("2025-10-18 13:15:00", "Set up Django project and initial app structure"),
    ("2025-10-19 15:30:00", "Implemented employee list"),
    ("2025-10-20 11:45:00", "Added employee registration and update forms"),
    ("2025-10-20 14:10:00", "authentication for frontend"),
    ("2025-10-22 16:25:00", "Enhanced UI with real-time updates and validation"),
    ("2025-10-30 19:00:00", "Fixed layout issues and optimized API calls"),
]
# --- Author Information ---
AUTHOR_NAME = "Ashwinkumar Sethi"
AUTHOR_EMAIL = "ashwinkumarsethi2223@ternaengg.ac.in"
PUSH_AFTER = True


def run_command(cmd):
    """Run shell command and print output."""
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)

def simulate_real_file_edit(date, message):
    """Simulate realistic Django frontend code edits based on 'employee' app structure."""
    message_lower = message.lower()

    # --- MODIFIED SECTION ---
    # Match commits to Django 'employee' app files from the image
    if "url" in message_lower:
        file_to_edit = "employee/urls.py"
    elif "auth" in message_lower or "session" in message_lower:
        file_to_edit = "employee/views.py"  # Auth logic in views
    elif "api" in message_lower:
        file_to_edit = "employee/views.py"  # API logic in views
    elif "view" in message_lower or "logic" in message_lower:
        file_to_edit = "employee/views.py"
    elif "template" in message_lower or "dashboard" in message_lower:
        # Use list.html as the dashboard, matching the image path
        file_to_edit = "employee/templates/list.html" 
    else:
        file_to_edit = "commit_log.txt"
    # --- END MODIFIED SECTION ---

    # Ensure directory exists if it's a nested path
    if "/" in file_to_edit:
        os.makedirs(os.path.dirname(file_to_edit), exist_ok=True)

    # Append simulated code changes
    with open(file_to_edit, "a", encoding="utf-8") as f:
        f.write(f"\n# Commit on {date}: {message}\n")

    print(f"Edited file: {file_to_edit}")


# --- Create commits sequentially ---
for date, message in commits:
    print(f"\n--- Creating commit for {date}: {message} ---")
    simulate_real_file_edit(date, message)

    # Stage changes
    run_command("git add .")

    # Commit with backdated timestamp
    env = os.environ.copy()
    env["GIT_COMMITTER_DATE"] = date
    env["GIT_AUTHOR_DATE"] = date
    cmd = f'git commit -m "{message}" --author="{AUTHOR_NAME} <{AUTHOR_EMAIL}>"'
    subprocess.run(cmd, shell=True, env=env)

# --- Push all commits to remote ---
if PUSH_AFTER:
    print("\nPushing all commits to GitHub...")
    run_command("git push origin main")