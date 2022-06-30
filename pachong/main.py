import os
from icrawler.builtin import BaiduImageCrawler
from icrawler.builtin import BingImageCrawler
from icrawler.builtin import GoogleImageCrawler

# def check_path(path):
#     if not os.path.exists(path):
#         os.makedirs(path)
#     return path
#
# def baidu_bing_crwal(key_words=['news'], max_nums=[1000], save_root=r'./'):
#
#     assert len(key_words)==len(max_nums), "key_words and max_nums must be the same length"
#     # 2个一起爬虫
#     save_root1 = os.path.join(save_root, 'baidu')
#     # 百度爬虫
#     for i in range(len(key_words)):
#         print('-'*20)
#         image_save_root = os.path.join(save_root1, str(i))
#
#         if not os.path.exists(image_save_root):
#             os.makedirs(image_save_root)
#
#         storage = {'root_dir': image_save_root}
#         crawler = BaiduImageCrawler(storage=storage)
#         crawler.crawl(key_words[i], max_num=max_nums[i])
#
#     # bing爬虫
#     save_root2 = os.path.join(save_root, 'bing')
#     for i in range(len(key_words)):
#         print('-'*20)
#         image_save_root = os.path.join(save_root2, str(i))
#
#         if not os.path.exists(image_save_root):
#             os.makedirs(image_save_root)
#
#         storage = {'root_dir': image_save_root}
#         crawler = BingImageCrawler(parser_threads=4,
#                                     downloader_threads=6,
#                                     storage=storage)
#
#         crawler.crawl(key_words[i], max_num=max_nums[i])
#     return

# if __name__ == '__main__':
#     baidu_bing_crwal(key_words=['工作服', '工衣', '工程夹克', '企业工服', '劳保工作服', '劳保服'],
#                      max_nums=[1000, 1000, 1000, 1000, 1000, 1000],#布隆过滤器
#                      #图片哈希
#                      save_root=r'dataset')
# 谷歌图片爬虫
# # 需要爬虫的关键字
list_word = ['石化工人', '化工厂工人' ]
for word in list_word:
#     #bing爬虫
    #保存路径
    bing_storage = {'root_dir': 'DataSets\\'+word}
    #从上到下依次是解析器线程数，下载线程数，还有上面设置的保存路径
    bing_crawler = BingImageCrawler(parser_threads=4,
                                    downloader_threads=6,
                                    storage=bing_storage)
    #开始爬虫，关键字+图片数量
    bing_crawler.crawl(keyword=word,
                       max_num=3000)
#
    #百度爬虫
    # baidu_storage = {'root_dir': 'baidu\\' + word}
    # baidu_crawler = BaiduImageCrawler(parser_threads=2,
    #                                   downloader_threads=4,
    #                                   storage=baidu_storage)
    # baidu_crawler.crawl(keyword=word,
    #                     max_num=2000)


    # # google爬虫
    # google_storage = {'root_dir': '‘google\\' + word}
    # google_crawler = GoogleImageCrawler(parser_threads=4,
    #                                    downloader_threads=4,
    #                                    storage=google_storage)
    # google_crawler.crawl(keyword=word,
    #                      max_num=4000)