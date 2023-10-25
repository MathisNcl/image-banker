import os
import shutil
import subprocess
import time

from seleniumbase import BaseCase


# @see: https://seleniumbase.io/help_docs/recorder_mode/
class PageContentTest(BaseCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app_process = subprocess.Popen(
            ["python", "-m", "streamlit", "run", "src/image_banker/app.py", "--server.headless", "True"],
            stdout=subprocess.PIPE,
        )
        time.sleep(5)
        # Check it started successfully
        assert not cls.app_process.poll(), cls.app_process.stdout.read().decode("utf-8")  # type: ignore

    def test_home_page(self) -> None:
        self.open("http://localhost:8501")
        time.sleep(8)

        self.assert_title("ImageBanker")

        # Assert the headers
        self.assert_text(
            "ImageBanker: Object Collector & Saver - Upload, select and collect your object to create a bank of images"
        )

        self.assert_text("Browse files")
        self.choose_file('input[data-testid="stDropzoneInput"]', "development/test_img.jpg")
        self.click('div[data-testid="stSelectbox"] > div > div > div')
        self.type('input[aria-label="Which object do you want to consider?"]', "1_mouse\n")
        self.click("div#root div div section div div:nth-of-type(10) button p")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.app_process.terminate()
        cls.app_process.wait()
        if os.path.isdir("downloaded_files"):
            shutil.rmtree("downloaded_files")
