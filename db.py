import psycopg2
import logging
import datetime
from scraping.utils import *

today = datetime.date.today()
ten_days_ago = datetime.date.today() - datetime.timedelta(10)
from find_job.secret import DB_PASSWORD, DB_HOST, DB_NAME, DB_USER

try:
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD)
except:
    logging.exception('Unable to open DB -{}'.format(today))
else:
    cur = conn.cursor()
    cur.execute("""SELECT city_id, speciality_id FROM subscribers_subscriber WHERE is_active=%s;""",(True,))
    cities_qs = cur.fetchall()
    print(cities_qs)
    todo_list = {i[0]:set() for i in cities_qs}
    for i in cities_qs:
        todo_list[i[0]].add(i[1])
    print(todo_list)
    cur.execute("""SELECT * FROM scraping_site;""")
    sities_qs = cur.fetchall()
    sites = {i[0]: i[1]for i in sities_qs}
    print(sites)
    url_list = []
    for city in todo_list:
        for sp in todo_list[city]:
            tmp = {}
            cur.execute("""SELECT site_id, url_address FROM scraping_url 
                     WHERE city_id=%s AND speciality_id=%s;""",(city, sp))
            qs = cur.fetchall()
            print(qs)
            if qs:
                tmp['city'] = city
                tmp['speciality'] = sp
                for item in qs:
                    site_id = item[0]
                    tmp[sites[site_id]] = item[1]
                url_list.append(tmp)
    print(url_list)
    all_data = []
    if url_list:
        for url in url_list:
            tmp = {}
            tmp_content = []
            tmp_content.extend(djinni(url['Djinni.co']))
            tmp_content.extend(rabota(url['Rabota.ua']))
            tmp_content.extend(work(url['Work.ua']))
            tmp_content.extend(dou(url['Dou.ua']))
            tmp['city'] = url['city']
            tmp['speciality'] = url['speciality']
            tmp['content'] = tmp_content
            all_data.append(tmp)

    #print(all_data)
    if all_data:
        for data in all_data:
            city = data['city']
            speciality = data['speciality']
            jobs = data['content']
            for job in jobs:
                cur.execute("""SELECT * FROM scraping_vacancy WHERE url=%s;""",(job['href'],))
                qs = cur.fetchone()
                if not qs:
                    cur.execute("""INSERT INTO scraping_vacancy (city_id, speciality_id, title,
                                                                 url, description, company, timestamp) VALUES (%s,%s,%s,%s,%s,%s,%s,);""",
                                (city,speciality, job['title'],job['href'],job['descript'],job['company'],today))
    cur.execute("""DELETE FROM scraping_vacancy WHERE timestamp<=%s;""",(ten_days_ago,))
    conn.commit()
    cur.close()
    conn.close()