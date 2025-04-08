from mcp.server import FastMCP
from spider import NewsSpider

app = FastMCP('spider')


@app.tool()
def spider_ai_daily() -> str:
    """ AI日报生成 """
    spider = NewsSpider()
    content = spider.extract_news_article()

    return content


# @app.tool()
# def translate(content: str) ->str:
#     """
#       翻译并精简总结
#
#     """
#     return

if __name__ == "__main__":
    app.run(transport='stdio')
