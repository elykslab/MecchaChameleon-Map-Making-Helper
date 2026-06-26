import os
import shutil
import sys
import json
import subprocess
import math
from PIL import Image

sepNum = 110 # Number of "-" in console output separators

# Windows terminal colors
os.system("")
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

current_dir = os.getcwd()

#Load config.json
json_path = os.path.join(current_dir, "config.json")
if not os.path.exists(json_path):
    print("-" * sepNum)
    default_config = {
        "auto_upload": False,
        "steamcmd_path": "C:/SteamCMD/steamcmd.exe",
        "steam_username": "",
    }
    try:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)
        print(f"|  {GREEN}Created: config.json {YELLOW}({', '.join(default_config.keys())}){RESET}")
    except Exception as e:
        print(f"|  {RED}Error creating default config.json: {e}{RESET}")
        sys.exit(1)
try:
    with open(json_path, "r", encoding="utf-8") as f:
        config = json.load(f)
except Exception as e:
    print(f"|  {RED}Error reading config.json: {e}{RESET}")
    sys.exit(1)

upload = config.get("auto_upload", False)
username = config.get("steam_username")
steamcmd_path = config.get("steamcmd_path")

# Load mods.json
json_path = os.path.join(current_dir, "mods.json")
if not os.path.exists(json_path):
    with open(json_path, "w", encoding="utf-8") as f:
        f.write("{}")
    print(f"|  {GREEN}Created: mods.json {YELLOW}(Config settings for each mod, empty until you add a mod){RESET}")
try:
    with open(json_path, "r", encoding="utf-8") as f:
        mods_config = json.load(f)
except Exception as e:
    print(f"|  {RED}Error reading mods.json: {e}{RESET}")
    sys.exit(1)
print("-" * sepNum)

try:
    plugin_name = sys.argv[1]
    mod_key = sys.argv[2].lower()  # Convert input to lowercase to match JSON keys
except Exception as e:
    print(f"|  {CYAN}Usage: {YELLOW}python gather_files.py {GREEN}<plugin_name> {YELLOW}<output_folder(no spaces)> {GREEN}<change_log_note(optional)>{RESET}")
    print(f"|  {CYAN}Example: {YELLOW}python gather_files.py {GREEN}SampleMyUGC {YELLOW}MyFirstHouse {GREEN}This is my first mod{RESET}")
    print("-" * sepNum)
    sys.exit(1)
change_log = ' '.join(sys.argv[3::])

# 3. Check if the provided mod exists in our JSON configuration
if mod_key in mods_config:
    mod_data = mods_config[mod_key]
    published_file_id = mod_data["published_file_id"]
    workshop_title = mod_data["workshop_title"]
    workshop_description = mod_data["workshop_description"]
    visibility = mod_data["visibility"]
