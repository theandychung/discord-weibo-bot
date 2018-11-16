# coding=utf-8

WEIBO_API_ROOT = 'https://m.weibo.cn/'

# 用户详情
PEOPLE_DETAIL_URL = WEIBO_API_ROOT + 'api/container/getIndex?type=uid&value={id}'

# 微博详情
STATUS_DETAIL_URL = WEIBO_API_ROOT + 'statuses/extend?id={id}'

# 文章详情 {文章ID} eg{2309404178688362029907}
ARTICLE_DETAIL_URL = WEIBO_API_ROOT + 'article/contents?id={id}'

# 粉丝列表 {用户ID} {page number}
FOLLOWERS_LIST_URL = WEIBO_API_ROOT + 'api/container/getIndex?containerid=231051_-_fans_-_{id}&since_id={page_num}'

# 他关注的用户的列表 {用户ID} {page number}
FOLLOWS_LIST_URL = WEIBO_API_ROOT + 'api/container/getIndex?containerid=231051_-_followers_-_{id}&page={page_num}'

# 全部微博列表
WEIBO_LIST_URL = WEIBO_API_ROOT \
                     + 'api/container/getIndex?containerid=230413{id}_-_WEIBO_SECOND_PROFILE_WEIBO&page={page_num}'

# 原创微博列表
ORI_WEIBO_LIST_URL = WEIBO_API_ROOT \
                     + 'api/container/getIndex?containerid=230413{id}_-_WEIBO_SECOND_PROFILE_WEIBO_ORI&page={page_num}'

# 全部文章列表 {用户id} {页数(时间戳_页码)}
# ARTICLE_LIST_URL = WEIBO_API_ROOT + 'api/container/getIndex?containerid=231018{id}_-_longbloglist&since_id={page_num}'

# 全部文章列表 {用户ID} {页数}
ARTICLE_LIST_URL = WEIBO_API_ROOT \
                   + 'api/container/getIndex?containerid=230413{id}_-_WEIBO_SECOND_PROFILE_WEIBO_ARTICAL&page={page_num}'

# 原创文章列表 {用户ID}
ORI_ARTICLE_LIST_URL = WEIBO_API_ROOT + 'api/container/getIndex?containerid=231018{id}_-_longbloglist_original'

# 图片

# 全部微博列表

# 搜索
SEARCH_URL = WEIBO_API_ROOT + 'searchs/result?type=all&queryVal={key_word}'

# 微博头条文章前缀
ARTICLE_HREF_PREFIX = 'http://media.weibo.cn/article'
