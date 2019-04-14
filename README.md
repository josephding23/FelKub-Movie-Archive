# FelKub-Movie-Archive 费库电影系统
### 命名由来
FelKub = Fellini + Kubrick，谨以此名来表达对个人最喜爱的两名导演费里尼和库布里克的尊敬，中文代号费库即简单音译。

### 准备工作

- 首先确保MongoDB数据库顺利安装，再点击datas目录下的mongod批处理文件来批量载入数据
- 使用pip安装pyqt和pymong

### 功能特性

- 所有电影条目检索，支持根据上映年份、豆瓣评分、观看人数、电影长度进行降序或升序排列；
- 支持简单的标题模糊查询和高级的查询，即根据上映年份、豆瓣评分和电影长度进行综合查询；
- 电影详情页面，包括对各项属性的链接和相关推荐；
- 包含多种推荐模式，包括基于电影特征评价、相同的导演和演员、相同的类别和标签；
- 支持电影分类的展示和特定分类的电影查询；
- 支持对于电影特征的修改和查询；
- 所有导演和主演条目的检索，支持根据平均评分、平均观看人数、总观看人数、平均活跃时期进行降序或生序排列；
- 导演和主演详情界面，包括基础信息和电影作品的展示。

### 功能展示
- ##### 全部电影界面
![image](screenshots/gifs/all_movies51.gif)
全部电影检索页面支持四种排序根据的升序和降序排列，翻页和首尾页功能齐全。鼠标点击后可以进入详情界面，悬停则可以查看电影的属性。
- ##### 电影标题搜索 + 高级搜索
![image](screenshots/gifs/search.gif)
支持根据电影标题进行模糊搜索，也支持根据其他信息进行高级搜索。
- ##### 电影详情界面
![image](screenshots/gifs/movie_detail27.gif)
高级搜索包括电影的基础信息和短评。
- ##### 电影推荐功能
![image](screenshots/gifs/recommendation42.gif)
根据电影特征属性、相似的影人和相同的标签与类别进行推荐。
- ##### 全部导演界面
![image](screenshots/gifs/directors22.gif)
全部导演界面支持根据四种属性进行升序和降序排序。
- ##### 全部演员界面
![image](screenshots/gifs/celebrities39.gif)
全部演员界面也支持根据四种属性进行升序和降序排序。
- ##### 影人详情界面
![image](screenshots/gifs/directors_celeb_detail44.gif)
影人详情界面包括基础信息和参加的电影条目信息。
- ##### 电影分类界面。
![image](screenshots/gifs/genres17.gif)
包括所有可用的电影分类，点击后会检索此类电影。


### 开发平台
- Qt (PyQt)
- MongoDB


