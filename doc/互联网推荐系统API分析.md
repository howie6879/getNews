## 互联网推荐系统API分析

### 一、目标新闻网站api分析

#### 1-1.今日头条

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

#### 1-2.新浪新闻

​	新浪新闻目录可分为如下部分：

​	domain : `http://roll.news.sina.com.cn`

​	directory:

​		链接功能：进入新浪新闻滚动业，页面返回的是新浪当前最新新闻

​		-2.1： *num=20&asc=&page=1* : 	`http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php?col=89&spec=&type=&k=&num=20&asc=&page=1&r=0.41627189057293945`

​		链接功能：返回滚动新闻
​		参数：num每页新闻条数,page页数


​		

|  参数  |  参数值   |
| :--: | :----: |
| num  | 每页新闻条数 |
| page |   页数   |

### 二、互联网推荐系统api

**说明：调用api时，首选进行tooken验证，验证通过返回结果**

#### 2-1.注册api

链接：`/api/register?name=huyu&passwd=123456&tags=x&phone=X&time=X&tooken=X`

链接功能：新用户进行注册

|   参数   |     说明      |
| :----: | :---------: |
|  name  |   注册用户昵称    |
| passwd |     密码      |
| phone  |     电话      |
|  tags  | 标签1，标签2.... |
|  time  |    注册时间戳    |
| token  |   身份验证字符串   |

**参数返回：**

注册结果：`{"data": {"user_id": ""}, "message": "success"}`

用户已存在：`{"message": "failed", "data": {"flag": -1}}`

注册失败：`{"message": "failed", "data": {"flag": 0}}`

#### 2-2.登录api

链接：`/api/login?passwd=x&phone=x&time=x&tooken=x`

链接功能：用户登录
|   参数   |   说明    |
| :----: | :-----: |
| passwd |   密码    |
| phone  |   电话    |
|  time  |  验证时间戳  |
| token  | 身份验证字符串 |

**参数返回：**

登录成功：`{"message": "success", "data": {"user_id": ""}}`

密码错误：`{"message": "failed", "data": {"flag": -1}}`

用户不存在：`{"message": "failed", "data": {"flag": -2}}`

请求失败：`{"message": "failed", "data": {"flag": 0}}`

#### 2-3.新闻列表api

链接：`/api/newstags?count=x&alrequest=x&userid=x&tag=x&time=x&tooken=x`

链接功能：返回新闻列表信息
|    参数     |      说明      |
| :-------: | :----------: |
|   count   |    请求新闻数量    |
| alrequest |   已请求新闻数量    |
|  userid   |     用户编号     |
|    tag    | 新闻标签（默认空为全部） |
|   time    |    验证时间戳     |
|   token   |   身份验证字符串    |

**参数返回：**
返回参数说明：
|      参数       |  说明   |
| :-----------: | :---: |
|     time      |  时间   |
|   abstract    |  摘要   |
|     title     |  标题   |
| comment_times | 评论次数  |
|  read_times   | 阅读次数  |
|  love_times   | 喜欢次数  |
|    news_id    | 新闻编号  |
|     image     | 图片url |
|    source     |  来源   |
查询返回成功：
`{"message": "success", "data": [{"time": "", "abstract": "", "title": "",` `"comment_times": 1, "read_times": 1, "love_times": 1, "news_id": "",` `"image": "", "source": ""}, {"time": "", "abstract": "", "title": "",` `"comment_times": 2, "read_times": 2, "love_times": 2, "news_id": "",` `"image": "", "source": ""}]}`

请求数目超出：
`{"message": "failed", "data": {"flag": -1}}`

请求失败：
`{"message": "failed", "data": {"flag": 0}}`

#### 2-4.新闻详情api

链接：`/api/newscontent?newsid=x&userid=x&time=x&tooken=x`

链接功能：返回新闻列表信息
|   参数   |   说明    |
| :----: | :-----: |
| newsid |  新闻编号   |
| userid |  用户编号   |
|  time  |  验证时间戳  |
| token  | 身份验证字符串 |

**参数返回：**
参数返回说明：
|       参数        |       说明       |
| :-------------: | :------------: |
|     content     |    新闻html正文    |
|  comment_time   |      留言时间      |
|    username     |     留言用户昵称     |
|    head_url     |   留言用户头像url    |
| comment_content |      留言内容      |
|   is_comment    | 用户是否评论该新闻（0/1） |
|     is_love     | 用户是否喜欢该新闻（0/1） |

