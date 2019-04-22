# FelKub-Movie-Archive 费库电影系统

## 项目依赖 *Developed Dependencies*
- Qt (PyQt)
- MongoDB

## 命名由来 *Why FelKub?*
- FelKub = Fellini + Kubrick，谨以此名来表达对个人最喜爱的两名导演费里尼和库布里克的尊敬，中文代号费库即简单音译。
- *FelKub = Fellini + Kubrick, I humbly choose this name as a tribute to two of my favorite directors, 
apologies for poor English... English version is on its way..*

## 准备工作 *Preparations*

- 首先确保MongoDB数据库顺利安装，开启MongoDB服务后通过根目录下initiate_data.sh来批量导入数据
- 使用pip安装pyqt和pymongo, 或运行根目录下install_dependant_libs.sh
- 使用start.sh来启动

- *Please make sure that MongoDB is successfully installed, then you may open it and import the data by 
running initiate_data.sh at the root directory.*
- *Using pip or other tools to install PyQt and PyMongo, or simply running install_dependant_libs.sh, but we cannot promise 
that it will work.*
- *Run the app using start.sh.*

## 功能特性 *Supported Functions*

- 所有电影条目检索，支持根据上映年份、豆瓣评分、观看人数、电影长度进行降序或升序排列；
- 支持简单的标题模糊查询和高级的查询，即根据上映年份、豆瓣评分和电影长度进行综合查询；
- 电影详情页面，包括对各项属性的链接和相关推荐；
- 包含多种推荐模式，包括基于电影特征评价、相同的导演和演员、相同的类别和标签；
- 支持电影分类的展示和特定分类的电影查询；
- 支持对于电影特征的修改和查询；
- 所有导演和主演条目的检索，支持根据平均评分、平均观看人数、总观看人数、平均活跃时期进行降序或生序排列；
- 导演和主演详情界面，包括基础信息和电影作品的展示。

- *Retrieving all movie items, and supports sorting by Year, Rating on Douban, Number of People who have watched, Length in descending or ascending order.*
- *Basic fuzzy search on movie title and advanced search, which supports searching by Year, Rating and Length.*
- *Movies Detail page, including link to many attributes and related recommendation.*
- *Many available algorithms in recommending, include recommendation based on movie traits, same directors, same stars, same genres and same tags.*
- *Display on genres and retrieving movies by different genres.*
- *Retrieving all directors and actors who have starred in some films, and support sorting them by average rating, average watched number, watched number in total, average active years in descending or ascending order.*
- *Detail pages of directors and stars, including basic info and display on their works.*

## 功能展示 *Displays*
### 电影检索界面 *Movies Retrieval*
![image](screenshots/gifs/all_movies51.gif)
- 全部电影检索页面支持四种排序根据的升序和降序排列，翻页和首尾页功能齐全。鼠标点击后可以进入详情界面，悬停则可以查看电影的属性。
- *Movies retrieval page supports sorting in descending and ascending order on four dimension and paging function. Click to go into detail page, hover to see traits.* 
### 电影标题搜索 + 高级搜索 *Fuzzy title search and Advanced search*
![image](screenshots/gifs/search.gif)
- 支持根据电影标题进行模糊搜索，也支持根据其他信息进行高级搜索。
- Support fuzzy search on title and advanced search on other attributes.
### 电影详情界面 *Movie Detail*
![image](screenshots/gifs/movie_detail27.gif)
- 电影详情包括电影的基础信息和短评。
- Movies detail page include basic info and short comment.
### 电影推荐功能 *Recommendation Page*
![image](screenshots/gifs/recommendation42.gif)
- 根据电影特征属性、相似的影人和相同的标签与类别进行推荐。
- Recommendation by distance on traits vector, similar directors or stars and similar tags and genres.
### 全部导演界面 *Directors Retrival*
![image](screenshots/gifs/directors22.gif)
- 全部导演界面支持根据四种属性进行升序和降序排序。
- Directors retrival page supports sorting in two directions and four dimensions as well. 
### 全部演员界面 *Stars Retrieval*
![image](screenshots/gifs/celebrities39.gif)
- 全部演员界面也支持根据四种属性进行升序和降序排序。
- Stars retrieval page supports sorting in two directions and four dimensions as well. 
### 影人详情界面 *Detail Pages for Directors and Stars*
![image](screenshots/gifs/directors_celeb_detail44.gif)
- 影人详情界面包括基础信息和参加的电影条目信息。
- Directors and stars detail page include basic info and movies that he or she had participated in.
### 电影分类界面。*Genres Page*
![image](screenshots/gifs/genres17.gif)
- 包括所有可用的电影分类，点击后会检索此类电影。
- Include all available genres, and could retrieve movies of some particular genre on click.





