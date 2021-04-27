import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool



def get_html(url):
    response = requests.get(url)
    return response.text

def get_total_pages(html):
    soup = BeautifulSoup(html,'lxml')
    pages_div = soup.find('div',class_="pageToInsert")
    last_page = pages_div.find_all("a")[-2]
    total_pages = last_page.get("href").split("=")[-1]

    return int(total_pages)

def write_to_csv(data):
    with open("Wildberries_notebooks.csv",'a') as file:
        writer = csv.writer(file, delimiter = "/")
        writer.writerow((data["title"],data["price"],data["characteristic"],data["photo"]))


def get_page_data(html):
    soup = BeautifulSoup(html,"lxml")
    product_list = soup.find("div",class_="catalog_main_table")
    products = product_list.find_all("a",class_="ref_goods_n_p j-open-full-product-card")
    
    for product in products:
        
        try:
            photo = product.find("div",class_="l_class").find("img").get("src")
            if photo.endswith('blank.gif'):
                photo = "https:"+photo[1:]
            else:
                photo = "https:"+photo
        except:
            photo = ""
        
        try:
            title = product.find("div",class_="l_class").find("img").get('alt')
            title = title.split(" ")
            title = title[0:4]
            title = " ".join(title)
            
        except:
            title = ""

        try:
            characteristic = product.find("div",class_="l_class").find("img").get('alt')
            characteristic = characteristic.split(" ")
            characteristic = characteristic[4:]
            characteristic = " ".join(characteristic)
        except:
            characteristic = ""
        
        try:
            price = product.find("span",class_="price-localized").text
        except:
            price = ''
        
        
        data = {'title':title,"characteristic":characteristic,"price":price ,"photo":photo}
        write_to_csv(data)



def speed_up(url):
    html=get_html(url)
    data=get_page_data(html)    





def main():
    notebooks_url = 'https://kg.wildberries.ru/catalog/elektronika/noutbuki-pereferiya/noutbuki-ultrabuki'
    pages="?sort=popular&page="
    
    total_pages=get_total_pages(get_html(notebooks_url))
    urls =[notebooks_url + pages + str(page) for page in range(1,total_pages+1)]
    with Pool(40) as p:
        p.map(speed_up, urls)

    
main()











