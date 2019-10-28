import pymysql
from datetime import date



# remote database connection
db_host = DB_HOST
db_user = DB_USER
db_password = DB_PASSWORD
db_name = DB_NAME
db_port = DB_PORT


# # local database connection
# db_host = DB_LOCAL_HOST
# db_user = DB_LOCAL_ROOT
# db_password = DB_LOCAL_PASSWORD
# db_name = DB_LOCAL_NAME
# db_port = DB_LOCAL_PORT






# get all asin in organized way from t_asinasin table. format is ['asin_name', 'asin_site']
def get_all_asin_record():

    # Open database connection
    mail_db = pymysql.connect( db_host, db_user, db_password, db_name, db_port )

    # cursor object
    cursor = mail_db.cursor()

    # run the query
    cursor.execute("SELECT asin, relatedasin, relatedasin2, relatedasin3, site FROM t_asinasin")

    # Fetch all rows
    raw_data = cursor.fetchall()

    # process each asin with it's correspond site name
    asin_list_with_site_name = []
    a_l = []
    for item in raw_data:
        temp_asin_data = []
        for x in range(0, len(item) - 1):
            if item[x]:
                temp_asin_data.append([item[x], item[-1]])
        a_l.append(temp_asin_data)
        temp_asin_data = []

    for item in a_l:
        for si_item in item:
            asin_list_with_site_name.append(si_item)
    # disconnect from server
    mail_db.close()

    return asin_list_with_site_name




# store asin review info in t_asinreview table
def store_asin_review_info(asin_name, asin_site, review_response):
    # Open database connection
    mail_db = pymysql.connect( db_host, db_user, db_password, db_name, db_port )

    # cursor object
    cursor = mail_db.cursor()

    # run the query
    if review_response:
        print(len(review_response))
        # try:
        #     for review in review_response['reviews']:
        #         cursor.execute("INSERT INTO t_asin_reviews(asin, asin_site, review_text, review_posted_date, review_title, review_rating, review_author) VALUES (%s, %s, %s, %s, %s, %s, %s)", (asin_name, asin_site, review['review_text'], review['review_posted_date'], review['review_header'], review['review_rating'], review['review_author']))
        #         mail_db.commit()
        #     print("Review info stored in db!")
        # except:
        #     print("No reviews found!")

        for review in review_response['reviews']:
            cursor.execute("INSERT INTO t_asin_reviews(asin, asin_site, review_text, review_posted_date, review_title, review_rating, review_author) VALUES (%s, %s, %s, %s, %s, %s, %s)", (asin_name, asin_site, review['review_text'], review['review_posted_date'], review['review_header'], review['review_rating'], review['review_author']))
            mail_db.commit()
        print("Review info stored in db!")



# store keepa graph picture info in t_asin_picture table
def store_asin_picture(asin_name, picture_name):
    # Open database connection
    mail_db = pymysql.connect( db_host, db_user, db_password, db_name, db_port )

    # cursor object
    cursor = mail_db.cursor()

    # run the query
    try:
        cursor.execute("INSERT INTO t_asin_picture(asin, image_name) VALUES (%s, %s)", (asin_name, picture_name))
        mail_db.commit()
        print(asin_name + "--------" + picture_name + "---------" + " stored in db!")
    except:
        print("Something wrong!")





# store asin all info info in t_asin_infos table
def store_asin_info(asin_name, asin_site, previous_price, price_change, review_response, keepa_image):
    # Open database connection
    mail_db = pymysql.connect( db_host, db_user, db_password, db_name, db_port )

    # cursor object
    cursor = mail_db.cursor()

    # get current date
    today = date.today()    
    
    # run the query
    cursor.execute("INSERT INTO t_asin_infos(asin, site, current_price, previous_price, price_change, total_review, score, crawl_date, keepa_image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (asin_name, asin_site, review_response['product_price'], previous_price, price_change, review_response['number_reviews'], review_response['total_score'], today, keepa_image))

    # # test query with constant value
    # cursor.execute("INSERT INTO t_asin_infos(asin, site, price, total_review, score, crawl_date, keepa_image) VALUES (%s, %s, %s, %s, %s, %s, %s)", ("B00O1N69VQ", "www.amazon.com", "$64.99", "33", "3.4", today, "B00O1N69VQ_1156374544.jpg"))
    
    mail_db.commit()
    print("All asin info stored in db!")
        







# delete all - used this function in development stage
def delete_old_record(asin):
    # Open database connection
    mail_db = pymysql.connect( db_host, db_user, db_password, db_name, db_port )

    # cursor object
    cursor = mail_db.cursor()

    cursor.execute("DELETE FROM t_asin_reviews WHERE asin='" + asin + "'")
    cursor.execute("DELETE FROM t_asin_picture WHERE asin='" + asin + "'")
    cursor.execute("DELETE FROM t_asin_infos WHERE asin='" + asin + "'")

    mail_db.commit()



# this function will return raw price without any price symbol
def price_without_symbol(asin, price):
    new_price = 0
    asin_ext = asin.split(".")[-1]
    if asin_ext == "de":
        new_price = float(price.split()[0].replace(",", "."))
    else:
        new_price = float(price.replace("$", ""))
    return new_price




# this function will return current_price, previous_price, price_change data
def price_analysis(asin_name, asin_site, current_scrpaed_price):
    price_data = []
    # Open database connection
    mail_db = pymysql.connect( db_host, db_user, db_password, db_name, db_port )

    # cursor object
    cursor = mail_db.cursor()

    # run the query
    # cursor.execute("SELECT price FROM t_asin_infos WHERE asin='" + asin_name + "'")
    cursor.execute("SELECT current_price FROM t_asin_infos WHERE asin='" + asin_name + "'")
    # Fetch all rows
    raw_data = cursor.fetchall()
    previous_raw_price = 0
    # new_raw_price = 0
    previous_price = 0
    new_price = 0
    price_gap = 0
    if raw_data:
        previous_raw_price = raw_data[0][0]
        previous_price = price_without_symbol(asin_site, raw_data[0][0])
    if current_scrpaed_price:
        # new_raw_price = current_scrpaed_price
        new_price = price_without_symbol(asin_site, current_scrpaed_price)
    if previous_price and new_price:
        price_gap = new_price - previous_price
    price_data.append(previous_price)
    print("Previous price", previous_raw_price)
    print("Current price", current_scrpaed_price)
    print("Price gap", price_gap)

    return previous_raw_price, price_gap




# delete all - used this function in development stage
def delete_all_record():
    # Open database connection
    mail_db = pymysql.connect( db_host, db_user, db_password, db_name, db_port )

    # cursor object
    cursor = mail_db.cursor()

    cursor.execute("DELETE FROM t_asin_picture WHERE asin='B07DNSBZTZ'")
    mail_db.commit()
