import requests
import re
from lxml import etree
from bs4 import BeautifulSoup
import codecs


class ContentOperator():
    """
    通过excel表中的链接获取对应网页新闻的正文
    """

    def __init__(self):
        pass

    """
    :param url为待爬取的头条网页链接
    """

    def getToutiaoContent(self, url):
        try:
            newstr = requests.get(url).content.decode("utf-8")  # 获取对应网页html正文

            soup = BeautifulSoup(newstr, "lxml")
            header = soup.find('div', class_="article-header")
            content = soup.find('div', class_="article-content")

            if content == None or header == None:
                return None, None, None

            htmlContent = str(header) + str(content)
            textContent = self.parseHtml(htmlContent)

            img_list = BeautifulSoup(htmlContent, "lxml").find_all("img")

            img_url_list = []
            if img_list:
                for img in img_list:
                    img_url_list.append(img.get("src"))

            return textContent, htmlContent, img_url_list

        except ConnectionError:
            exit("ConnecttionError")
        except Exception:
            return None, None, None

    """
     :param url为待爬取的新浪网页链接
     """

    def getSinaContent(self, url):
        try:
            newstr = requests.get(url).content.decode("utf-8")  # 获取对应网页html正文

            soup = BeautifulSoup(newstr, "lxml")
            header = soup.find('h1', id="artibodyTitle")
            content = soup.find('div', id="artibody")
            keywordTag = soup.find('div', class_="article-keywords")
            quotation = soup.find('div', class_="quotation")

            if header == None:
                header = soup.find('h1', id="main_title")

            if keywordTag == None:
                keywordTag = soup.find('p', class_="art_keywords")

            if content == None or header == None:
                return

            htmlContent = str(header) + str(content)
            textContent = self.parseHtml(htmlContent)
            # 设置摘要
            if quotation:
                patten = re.compile('<p.*?>(.*?)</p>', re.S)
                item = re.findall(patten, str(quotation))
                abstract = item[0]
            else:
                abstract = str(textContent)
                abstract = re.sub('\s*','',re.sub('\n*','',abstract))[0:100]
            abstract = re.findall(r'<meta\s*name="?description"?\s*content="(.*?)"', newstr)[0] + abstract
            print(abstract)
            img_url_list = []
            if content:
                img_list = BeautifulSoup(htmlContent, "lxml").find_all("img")
                if img_list:
                    for img in img_list:
                        if 'ico' not in str(img.get("src")):
                            img_url_list.append(img.get("src"))
            keyword_list = []
            if keywordTag:
                keyword = keywordTag.find_all("a")
                if keyword:
                    for word in keyword:
                        keyword_list.append(word.get_text())

            # print(textContent)
            # print(htmlContent)
            # print(','.join(img_url_list))
            # print(','.join(keyword_list))
            # print(abstract)
            return textContent, htmlContent, img_url_list, keyword_list, abstract

        except ConnectionError:
            exit("ConnecttionError")
        except Exception as e:
            print(e)
            return None, None, None, None, None

    def parseHtml(self, htmlContent):
        """
        :param htmlContent为要解析为纯文本的html正文
        """
        pn = re.compile(r'<script>[\s\S]*</script>', re.S)
        tmpContent = pn.sub('', htmlContent)
        pt = re.compile(r'<[^>]+>', re.S)
        return pt.sub(' ', tmpContent)

# c = ContentOperator()
# c.getSinaContent("http://ent.sina.com.cn/tv/zy/2016-05-26/doc-ifxsqxxs7700323.shtml")
