import json
import requests

class OneDriveClient:
    def __init__(self, cookies_path="cookies.json"):
        with open(cookies_path, "r") as f:
            self.cookies = json.load(f)

        self.session = requests.Session()
        self.session.cookies.update(self.cookies)

    def download_file(self, download_url, save_path):
        """
        download_url example:
        https://onedrive.live.com/download?resid=XXXX
        """
        response = self.session.get(download_url)

        if response.status_code != 200:
            raise Exception("Failed to download file. Cookies may be expired.")

        with open(save_path, "wb") as f:
            f.write(response.content)

        return save_path
