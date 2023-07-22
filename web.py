from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import io
import torch
import numpy as np
import time

class SeleniumLoadPageNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "url": ("STRING",{"multiline": False}),
                "implicit_wait": ("INT",{"default": 5, "min": 0, "max": 60, "step": 1}),
            },
        }

    RETURN_TYPES = ("WEBPAGE",)
    FUNCTION = "load_page"

    CATEGORY = "Terrible Nodes/Web"

    def load_page(self, url, implicit_wait):
        if not url.startswith("http"):
            url = "https://" + url

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(implicit_wait)
        driver.get(url)
        time.sleep(3)
        return (driver,)

class SeleniumSetPageSizeNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "webpage": ("WEBPAGE",),
                "width": ("INT",{"default": 1024, "min": 8, "max": 4096, "step": 1}),
                "height": ("INT",{"default": 1024, "min": 8, "max": 4096, "step": 1}),
            },
        }

    RETURN_TYPES = ("WEBPAGE",)
    FUNCTION = "set_page_size"

    CATEGORY = "Terrible Nodes/Web"

    def set_page_size(self, webpage, width, height):
        driver = webpage
        driver.set_window_size(width, height)
        time.sleep(2)
        return (driver,)


class SeleniumWebpageToImageNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "webpage": ("WEBPAGE",),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "webpage_to_image"

    CATEGORY = "Terrible Nodes/Web"

    def webpage_to_image(self, webpage):
        driver = webpage
        png = driver.get_screenshot_as_png()
        image = Image.open(io.BytesIO(png))
        image_array = np.array(image).astype(np.float32)
        tensor = torch.from_numpy(image_array / 255.0)
        tensor = tensor.unsqueeze(0)
        return (tensor,)

WEB_NODE_CLASS_MAPPINGS = {
    "SeleniumLoadPageNode": SeleniumLoadPageNode,
    "SeleniumSetPageSizeNode": SeleniumSetPageSizeNode,
    "SeleniumWebpageToImageNode": SeleniumWebpageToImageNode,
}

WEB_NODE_DISPLAY_NAME_MAPPINGS = {
    "SeleniumLoadPageNode": "Load Webpage",
    "SeleniumSetPageSizeNode": "Set Webpage Size",
    "SeleniumWebpageToImageNode": "Webpage to Image",
}
