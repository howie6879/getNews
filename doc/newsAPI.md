## 各大新闻网站API分析

### 1.今日头条

​	今日头条目录可分为如下部分：

​	domain : `http://toutiao.com`

​	directory:

​		-1.1：  *hot_words* : `http://toutiao.com/hot_words/?_=1463066142015`

​		链接功能：返回实时新闻热词	

​		参数：?_

​		参数值：当前时间戳	?_ = time.time()

​		-1.2： */api/article/recent/* : `http://toutiao.com/api/article/recent/?source=2&count=20&category=__all__&max_behot_time=1463067626.96&utm_source=toutiao&offset=0&_=1463067627001`

​		链接功能：返回对应模块实时新闻

​		链接：`http://toutiao.com/api/article/recent/`

`?count=20&category=__all__&max_behot_time=1463067626.96`

​		

|       参数       |   参数值    |
| :------------: | :------: |
|     count      |  返回新闻数量  |
|    category    |   新闻种类   |
| max_behot_time | 热点新闻最大时间 |

​	

​		category：

|      category      | name |
| :----------------: | :--: |
|     \_\_all__      | 推荐新闻 |
|      news_hot      | 热点新闻 |
|       video        | 视频新闻 |
|   gallery_detail   | 图片新闻 |
|    news_society    | 社会新闻 |
| news_entertainment | 娱乐新闻 |
|     news_tech      | 科技新闻 |
|      news_car      | 汽车新闻 |
|    news_sports     | 体育新闻 |
|    news_finance    | 财经新闻 |
|   news_military    | 军事新闻 |
|     news_world     | 国际新闻 |
|    news_fashion    | 时尚新闻 |
|    news_travel     | 旅游新闻 |
|   news_discovery   | 探索新闻 |
|     news_baby      | 育儿新闻 |
|    news_regimen    | 养生新闻 |
|     news_story     | 故事新闻 |
|     news_essay     | 美文新闻 |
|     news_game      | 游戏新闻 |
|    news_history    | 历史新闻 |
|     news_food      | 美食新闻 |