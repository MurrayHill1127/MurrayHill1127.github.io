<h2 style="text-align: center;">过早优化是万恶之源</h2>
<p class="right">July 25, 2024<br />Huai'an</p>

最近在完善我的博客框架，想要添加一个按 `Subject` 分类的功能。

网站结构很简单，`Blog` 下分为 `Archive` 和 `Category` 两个索引页。

  - Archive:  档案，按时间存放所有文章。
  - Category: 分类，按类别存放所有文章。

现在问题是，只设计一级分类不够。例如，学 `OS` 时，同时看 *xv6* 和*《操作系统真相还原》*，就需要二级分类 'OS/xv6' 。

我目前的工作流是这样的：

  1. 按月份建立目录
  2. 在对应目录下创建形如 *0725_Premature-optimization-is-the-root-of-all-evil_Diary.md* 的文件
  3. 编辑完成后执行一个 shell 脚本：
    - 将 markdown 文件 转为 html 文件
    - 解析所有 md 文件文件名，提取日期、标题、分类并生成相应索引页
  4. 推送至 GitHub Pages

因为分类是在文件命名时做的，所以很自然地可以想到改成诸如 *_Diary-x86* 这样的形式。这个想法延续了之前工作的风格，只需修改解析文件名称得到脚本即可。

可是问题又来了，假如二级分类也不够，二级下又有三级，三级下又有四级...还要计算好一共有几级标题，建立对应的目录结构；还需要研究一下 HTML 中嵌套列表相关的东西...似乎很麻烦，感觉压力`山大`。

实际上，博客的初步功能在一周前就写好了，但是这一周却没有正式写一遍文章。一部分原因就是，觉得当前还是一个半成品，想要尽善尽美之后再开始使用。

现在，我觉得不应该这样。目前最好的状态是把网站拿起来使用，每天写文章发文章。至于升级的事情慢慢做。或许积累了一些文章之后，会更有动力写新脚本。

> 过早优化是万恶之源。
> 
> - 高德纳	

---

Today Done:

  1. PA0
  2. *Harley Hahn's Guide to Unix and Linux* 读至第七章

Tomorrow To Do:

  1. Finish ysyx's C tests
  2. Go on PA1
  3. Reading:
    - *Harley Hahn's Guide to Unix and Linux*
	- *Hacking: The art of Exploitation*
	- *GroudUp*
	- *Linkers and Loaders* 
	- *程序员的自我修养*
  4. Learn:
    - *Sid Meier's Civilization VI*
	- *StarCraft II*
