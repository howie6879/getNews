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

            title = soup.find('h1', class_="title").get_text()
            abstract = re.findall(r'<meta\s*name="?description"?\s*content="(.*?)"', newstr)[0]
            keywords = re.findall(r'<meta\s*name="?keywords"?\s*content="(.*?)"', newstr)[0]
            source = soup.find('span', class_="src").get_text()
            tag = soup.find('a', ga_event="click_channel").get_text()
            cateType = {"社会": "news_society", "娱乐": "news_entertainment", "科技": "news_tech", "汽车": "news_car",
                        "体育": "news_sports", "财经": "news_finance",
                        "军事": "news_military", "国际": "news_world", "时尚": "news_fashion", "旅游": "news_travel",
                        "探索": "news_discovery", "育儿": "news_baby",
                        "养生": "news_regimen", "美文": "news_story", "故事": "news_essay", "游戏": "news_game",
                        "历史": "news_history", "美食": "news_food"}

            try:
                tag = cateType[tag]
            except Exception:
                tag = 'news_society'
            htmlContent = str(header) + str(content)
            textContent = self.parseHtml(htmlContent)
            img_url_list = re.findall(r'<img.*?src="(.*?)"/?>',htmlContent)

            return textContent, htmlContent, img_url_list, title, abstract, keywords, source, tag

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
                abstract = re.sub('\s*', '', re.sub('\n*', '', abstract))[0:100]
            abstract = re.findall(r'<meta\s*name="?description"?\s*content="(.*?)"', newstr)[0] + abstract
            #print(abstract)
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