查询返回成功：
`{"message": "success", "data": {"content": "", "comment_list": [{"time": "",` `"username": "", "head_url": "", "comment_content": "","dianzan_num": "9"}, {"time":` `"shijian2", "username": "", "head_url": "", "comment_content": ""}],` `"is_comment": 1, "is_love": 0}}`

请求失败：`{"message": "failed", "data": {"flag": 0}}`

#### 2-5.用户信息查询api

链接：`/api/userinfo?userid=x&time=x&tooken=x`

链接功能：返回用户详细信息
|   参数   |   说明    |
| :----: | :-----: |
| userid |  用户编号   |
|  time  |  验证时间戳  |
| token  | 身份验证字符串 |

**参数返回：**
参数返回说明：
|      参数       |  说明  |
| :-----------: | :--: |
|   user_name   | 用户昵称 |
|     phone     | 用户电话 |
|     image     |  头像  |
|     email     | 用户邮箱 |
|  read_times   | 阅读次数 |
|  love_times   | 喜欢次数 |
| message_times | 评论次数 |


查询返回成功：
`{"message": "success", "data": {"love_times": 1, "phone": "",` `"message_times": 1, "read_times": 1, "user_name": "", "email": "",` `"image": ""}}`

请求失败：`{"message": "failed", "data": {"flag": 0}}`


#### 2-6.用户信息修改api

链接：`/api/userinfochange?userid=x&username=x&image=x`
`&email=x&time=1&tooken=x`

链接功能：返回用户详细信息
|    参数    |   说明    |
| :------: | :-----: |
|  userid  |  用户编号   |
| username |  用户昵称   |
|  image   |   头像    |
|  email   |  用户邮箱   |
|   time   |  验证时间戳  |
|  token   | 身份验证字符串 |

**参数返回：**
参数返回说明：
|      参数       |  说明  |
| :-----------: | :--: |
|   user_name   | 用户昵称 |
|     phone     | 用户电话 |
|     image     |  头像  |
|     email     | 用户邮箱 |
|  read_times   | 阅读次数 |
|  love_times   | 喜欢次数 |
| message_times | 评论次数 |


查询返回成功：
`{"message": "success", "data": {"love_times": 1, "phone": "",` `"message_times": 1, "read_times": 1, "user_name": "", "email": "",` `"image": ""}}`

请求失败：`{"message": "failed", "data": {"flag": 0}}`


#### 2-7.用户一周喜欢新闻列表api

链接：`/api/lovelist?userid=000001&time=1&tooken=764bfd755bc07f6871eee104219b2b2c`

链接功能：返回用户详细信息
|   参数   |   说明    |
| :----: | :-----: |
| userid |  用户编号   |
|  time  |  验证时间戳  |
| token  | 身份验证字符串 |

**参数返回：**
参数返回说明：
|      参数       |  说明  |
| :-----------: | :--: |
|    news_id    | 新闻编号 |
|     title     | 新闻标题 |
|   abstract    | 新闻摘要 |
|     time      |  时间  |
|     image     | 新闻图片 |
|      tag      | 新闻标签 |
|  read_times   | 阅读次数 |
|  love_times   | 喜欢次数 |
| message_times | 评论次数 |


查询返回成功：
`{"message": "success",data": [{"comment_times": 0, "image": "", "tag": "", "time": "", "title": "", "love_times": 3, "news_id": "", "abstract": "", "read_times": 7}]}`

请求失败：`{"message": "failed", "data": {"flag": 0}}`




#### 2-8.热点新闻（每天喜欢/阅读/评论次数最多）api

链接：`/api/hotlist?hot=1&time=1&tooken=764bfd755bc07f6871eee104219b2b2c`

链接功能：返回用户详细信息
|    参数     |       说明       |
| :-------: | :------------: |
|    hot    | 1为喜欢/2为阅读/3为评论 |
|   count   |      请求数量      |
| alrequest |     已请求数量      |
|   time    |     验证时间戳      |
|   token   |    身份验证字符串     |

**参数返回：**
参数返回说明：
|      参数       |  说明  |
| :-----------: | :--: |
|    news_id    | 新闻编号 |
|     title     | 新闻标题 |
|   abstract    | 新闻摘要 |
|     time      |  时间  |
|     image     | 新闻图片 |
|      tag      | 新闻标签 |
|  read_times   | 阅读次数 |
|  love_times   | 喜欢次数 |
| message_times | 评论次数 |


