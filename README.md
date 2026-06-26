# MecchaChameleon-Map-Making-Helper
After you use MecchaCModKit_Load to build your map use MCMMH.py to gather the AssetRegistry.bin, MecchaCModKit_Load-Windows(.pak , .ucas , .utoc), and MyItem.vdf into a single folder to upload with SteamCMD.

Usage:
1. If this is your first time running MCMMH in this directory, run 'python MCMMH.py' without arguments to generate config.json and mods.json
2.  Usage: python gather_files.py <plugin_name> <output_folder(no spaces)> <change_log_note(optional)>
    Example: python gather_files.py SampleMyUGC MyFirstHouse This is my first mod

SteamCMD Auto-Upload Setup:
1. Login to SteamCMD to cache your credentials
2. Set 'auto_upload' in config.json to true
3. Point 'steamcmd_path' in config.json to steamcmd.exe
4. Set 'steam_username' in config.json to your login username for Steam