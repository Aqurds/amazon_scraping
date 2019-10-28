import json
import random
import urllib3
import csv
from lxml import html
from json import loads, dump
from requests import get
from dateutil import parser as dateparser_to_html
import concurrent.futures
from time import sleep


#GLOBAL VARIABLES
review_total_pages = []
headers = {}

def parse_json_to_csv(name, json):
    with open(f"{name}.csv", mode='w', newline='') as file:
        employee_writer = csv.writer(file, delimiter=',')
        employee_writer.writerow(json['reviews'][0].keys())
        for data in json['reviews']:
            employee_writer.writerow(data.values())


def get_random_user_agent():
    user_agent_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
                       'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36']
    # return random.choice(user_agent_list)
    return user_agent_list[0]


def get_header(asin, site):
    try:
        global headers
        # ratings_dict = {}
        amazon_url = 'https://' + site + '/product-reviews/' + asin + '/ref=cm_cr_arp_d_paging_btm_next_1?pageNumber=1'
        headers = {'User-Agent': get_random_user_agent()}
        urllib3.disable_warnings()
        response = get(amazon_url, headers=headers)
        print(response)
        cleaned_response = response.text.replace('\x00', '')
        parser_to_html = html.fromstring(cleaned_response)
        # print(parser_to_html)

        # data = {'number_reviews': ''.join(parser_to_html.xpath('//*[@id="cm_cr-product_info"]/div/div[1]/div[3]/span/text()')).strip().replace("  customer ratings", "").replace(",", ""),
        #         'product_price': ''.join(parser_to_html.xpath('.//span[contains(@class,"a-color-price arp-price")]//text()')).strip(),
        #         'product_name': ''.join(parser_to_html.xpath('.//a[@data-hook="product-link"]//text()')).strip()}
        #         # 'total_ratings': parser_to_html.xpath('//table[@id="histogramTable"]//tr')}
        data = {'number_reviews': ''.join(parser_to_html.xpath('//*[@id="cm_cr-product_info"]/div/div[1]/div[3]/span/text()')).split()[0].replace(",", ""),
                'product_price': ''.join(parser_to_html.xpath('.//span[contains(@class,"a-color-price arp-price")]//text()')).strip(),
                'product_name': ''.join(parser_to_html.xpath('.//a[@data-hook="product-link"]//text()')).strip(),
                'total_score': parser_to_html.xpath('//*[@id="cm_cr-product_info"]/div/div[1]/div[2]/div/div/div[2]/div/span/a/span//text()')[0].split()[0]}
                # 'total_ratings': parser_to_html.xpath('//table[@id="histogramTable"]//tr')}
        # print(parser_to_html.xpath('//*[@id="cm_cr-product_info"]/div/div[1]/div[2]/div/div/div[2]/div/span/a/span//text()'))
        # for ratings in data['total_ratings']:
        #     extracted_rating = ratings.xpath('./td//a//text()')
        #     if extracted_rating:
        #         rating_key = extracted_rating[0]
        #         rating_value = extracted_rating[1]
        #         if rating_key:
        #             ratings_dict.update({rating_key: rating_value})

        number_page_reviews = int(int(data['number_reviews']) / 10) + 2

        # if number_page_reviews % 2 == 0:
        #     number_page_reviews += 1
        # else:
        #     number_page_reviews += 2
        # print(number_page_reviews)
        return data['product_price'], data['product_name'], data['number_reviews'], data['total_score'], number_page_reviews
    except Exception as e:
        print("------- get_header() function returns error!")



