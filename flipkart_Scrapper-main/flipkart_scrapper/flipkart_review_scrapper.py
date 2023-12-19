import requests
from bs4 import BeautifulSoup
import csv
import os
import codecs
import emoji
import logging

logging.basicConfig(filename="scrapper.log" , level=logging.INFO)


flipkart_page="https://www.flipkart.com"
########inputs query########################
query=str(input("enter the query : "))
query =query.replace(" ","")
# proxy="https://vepro.hocke.eu/proxy/index.php?"
proxy=""
flipkart_query_page=f'{proxy}{flipkart_page}/search?q={query}'
print(flipkart_query_page)
try:
    flipkart_query_page_result=requests.get(flipkart_query_page)
except ConnectionError:
  print("Connection error")
except requests.exceptions.RequestException as e:
  # Handle any other errors
  print(f"Unhandled error: {e}")

print(flipkart_query_page_result)
# print(flipkart_query_page_result.text)
soup=BeautifulSoup(flipkart_query_page_result.text,"html.parser")
# print(soup)

####################################getting list of all the products#################################################
product_box_list=soup.find_all("div",{"class":"_2kHMtA"})
# len(product_box_list)
# print (len(product_box_list))
# print(product_box_list[0])
# link=flipkart_page+product_box_list[0].a['href']
# print(link)

# for i in product_box_list:      ######## gettting all produc tlinks######
#    print(i.a['href'])



######################################## opening product link###################################

product_link_test=flipkart_page+product_box_list[0].a['href']
k=0
for product in product_box_list:
  k=k+1
  product_link_test=flipkart_page+product.a['href']
  try:
      product_page_request=(requests.get(product_link_test))
  except ConnectionError:
    print("Connection error")
  except requests.exceptions.RequestException as e:
    # Handle any other errors
    print(f"Unhandled error: {e}")
  product_soup=BeautifulSoup(product_page_request.text,'html.parser')
  # print (product_soup.prettify(encoding='utf-8')) ############### this line nessesary to prevent error###############
  comment_box_list=product_soup.find_all('div',{"class":"_16PBlm"})
  print(len(comment_box_list))
##################################stores in csv file all comments of a perticular product#################################
  file_name=f'reviews{k}.csv'
  folder_path = 'C:/Users/HP/Desktop/flipkart_scrapper/review_storage'  
  file_path = os.path.join(folder_path, file_name)

  try:
      with open(file_path, 'w', encoding='utf-8', errors='replace') as csvfile:
        fieldnames = ['name', 'rating', 'review_heading', 'review_full']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
  except OSError as e :
      print(f"Error writing file: {e}")

  for comment_box in comment_box_list:
    try:
      name=emoji.demojize(comment_box.div.div.find('p',{"class":"_2sc7ZR _2V5EHH"}).text)
      print(name)
    except:
      logging.info("name")
    try:
      rating=comment_box.div.div.div.div.text
      print(rating)
    except:
      rating = 'No rating'
      logging.info("rating")
    try:
      review_heading=emoji.demojize(comment_box.div.div.div.p.text)
      print(review_heading)
    except:
      review_heading='No review_heading'
      logging.info("No review_heading")
    try:
      review_full=emoji.demojize(comment_box.div.div.find_all('div',{"class":""})[0].div.text)
      print(review_full)
    except:
      review_full='No review_full'
      logging.info("No review_full")

    try:
      with open(file_path, 'a', encoding='utf-8', errors='replace') as csvfile:
        fieldnames = ['name', 'rating', 'review_heading', 'review_full']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writerow({'name': name, 'rating': rating, 'review_heading': review_heading, 'review_full': review_full})
    except OSError as e :
      print(f"Error writing file: {e}")