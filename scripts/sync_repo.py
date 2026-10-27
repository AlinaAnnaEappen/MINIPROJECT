import os
import shutil

source_dir = r"c:\Users\alina\OneDrive\Desktop\SHE"
cloned_dir = os.path.join(source_dir, "cloned_repo")
legacy_dir = os.path.join(cloned_dir, "legacy_prototype")

os.makedirs(legacy_dir, exist_ok=True)

legacy_files = [
    "aboutus new.html", "aboutus.html", "advisory new.html", "advisory.html",
    "contact new.html", "contact.html", "feedback new.html", "feedback.html",
    "frontent.html  new.html", "frontent.html.html", "dataset", "datasetup.py",
    "dtaset.py", "fetch_features.py", "get_coordinates.py", "model_training.py",
    "predict_safety.py", "logo.png", "hero.png"
]

for lf in legacy_files:
    src = os.path.join(cloned_dir, lf)
    if os.path.exists(src):
        dest = os.path.join(legacy_dir, lf)
        shutil.move(src, dest)
        print(f"Archived legacy file: {lf}")

with open(os.path.join(legacy_dir, "README.md"), "w", encoding="utf-8") as f:
    f.write("# Original Prototype Archive\n\nThis directory contains the initial college mini-project prototype files, preserved for academic history.\n")

files_to_copy = [
    "app.py", "requirements.txt", "README.md", "PROJECT_REFERENCE_REPORT.md",
    "DATASET_DOCUMENTATION.md", "COLLEGE_VIVA_GUIDE.md", ".gitignore"
]

for f in files_to_copy:
    src = os.path.join(source_dir, f)
    dst = os.path.join(cloned_dir, f)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"Copied file: {f}")

dirs_to_copy = ["data", "models", "services", "templates", "static", "tests", "scripts"]
for d in dirs_to_copy:
    src = os.path.join(source_dir, d)
    dst = os.path.join(cloned_dir, d)
    if os.path.exists(src):
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        print(f"Copied directory: {d}")

print("Repository sync complete!")
