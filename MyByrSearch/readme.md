##功能
利用论坛网页接口（？）对用户id或者标题title进行搜索，返回包含该关键字的帖子的发帖时间，链接，以及标题。

**暂时只支持进行英文id和title搜索**，并未对中文搜索进行适配（应该用urlencode编码一下就可以了，吧）

可能是网页搜索的问题，搜索title总是搜不出结果来，遇到bug再改

##Python版本及用到的库
- Python 2.7
- requests
- BeautifulSoup
- re
