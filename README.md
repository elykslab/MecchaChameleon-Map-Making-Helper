# MecchaChameleon-Map-Making-Helper
After you use MecchaCModKit_Load in Unreal Engine 5.6.1 to build your map files use MCMMH.py to gather the AssetRegistry.bin, MecchaCModKit_Load-Windows(.pak , .ucas , .utoc), and MyItem.vdf into a single folder to upload with SteamCMD.

HowTo:
-   Put MCMMH.py right before the MecchaCModKit_Load folder, like this:
        <img width="634" height="247" alt="image" src="https://github.com/user-attachments/assets/c19f06e4-ac09-4384-a229-ed2a6e54e04b" />

-   To install required Python libraries run: pip install -r requirements.txt

-   If this is your first time running MCMMH in this directory, run 'python .\MCMMH.py' without arguments to generate config.json and mods.json

-   Usage: python MCMMH.py <plugin_name> <output_folder(no spaces)> <change_log_note(optional)>

    Example: python MCMMH.py SampleMyUGC MyFirstHouse This is my first mod

SteamCMD Auto-Upload Setup:
1.  Login to SteamCMD to cache your credentials
2.  Set 'auto_upload' in config.json to true
3.  Point 'steamcmd_path' in config.json to steamcmd.exe
4.  Set 'steam_username' in config.json to your login username for Steam
        - If the login starts failing you may have to login to SteamCMD manually to cache your credentials again
