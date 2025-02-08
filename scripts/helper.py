import os
import datetime
from settings import model

# List of helper variables/ functions that is not a modifiable setting

repo_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../")

current_date = datetime.datetime.now().strftime("%Y-%m-%d")

archive_json = os.path.join(repo_dir, "archive", f"{current_date}.json")

is_r1 = "R1" in model
