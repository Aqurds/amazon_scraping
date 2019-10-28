# import db function from db_op file
import db_conn as d_c
# import review scraping function from review_scraper file
import review_scraper as r_s
# import review scraping function from review_scraper file
import keepa_image as k_i

# import test
# import test_copy




# get full record of asin organized with the format ['asin_name', 'asin_site']
full_url_list = d_c.get_all_asin_record()
for item in full_url_list:
    print(item)   

for x in range(7, 8):
# for x in range(0, len(full_url_list)):
    asin_list = full_url_list[x]
    asin_name = asin_list[0]
    asin_site = asin_list[1]
    # asin_list = ['B00SUSHIU4', 'www.amazon.de']
    # asin_name = asin_list[0]
    # asin_site = asin_list[1]

    # get the full response containing all information for asin
    review_response = r_s.core(asin_list)
    print("============", review_response['product_price'])
    current_scrpaed_price = review_response['product_price']

    # get current_price, previous_price, price_change data
    previous_price, price_change = d_c.price_analysis(asin_name, asin_site, current_scrpaed_price)

    # delete old record before storing new record
    d_c.delete_old_record(asin_name)

    # get keepa image and save it
    keepa_image_name = k_i.save_keepa_image(asin_list)
    # print(keepa_image_name)

    # store all review info in t_asin_review table
    d_c.store_asin_review_info(asin_name, asin_site, review_response)


    # store all asin info in t_asin_info table
    d_c.store_asin_info(asin_name, asin_site, previous_price, price_change, review_response, keepa_image_name)

    # d_c.delete_all_record()