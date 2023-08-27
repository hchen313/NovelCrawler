import requests
from lxml import etree
from multiprocessing import Pool
import re

# only tested for https://www.biquge.co/


#  single chapter download
def download(args):
    try:
        title, url= args
        page= requests.get(url)
        page.encoding= page.apparent_encoding
        page_content= etree.HTML(page.text)
        text= page_content.xpath("//div[@id='content']/text()")
        return [(line, title) for line in text]
    except:
        print("fail to download:" + title )


if __name__ == "__main__":

    url= input("Enter the link:\n")
    r= requests.get(url)
    r.encoding= r.apparent_encoding
    content = etree.HTML(r.text)
    list= content.xpath("//div[@id='list']/dl/dt[2]/following::dd")


    # find the main page link, find the 3rd occurrence of /
    val= -1
    for i in range(0, 3):
        val= url.find('/', val + 1)
    main_page= url[0:val]

    new_list= [(chapter.xpath("./a/text()")[0], main_page + chapter.xpath("./a/@href")[0]) for chapter in list]

    with Pool() as pool:
        res= pool.map(download, new_list)

    with open("text.txt", "a+", encoding='utf-8') as file:
        for chapter_content in res:
            if chapter_content:
                title_written = False
                for line, title in chapter_content:
                    if not title_written:
                        file.write(title)  # Write the title
                        file.write("\n")
                        title_written = True
                    # remove all the non-chinese characters
                    new_line= re.sub(r'[^\u4e00-\u9fff]+', '', line)
                    file.write(new_line)
                    file.write("\n")