else:
    mods_config[mod_key] = {
        "published_file_id": "0",
        "workshop_title": f"{mod_key}",
        "workshop_description": f"{change_log}",
        "visibility": "2"
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(mods_config, f, indent=4)

    print("-" * sepNum)
    print(f"|  {GREEN}New mod added to mods.json: {mod_key}{RESET}")
    print(f"|  {YELLOW}Update the mod details in mods.json{RESET}")
    print(f"|  {YELLOW}- Leave the mod_name lowercase{RESET}")
    print(f"|  {YELLOW}- published_file_id is found in the Workshop URL for the mod{RESET}")
    print(f"|  {YELLOW}- workshop_title and workshop_description are what people see in the Workshop{RESET}")
    print(f"|  {YELLOW}- visibility: 0 = Public, 1 = Friends Only, 2 = Private, 3 = Unlisted{RESET}")
    print("-" * sepNum)
    sys.exit(1)

def upload_to_steamcmd(username, vdf_path):
    cmd = [ steamcmd_path, "+login", username ]
    cmd.extend(["+workshop_build_item", vdf_path])
    cmd.append("+quit")

    try:
        print(f"{CYAN}Uploading to Steam Workshop...")
        result = subprocess.run(cmd, check=True, text=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"SteamCMD failed with exit code {e.returncode}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

# Base paths setup
files = [
    os.path.join(current_dir, "MecchaCModKit_Load", "Plugins", plugin_name, "Saved", "Cooked", "Windows", "MecchaCModKit_Load", "Plugins", plugin_name, "AssetRegistry.bin"),
    os.path.join(current_dir, "MecchaCModKit_Load", "Plugins", plugin_name, "Saved", "StagedBuilds", "Windows", "MecchaCModKit_Load", "Plugins", plugin_name, "Content", "Paks", "Windows", f"{plugin_name}MecchaCModKit_Load-Windows.pak"),
    os.path.join(current_dir, "MecchaCModKit_Load", "Plugins", plugin_name, "Saved", "StagedBuilds", "Windows", "MecchaCModKit_Load", "Plugins", plugin_name, "Content", "Paks", "Windows", f"{plugin_name}MecchaCModKit_Load-Windows.ucas"),
    os.path.join(current_dir, "MecchaCModKit_Load", "Plugins", plugin_name, "Saved", "StagedBuilds", "Windows", "MecchaCModKit_Load", "Plugins", plugin_name, "Content", "Paks", "Windows", f"{plugin_name}MecchaCModKit_Load-Windows.utoc"),
]

# Destination directory based on the CLI input string
dest_dir = os.path.join(current_dir, "SteamWorkshop", mod_key)

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

print("-" * sepNum)
modkit_found = True

for file in files:
    if os.path.exists(file):
        shutil.copy(file, dest_dir)
        print(f"|  {GREEN}Copied: {os.path.basename(file)}{RESET}")
    else:
        modkit_found = False
if modkit_found == False:
    print(f"|  {RED}MecchaCModKit_Load files not found in '{current_dir}'{RESET}")
    print("-" * sepNum)
    sys.exit(1)

print("-" * sepNum)
print(f"|  {CYAN}Gathering files for mod '{mod_key}' in '{dest_dir}'{RESET}")
print(f"|  {CYAN}Change Log: '{change_log}'{RESET}")

# 2. Generate the MyItem.vdf file directly in the destination folder
vdf_content_folder = dest_dir.replace("/", "\\")
preview_image = os.path.join(dest_dir, "Preview.png").replace("/", "\\")

vdf_template = f""""workshopitem"
{{
    "appid"        "4704690"
    "publishedfileid"        "{published_file_id}"
    "contentfolder"        "{vdf_content_folder}"
    "previewfile"        "{preview_image}"
    "visibility"        "{visibility}"
    "title"        "{workshop_title}"
    "description"        "{workshop_description}"
    "changenote"        "{change_log}"
}}"""

vdf_output_path = os.path.join(dest_dir, "MyItem.vdf")

try:
    with open(vdf_output_path, "w", encoding="utf-8") as vdf_file:
        vdf_file.write(vdf_template)
    print(f"|  {GREEN}Generated: {os.path.basename(vdf_output_path)}{RESET}")
except Exception as e:
    print(f"|  {RED}Error generating MyItem.vdf: {e}{RESET}")

preview_check = True
preview_size_check = True

if not os.path.exists(os.path.join(dest_dir, "Preview.png")):
    preview_check = False
    print(f"|  {YELLOW}You will need to put a Preview.png in '{dest_dir}'{RESET}")
    print(f"|  {YELLOW}- Must be under 1MB{RESET}")
    print(f"|  {YELLOW}- 1:1 Aspect Ratio highly recommended or Steam will shrink it to fit in a 1:1{RESET}")
elif os.path.getsize(os.path.join(dest_dir, "Preview.png")) > 1024 * 1024:
    preview_size_check = False
    print(f"|  {RED}Preview.png is over 1MB{RESET}")
    print(f"|  {YELLOW}- Must be under 1MB{RESET}")
    print(f"|  {YELLOW}- 1:1 Aspect Ratio highly recommended or Steam will shrink it to fit in a 1:1{RESET}")
else:
    img = Image.open(os.path.join(dest_dir, "Preview.png"))
    divisor = math.gcd(img.width, img.height)
    ratio_width = img.width // divisor
    ratio_height = img.height // divisor

    print(f"|  {GREEN}Found: Preview.png{RESET}")
    print(f"|  {GREEN}- Size: {os.path.getsize(os.path.join(dest_dir, 'Preview.png')) / 1024 / 1024:.2f} MB{RESET}")
    if ratio_width == ratio_height:
        print(f"|  {GREEN}- Aspect Ratio: {ratio_width}:{ratio_height}{RESET}")
    else:
        print(f"|  {YELLOW}- Aspect Ratio: {ratio_width}:{ratio_height} (This will upload, but Steam will shrink it to fit in a 1:1){RESET}")

print("-" * sepNum)
print(f"|  {CYAN}SteamCMD Upload Command:{RESET}")
print(f"|  {YELLOW}workshop_build_item \"{vdf_output_path}\"{RESET}")
print("-" * sepNum)

if upload == True:
    if preview_check == False:
        print(f"{RESET}|  {RED}Skipping upload... {YELLOW}(Missing Preview.png){RESET}")
    elif preview_size_check == False:
        print(f"{RESET}|  {RED}Skipping upload... {YELLOW}(Preview.png is over 1MB){RESET}")
    elif len(username) == 0:
        print(f"{RESET}|  {RED}Skipping upload... {YELLOW}(Missing steam_username in config.json){RESET}")
    elif os.path.exists(steamcmd_path) == False:
        print(f"{RESET}|  {RED}Skipping upload... {YELLOW}(steamcmd.exe not found at steamcmd_path set in config.json){RESET}")
    else:
        success = upload_to_steamcmd("Cripticlord", vdf_output_path)
        if success:
            print(f"{RESET}|  {GREEN}Upload successful!{RESET}")
        else:
            print(f"{RESET}|  {RED}Upload failed!{RESET}")
else:
    print(f"{RESET}|  {RED}Skipping upload... {YELLOW}(auto_upload disabled in config.json){RESET}")
print("-" * sepNum)