def download_site(url, asin_ext):
    global review_total_pages, headers
    urllib3.disable_warnings()
    response = get(url, headers=headers, verify=False, timeout=20)
    cleaned_response = response.text.replace('\x00', '')
    parser_to_html = html.fromstring(cleaned_response)
    reviews = parser_to_html.xpath('//div[contains(@id,"reviews-summary")]')
    if not reviews:
        reviews = parser_to_html.xpath('//div[@data-hook="review"]')
    for review in reviews:
        raw_review_author = review.xpath('.//span[contains(@class,"profile-name")]//text()')
        raw_review_rating = review.xpath('.//i[@data-hook="review-star-rating"]//text()')
        raw_review_header = review.xpath('.//a[@data-hook="review-title"]//text()')
        raw_review_posted_date = review.xpath('.//span[@data-hook="review-date"]//text()')
        raw_review_text1 = review.xpath('.//span[@data-hook="review-body"]//text()')
        # raw_review_text2 = review.xpath(
        #     './/div//span[@data-action="columnbalancing-showfullreview"]/@data-columnbalancing-showfullreview')
        # raw_review_text3 = review.xpath('.//div[contains(@id,"dpReviews")]/div/text()')
        # print(raw_review_posted_date)

        # Cleaning data
        author = ' '.join(' '.join(raw_review_author).split())
        # print(asin_ext)
        if asin_ext == "de":
            review_rating = ''.join(raw_review_rating).replace(' von 5 Sternen', '').replace(',', '.')
        else:
            review_rating = ''.join(raw_review_rating).replace('out of 5 stars', '')
        review_header = ' '.join(' '.join(raw_review_header).split())

        if asin_ext == "de":
            review_posted_date = raw_review_posted_date
        else:
            try:
                review_posted_date = dateparser_to_html.parse(''.join(raw_review_posted_date)).strftime('%d %b %Y')
            except:
                review_posted_date = None
        review_text = ' '.join(' '.join(raw_review_text1).split())

        # # Grabbing hidden comments if present
        # if raw_review_text2:
        #     json_loaded_review_data = loads(raw_review_text2[0])
        #     json_loaded_review_data_text = json_loaded_review_data['rest']
        #     cleaned_json_loaded_review_data_text = re.sub('<.*?>', '', json_loaded_review_data_text)
        #     full_review_text = review_text + cleaned_json_loaded_review_data_text
        # else:
        #     full_review_text = review_text
        # if not raw_review_text1:
        #     full_review_text = ' '.join(' '.join(raw_review_text3).split())

        full_review_text = review_text

        review_dict = {
            'review_text': full_review_text,
            'review_posted_date': review_posted_date,
            'review_header': review_header,
            'review_rating': review_rating,
            'review_author': author
        }
        review_total_pages.append(review_dict)



def get_all_reviews(asin, site):
    global review_total_pages
    url_list = []
    product_price, product_name, number_reviews, total_score, stop_loop_for = get_header(asin, site)
    for page_number in range(1, stop_loop_for):
        amazon_url = 'https://' + site + '/product-reviews/' + \
                     asin + \
                     '/ref=cm_cr_arp_d_paging_btm_next_' + \
                     str(page_number) + \
                     '?pageNumber=' + \
                     str(page_number)
        url_list.append(amazon_url)

    # with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    #     executor.map(download_site, url_list)

    asin_ext = site.split(".")[-1]

    for url in url_list:
        download_site(url, asin_ext)
        print(url)
        # sleep(20)

    response = {
        'product_name': product_name,
        'product_price': product_price,
        'number_reviews': number_reviews,
        'total_score': total_score,
        # 'ratings': ratings_dict,
        'reviews': review_total_pages,
    }
    review_total_pages = [] #empty the list to avoid overlap
    # print(response)
    return response





def core(asinlist):
    try:
        data = {'asin_list': [asinlist],
                'format': 'csvs'}
        if data['format'] == 'csv':
            for asin in data['asin_list']:
                print(f"IN PROCESS FOR: {asin[0]}")
                response = get_all_reviews(asin[0], asin[1])
                parse_json_to_csv(asin, response)
        else:
            for asin in data['asin_list']:
                print(f"IN PROCESS FOR: {asin[0]}")
                temp = get_all_reviews(asin[0], asin[1])
                f = open(asin[0] + '.json', 'w')
                dump(temp, f, indent=4)
                f.close()
                return temp
        
        return f'Success download {data["format"]} file in root directory'
    except Exception as e:
        return f'Error: {e}'




# if __name__ == '__main__':
#     core()