查询返回成功：
`{"message": "success",data": [{"comment_times": 0, "image": "", "tag": "", "time": "", "title": "", "love_times": 3, "news_id": "", "abstract": "", "read_times": 7}]}`

请求失败：`{"message": "failed", "data": {"flag": 0}}`


#### 2-9.喜欢api

链接：`/api/lovenews?newsid=x&userid=x&islove=x&time=x&tooken=x`

链接功能：用户登录
|   参数   |     说明      |
| :----: | :---------: |
| newsid |    新闻编号     |
| userid |    用户编号     |
| islove | 1为喜欢/0为取消喜欢 |
|  time  |     时间      |
| token  |   身份验证字符串   |

**参数返回：**

喜欢成功：`{"message": "success", "data": {"flag": 1}}`

取消喜欢：`{"message": "success", "data": {"flag": 2}}`

请求失败：`{"message": "failed", "data": {"flag": 0}}`


#### 2-10.反馈api

链接：`/api/feedback?userid=x&feedback=x`
`&email=x&time=1&tooken=x`

链接功能：返回用户详细信息
|    参数    |   说明    |
| :------: | :-----: |
|  userid  |  用户编号   |
| feedback |  反馈内容   |
|   time   |  验证时间戳  |
|  token   | 身份验证字符串 |

**参数返回：**

喜欢成功：`{"message": "success", "data": {"flag": 1}}`

请求失败：`{"message": "failed", "data": {"flag": 0}}`


#### 2-11.关键词搜索api

链接：`/api/newstags?keyword=x&time=x&tooken=x`

链接功能：返回新闻列表信息
|   参数    |   说明    |
| :-----: | :-----: |
| keyword |   关键词   |
|  time   |  验证时间戳  |
|  token  | 身份验证字符串 |

**参数返回：**
返回参数说明：
|      参数       |  说明   |
| :-----------: | :---: |
|     time      |  时间   |
|   abstract    |  摘要   |
|     title     |  标题   |
| comment_times | 评论次数  |
|  read_times   | 阅读次数  |
|  love_times   | 喜欢次数  |
|    news_id    | 新闻编号  |
|     image     | 图片url |
|    source     |  来源   |
查询返回成功：
`{"message": "success", "data": [{"time": "", "abstract": "", "title": "",` `"comment_times": 1, "read_times": 1, "love_times": 1, "news_id": "",` `"image": "", "source": ""}, {"time": "", "abstract": "", "title": "",` `"comment_times": 2, "read_times": 2, "love_times": 2, "news_id": "",` `"image": "", "source": ""}]}`

请求失败：
`{"message": "failed", "data": {"flag": 0}}`


#### 2-12.评论api

链接：`/api/comment?userid=x&newsid=x&content=x&time=x&tooken=x`

链接功能：返回新闻列表信息
|   参数    |   说明    |
| :-----: | :-----: |
| userid  |  用户编号   |
| newsid  |  新闻编号   |
| content |  评论内容   |
|  time   |  验证时间戳  |
|  token  | 身份验证字符串 |

**参数返回：**
返回参数说明：
|      参数      |   说明   |
| :----------: | :----: |
|  user_image  | 评论用户头像 |
|   user_id    | 评论用户编号 |
|  user_name   | 评论用户昵称 |
| comment_time |  评论时间  |
|   content    |  评论内容  |
|   news_id    |  新闻编号  |
查询返回成功：
`{"message": "success", "data": {"user_image": "", "user_id": "", "user_name": "", "comment_time": "", "content": "", "news_id": ""}}`

请求失败：
`{"message": "failed", "data": {"flag": 0}}`


#### 2-13.点赞评论api

链接：`/api/feedback?userid=x&feedback=x`
`&email=x&time=1&tooken=x`

链接功能：返回用户详细信息
|     参数      |   说明    |
| :---------: | :-----: |
|   userid    |  用户编号   |
|   newsid    |  新闻编号   |
|   comment   |  该评论内容  |
| commenttime |  该评论时间  |
|    time     |  验证时间戳  |
|    token    | 身份验证字符串 |

**参数返回：**

喜欢成功：`{"message": "success", "data": {"flag": 1}}`

请求失败：`{"message": "failed", "data": {"flag": 0}}`
