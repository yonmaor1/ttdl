# Save all your TikToks before the goberment takes them away
This repo currently supports saving all your Favorited (saved) posts to your local harddrive.

## Quickstart
- You must have chrome and python installed
- Open a terminal and `cd` somewhere comfortable
- Clone this repo:
    - if you have git installed (reccomended)
        ```
        git clone https://github.com/yonmaor1/ttdl.git
        cd ttdl
        ```
    - if you don't have git installed, save this as a zip and unzip it somewhere, then `cd path\to\ttdl`
- create and launch a virtual enviorment:
    ```
    python -m venv venv
    venv/bin/activate
    ``` 
- install the requirements:
    ```
    pip install -r requirements.txt
    ```
- you are now ready to run the script


## Save your Favorited (saved) videos: ttdl-faves.py
```
Usage:
    python ttdl-faves.py -u <username> -o <output_directory>

Arguments:
    -u, --handle: The handle of the user whos favorites you want to save.
    -o, --output: The output directory to save the TikToks to (optional, defaults 'out')
```

This script will launch a chrome tab and attempt to fetch your saved videos. You will at one point need to sign into your tiktok account. Other then that, you don't need to (nor should you), touch the chrome tab. It will close on its own once its done.
