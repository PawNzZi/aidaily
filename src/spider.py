# spider.py
import requests
from bs4 import BeautifulSoup
import re


class NewsSpider:
    def __init__(self):
        # 统一请求头配置
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            "Accept-Language": "zh-CN",
            "Referer": "https://www.aibase.com/zh/daily"
        }

        # 初始化结果存储
        self.latest_news = {
            "title": "",
            "link": "",
            "content": ""
        }

    def extract_news_article(self):
        """主入口方法"""
        try:

            list_data = self._fetch_news_list()

            if not list_data:
                return "未获取到新闻列表"

            content_data = self._fetch_news_content(list_data["link"], list_data["title"])

            if not content_data:
                return "内容解析失败"

            return content_data
        except Exception as e:
            return str(e)

    def _fetch_news_list(self):
        """获取新闻列表"""
        try:

            response = requests.get("https://www.aibase.com/zh/daily",
                                    headers=self.headers,
                                    timeout=30)
            response.encoding = "utf-8"

            soup = BeautifulSoup(response.text, "html.parser")
            grid_div = soup.find("main", class_="flex flex-col mx-auto w-full")

            if grid_div:
                a_tag = grid_div.find("a")
                if a_tag and a_tag.has_attr("href"):
                    return {
                        "link": a_tag["href"],
                        "title": a_tag.find("div").get_text(strip=True) if a_tag.find("div") else ""
                    }
            return None
        except Exception as e:
            raise Exception(f"获取列表失败: {str(e)}")

    def _fetch_news_content(self, href, title):
        """获取新闻详情"""
        try:

            full_url = f"https://www.aibase.com{href}"
            response = requests.get(full_url,
                                    headers=self.headers,
                                    timeout=35)
            response.encoding = "utf-8"

            soup = BeautifulSoup(response.text, "html.parser")
            article_div = soup.find("div", class_="px-4 flex flex-col mt-8 md:mt-16")

            if article_div:
                paragraphs = article_div.find_all("p")
                exclude_paragraphs = self._get_excluded_paragraphs(article_div, paragraphs)

                paragraph_texts = [
                    p.get_text(strip=True)
                    for p in paragraphs
                    if p not in exclude_paragraphs
                ]

                # 定位有效内容起始点
                try:

                    # start_index = next(i for i, t in enumerate(paragraph_texts) if "1." in t)
                    # start_index = next(i for i, t in enumerate(paragraph_texts) if "https: // top.aibase.com / '," in t)

                    return self._process_paragraphs(paragraph_texts[2:])
                except StopIteration:
                    return ' '.join(paragraph_texts)  # Fallback方案
            return None
        except Exception as e:
            raise Exception(f"获取内容失败: {str(e)}")

    def _get_excluded_paragraphs(self, article, paragraphs):
        """获取需要排除的段落"""
        excluded = set()
        # 排除带样式的段落
        excluded.update(p for p in paragraphs if p.has_attr("style"))
        # 排除引用块中的段落
        for blockquote in article.find_all("blockquote"):
            excluded.update(blockquote.find_all("p"))
        return excluded

    def _process_paragraphs(self, paragraphs):
        """结构化处理内容（私有方法）"""
        title_pattern = re.compile(r"^(\d+)[\.、]")
        processed = []
        current_title = None
        content_buffer = []

        for text in paragraphs:
            match = title_pattern.match(text)
            if match:
                if current_title is not None and content_buffer:
                    processed.append(f"{current_title}. {' '.join(content_buffer)}")
                try:
                    current_title = int(match.group(1))
                except ValueError:
                    current_title = None
                content_buffer = []
            elif current_title is not None:
                content_buffer.append(text)

        if current_title is not None and content_buffer:
            processed.append(f"{current_title}. {' '.join(content_buffer)}")

        return '\\n'.join(processed)

# if __name__ == "__main__":
#     spider = NewsSpider()
#     result = spider.extract_news_article()
#     if result["status"]:
#         print("抓取成功：")
#         print(f"标题：{result["data"]["title"]}")
#         print(f"内容：{result["data"]["content"]}...")
#     else:
#         print(f"抓取失败：{result['error']}")





