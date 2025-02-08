import os
import datetime

repo_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../")

current_date = datetime.datetime.now().strftime("%Y-%m-%d")

archive_json = os.path.join(repo_dir, "history", f"{current_date}.json")
