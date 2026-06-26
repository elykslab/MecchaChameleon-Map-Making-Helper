# MecchaChameleon-Map-Making-Helper
After you use MecchaCModKit_Load in Unreal Engine 5.6.1 to build your map files use MCMMH.py to gather the AssetRegistry.bin, MecchaCModKit_Load-Windows(.pak , .ucas , .utoc), and MyItem.vdf into a single folder to upload with SteamCMD.

Usage:
-   If this is your first time running MCMMH in this directory, run 'python MCMMH.py' without arguments to generate config.json and mods.json
-   Usage: python gather_files.py <plugin_name> <output_folder(no spaces)> <change_log_note(optional)>
    Example: python gather_files.py SampleMyUGC MyFirstHouse This is my first mod

SteamCMD Auto-Upload Setup:
1.  Login to SteamCMD to cache your credentials
2.  Set 'auto_upload' in config.json to true
3.  Point 'steamcmd_path' in config.json to steamcmd.exe
4.  Set 'steam_username' in config.json to your login username for Steam
        - If the login starts failing you may have to login to SteamCMD manually to cache your credentials again