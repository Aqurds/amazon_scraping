import requests as rq
import random as rn
# import db function from db_op file
from db_conn import store_asin_picture



def save_keepa_image(asin_list):

    random_integer = rn.randint(0, 10000000000)
    asin_name = asin_list[0]
    asin_site_ext = asin_list[1].replace("www.amazon.", "")
    image_url = "https://graph.keepa.com/pricehistory.png?domain=" + asin_site_ext + "&asin=" + asin_name + ""

    image_name = asin_name + "_" + str(random_integer) + ".jpg"

    response = rq.get(image_url)
    if response.status_code == 200:
        with open(image_name, 'wb') as f:
            f.write(response.content)

    # store keepa image name and asin into t_asin_picture table
    store_asin_picture(asin_name, image_name)

    return image_name