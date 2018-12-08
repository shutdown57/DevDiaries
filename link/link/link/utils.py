import os
import requests
from werkzeug.utils import secure_filename

from common.utils import allowed_file
from config import Config


CALLBACK = 'https://link.devdiaries.xyz/links/call_back?image_id='
API_CALL_STATUS_ERROR = 'error'
API_CALL_STATUS_PROCESSING = 'processing'
API_CALL_STATUS_FIHISHED = 'finished'


def make_img(p2i_url: str, link_id: str) -> None:
    """
    Make image screenshut
    :param p2i_url str: Website url to make screenshut
    :param name str: Website name
    :param link_id int: Link id object to store image url
    """
    p2i = {
        'p2i_url': p2i_url,
        'p2i_key': os.environ.get('P2I_KEY', ''),
        'p2i_device': 6,
        'p2i_fullpage': 1,
        'p2i_imageformat': 'jpg',
        'p2i_size': '600x0',
        'p2i_callback': CALLBACK + link_id,
        'p2i_screen': '1024x768'
    }

    request_url = 'http://api.page2images.com/restfullink'
    request_img(request_url, p2i)


def request_img(request_url: str, params: dict) -> dict:
    """
    Get request to p2i api to make screenshut
    :param request_url str: Website we want to make screenshut
    :param params dict: Configuration to make screenshut
    :return: Response of p2i api
    """
    try:
        requests.get(request_url, params=params)
    except Exception as e:
        print(f"Error in [get image url]: {e}")
        raise # TODO enter exception class


def write_img(img_url: str) -> str:
    """
    Download and write image to disk
    :param img_url str: The image url of screenshut
    :param img_name str: Name of file
    """
    img_name = '-'.join(img_url.split('/')[-1])
    #  img_url = 'http://api.page2images.com/ccimages/cf/77/tE2byaNynW4mGgQ2.jpg'
    if not img_url:
        print("Image url required")
        raise # TODO enter exception class
    try:
        img_file = requests.get(img_url).content
    except Exception as e:
        print(f"Error in [get image url]: {e}")
        raise # TODO enter exception class
    if img_file and allowed_file(img_name):
        img_name = secure_filename(img_name)
        with open(Config.UPLOAD_FOLDER + '/' + img_name, 'wb') as image:
            image.write(img_file)
        return Config.UPLOAD_FOLDER + '/' + img_name
