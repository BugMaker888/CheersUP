
[CheersUP](https://github.com/BugMaker888/CheersUP)是一个基于Python3的命令行工具，可以制作动态头像、动态横幅，干杯动画、情侣动态图等。

目前支持的NFT及数字藏品头像：

| 名称         | 类型     | 发行量       | 预览地址 |
| ------------ | :------: | ------------ | -------- |
| CheersUP     | NFT      | 5000 / 10000 | [CheersUP](https://opensea.io/collection/cheers-up) |
| 干杯2022     | 数字藏品 | 7042 / 10000 | [干杯2022](https://www.bilibili.com/blackboard/pangu/nft-collection.html?item_id=1004) |
| 干杯！京剧   | 数字藏品 | 1728 / 1790  | [干杯！京剧](https://www.bilibili.com/blackboard/pangu/nft-collection.html?item_id=1056) |
| 干杯！故宫   | 数字藏品 | 1730 / 2000  | [干杯！故宫](https://www.bilibili.com/blackboard/pangu/nft-collection.html?item_id=1152) |
| 干杯！洛天依 | 数字藏品 | 1967 / 2022  | [干杯！洛天依](https://www.bilibili.com/blackboard/pangu/nft-collection.html?item_id=1234) |


## 工具使用方法

#### 一、安装依赖库

``` bash
$ git clone https://github.com/BugMaker888/CheersUP.git
$ cd CheersUP
$ pip install -r requirements.txt
```

#### 二、查看帮助

``` bash
$ python cup.py --help

usage: cup.py [-h] [--version] [--avatar] [--banner] [--cheers] [--couple]
              [--distance DISTANCE] [--repeat] [--urls URLS [URLS ...]]

CheersUP

optional arguments:
  -h, --help            show this help message and exit
  --version, -v         查看当前版本号
  --avatar, -a          生成头像gif图片
  --banner, -b          生成横幅gif图片
  --cheers, -c          生成干杯gif图片
  --couple, -cp         生成情侣gif图片
  --circulation, -cl    生成恋爱循环gif图片
  --distance DISTANCE, -dd DISTANCE
                        调整情侣gif人物之间的距离（负靠近，正远离）
  --repeat, -r          重复显示干杯动画，生成cheers和couple动画时有效
  --urls URLS [URLS ...], -u URLS [URLS ...]
                        配置文件地址
```

## 使用示例

### 零、获取配置文件地址

按照文章[《CheersUP动态图生成工具》](https://mirror.xyz/bugmaker.eth/tc5kyBHZlM6A6vqBi9xB8UiJtECgIVQNid0GFPXh-wM)的教程获取NFT头像的动画配置文件地址。

我的`NFT`头像的配置文件地址为：`http://i0.hdslb.com/bfs/baselabs/a1c1d0406601836f9375543ae96f7c32fbee49b3.plain`


### 一、制作动态头像 (可用于Discord)

![](https://cdn.jsdelivr.net/gh/BugMaker888/CheersUP/preview/avatar.gif)

``` bash
python cup.py -a -u http://i0.hdslb.com/bfs/baselabs/a1c1d0406601836f9375543ae96f7c32fbee49b3.plain
```

### 二、制作动态横幅 (可用于Discord)

![](https://cdn.jsdelivr.net/gh/BugMaker888/CheersUP/preview/banner.gif)

``` bash
python cup.py -b -u http://i0.hdslb.com/bfs/baselabs/a1c1d0406601836f9375543ae96f7c32fbee49b3.plain
```

### 三、制作干杯动画

#### 1、默认干杯效果：

![](https://cdn.jsdelivr.net/gh/BugMaker888/CheersUP/preview/cheers.gif)

``` bash
python cup.py -c -u http://i0.hdslb.com/bfs/baselabs/a1c1d0406601836f9375543ae96f7c32fbee49b3.plain
```

#### 2、重复干杯效果：

![](https://cdn.jsdelivr.net/gh/BugMaker888/CheersUP/preview/cheers_repeat.gif)

``` bash
python cup.py -c -r -u http://i0.hdslb.com/bfs/baselabs/a1c1d0406601836f9375543ae96f7c32fbee49b3.plain
```

### 四、制作情侣动态图

需要使用两个配置文件地址，第一个显示在左边，第二个显示在右边。

#### 1、默认情侣图效果：

![](https://cdn.jsdelivr.net/gh/BugMaker888/CheersUP/preview/couple.gif)

``` bash
python cup.py -cp -u http://s1.hdslb.com/bfs/static/baselabs/json/9562e7646ba4bf5961cc8278615c10d47499c1a6.json http://i0.hdslb.com/bfs/baselabs/a1c1d0406601836f9375543ae96f7c32fbee49b3.plain 
```

#### 2、情侣图重复干杯效果：

![](https://cdn.jsdelivr.net/gh/BugMaker888/CheersUP/preview/couple_repeat.gif)

``` bash
python cup.py -cp -r -u http://s1.hdslb.com/bfs/static/baselabs/json/9562e7646ba4bf5961cc8278615c10d47499c1a6.json http://i0.hdslb.com/bfs/baselabs/a1c1d0406601836f9375543ae96f7c32fbee49b3.plain 
```

#### 3、减少人物之间的距离：

可以通过`-dd`参数调整人物之间的距离，以下是减少了50像素的效果：

![](https://cdn.jsdelivr.net/gh/BugMaker888/CheersUP/preview/couple-50.gif)

``` bash
python cup.py -cp -dd -50 -u http://s1.hdslb.com/bfs/static/baselabs/json/9562e7646ba4bf5961cc8278615c10d47499c1a6.json http://i0.hdslb.com/bfs/baselabs/a1c1d0406601836f9375543ae96f7c32fbee49b3.plain 
```

#### 4、增加人物之间的距离：

以下是增加了50像素的效果：

![](https://cdn.jsdelivr.net/gh/BugMaker888/CheersUP/preview/couple+50.gif)

``` bash
python cup.py -cp -dd 50 -u http://s1.hdslb.com/bfs/static/baselabs/json/9562e7646ba4bf5961cc8278615c10d47499c1a6.json http://i0.hdslb.com/bfs/baselabs/a1c1d0406601836f9375543ae96f7c32fbee49b3.plain 
```

### 五、制作恋爱循环动态图

支持2到4个配置文件地址，从3点钟方向开始，按顺时针方向排列。

#### 1、双人恋爱循环效果：

![](https://cdn.jsdelivr.net/gh/BugMaker888/CheersUP/preview/circulation_2.gif)

``` bash
python cup.py -cl -u http://i0.hdslb.com/bfs/baselabs/a1c1d0406601836f9375543ae96f7c32fbee49b3.plain http://i0.hdslb.com/bfs/baselabs/0edc00a83666f149a7db6b5066e90de3618b3ca0.plain
```

#### 2、三人运动效果：

![](https://cdn.jsdelivr.net/gh/BugMaker888/CheersUP/preview/circulation_3.gif)

``` bash
python cup.py -cl -u http://i0.hdslb.com/bfs/baselabs/a1c1d0406601836f9375543ae96f7c32fbee49b3.plain http://i0.hdslb.com/bfs/baselabs/0edc00a83666f149a7db6b5066e90de3618b3ca0.plain http://s1.hdslb.com/bfs/static/baselabs/json/e1de7fa803aba05aea3e93990c68e4e97aaf9cb6.json
```

#### 3、四人运动效果：

![](https://cdn.jsdelivr.net/gh/BugMaker888/CheersUP/preview/circulation_4.gif)

``` bash
python cup.py -cl -u http://i0.hdslb.com/bfs/baselabs/a1c1d0406601836f9375543ae96f7c32fbee49b3.plain http://i0.hdslb.com/bfs/baselabs/0edc00a83666f149a7db6b5066e90de3618b3ca0.plain http://s1.hdslb.com/bfs/static/baselabs/json/e1de7fa803aba05aea3e93990c68e4e97aaf9cb6.json http://s1.hdslb.com/bfs/static/baselabs/json/d045e03d6198b58d4a0f268ee28a0e4ff9f78a93.json
```

