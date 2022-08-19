import os
import argparse
import requests
import imageio
from PIL import Image


class CheersUP():

    duration = 50    # 1秒20帧

    def __init__(self):
        self.temp_dir = "temp"
        self.make_dir(self.temp_dir)
        self.resouces_dir = f"{self.temp_dir}/resouces"
        self.make_dir(self.resouces_dir)
        self.couple_distance = 0
        self.repeat = False

    def make_dir(self, path):
        ''' 创建目录 '''
        if not os.path.exists(path):
            os.mkdir(path)

    def download_image(self, image_url):
        ''' 下载图片 '''
        image_name = image_url.split("/")[-1]
        image_path = f"{self.resouces_dir}/{image_name}"
        if os.path.exists(image_path):
            return
        image = requests.get(image_url).content
        with open(image_path, "wb") as f:
            f.write(image)
            f.close()

    def download_resouces(self, config_url):
        ''' 下载资源，返回资源配置文件 '''
        config = requests.get(config_url).json()
        for avatar in config["avatar"]:
            self.download_image(avatar["img"])
        for banner in config["animation"]:
            self.download_image(banner["img"])
        return config

    def get_res_image(self, image_url):
        ''' 获取本地资源图片 '''
        res_image_name = image_url.split("/")[-1]
        res_image = Image.open(f"{self.resouces_dir}/{res_image_name}")
        return res_image

    def get_crop_image(self, res_image, frame, margin=0):
        ''' 获取切割的图片 '''
        image = res_image.crop((
            frame["x"] + margin,
            frame["y"] + margin,
            frame["x"] + frame["width"] - margin,
            frame["y"] + frame["height"] - margin,
        ))
        return image

    def get_bg_color(self, res_image, frame):
        ''' 获取背景颜色 '''
        image = self.get_crop_image(res_image, frame)
        pixels = image.load()
        bg_color = pixels[200, 170]
        return bg_color

    # ============================================================

    def save_avatar_png(self, image):
        ''' 保存avatar逐帧图片 '''
        bg_image = Image.new("RGB", image.size, (255, 255, 255))
        bg_image.paste(image, image)
        bg_image.save(f"{self.avatar_dir}/{self.index}.png")
        self.index += 1

    def save_avatar_gif(self, config):
        ''' 保存avatar动态图片 '''
        self.avatar_dir = f"{self.temp_dir}/avatar"
        self.make_dir(self.avatar_dir)
        self.index = 0
        margin = 27
        for avatar in config["avatar"]:
            res_image = self.get_res_image(avatar["img"])
            # 等待banner动画消失
            if avatar["delay"] > 0:
                delay_frame = 3000 // self.duration
                for i in range(delay_frame):
                    image = self.get_crop_image(res_image, avatar["frames"][0], margin)
                    self.save_avatar_png(image)
            # 生成avatar动画图片
            for frame in avatar["frames"]:
                image = self.get_crop_image(res_image, frame, margin)
                self.save_avatar_png(image)
        # 保存gif图片
        images = []
        for i in range(self.index):
            images.append(imageio.v3.imread(f"{self.avatar_dir}/{i}.png"))
        imageio.mimsave("avatar.gif", images, duration=self.duration/1000)

    # ============================================================

    def save_banner_png(self, image, bg_color, position):
        ''' 保存banner逐帧图片 '''
        bg_image = Image.new("RGB", (600, 240), bg_color)
        x = 0
        if position == 0:
            x = (bg_image.size[0] - image.size[0]) // 2
        elif position == 1:
            x = bg_image.size[0] - image.size[0]
        y = bg_image.size[1] - image.size[1] - 10
        bg_image.paste(image, (x, y), mask=image)
        bg_image.save(f"{self.banner_dir}/{self.index}.png")
        self.index += 1

    def save_banner_gif(self, config):
        ''' 保存banner动态图片 '''
        self.banner_dir = f"{self.temp_dir}/banner"
        self.make_dir(self.banner_dir)
        self.index = 0
        banner = config["animation"][0]
        res_image = self.get_res_image(banner["img"])
        # 从第7帧获取背景颜色
        bg_color = self.get_bg_color(res_image, banner["frames"][7])
        # 人物交替出现在两个位置
        for position in range(2):
            # 等待avatar人物消失
            delay_frame = banner["delay"] // self.duration
            for i in range(delay_frame):
                image = self.get_crop_image(res_image, banner["frames"][0])
                self.save_banner_png(image, bg_color, position)
            # banner人物出现及消失
            for frame in banner["frames"]:
                image = self.get_crop_image(res_image, frame)
                self.save_banner_png(image, bg_color, position)
            # 等待avatar人物出现
            for i in range(delay_frame):
                image = self.get_crop_image(res_image, banner["frames"][0])
                self.save_banner_png(image, bg_color, position)
        # 保存gif图片
        images = []
        for i in range(self.index):
            images.append(imageio.v3.imread(f"{self.banner_dir}/{i}.png"))
        imageio.mimsave("banner.gif", images, duration=self.duration/1000)

    # ============================================================

    def save_cheers_png(self, image, bg_color):
        ''' 保存干杯逐帧图片 '''
        bg_image = Image.new("RGB", image.size, bg_color)
        bg_image.paste(image, (0, 0), mask=image)
        bg_image.save(f"{self.cheers_dir}/{self.index}.png")
        self.index += 1

    def save_cheers_gif(self, config):
        ''' 保存干杯动态图片 '''
        self.cheers_dir = f"{self.temp_dir}/cheers"
        self.make_dir(self.cheers_dir)
        self.index = 0
        banner = config["animation"][0]
        res_image = self.get_res_image(banner["img"])
        # 从第7帧获取背景颜色
        bg_color = self.get_bg_color(res_image, banner["frames"][7])
        # 干杯动画
        for frame in banner["frames"]:
            image = self.get_crop_image(res_image, frame)
            self.save_cheers_png(image, bg_color)
        # 保存gif图片
        images = []
        image_range = range(23, 44) if self.repeat else range(self.index)
        for i in image_range:
            images.append(imageio.v3.imread(f"{self.cheers_dir}/{i}.png"))
        imageio.mimsave("cheers.gif", images, duration=self.duration/1000)

    # ============================================================

    def save_couple_png(self, image1, image2, bg_color):
        ''' 保存情侣图逐帧图片 '''
        distance = 75 - self.couple_distance
        bg_image = Image.new("RGB", (500, 200), bg_color)
        # 翻转左边的图片
        image1 = image1.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        x = bg_image.size[0] // 2 - image1.size[0] + distance
        y = bg_image.size[1] - image1.size[1] - 0
        bg_image.paste(image1, (x, y), mask=image1)
        # 添加右边的图片
        x = bg_image.size[0] // 2 - distance
        bg_image.paste(image2, (x, y), mask=image2)
        bg_image.save(f"{self.couple_dir}/{self.index}.png")
        self.index += 1

    def save_couple_gif(self, config1, config2):
        ''' 保存情侣图动态图片 '''
        self.couple_dir = f"{self.temp_dir}/couple"
        self.make_dir(self.couple_dir)
        self.index = 0
        banner = config1["animation"][0]
        res_image1 = self.get_res_image(config1["animation"][0]["img"])
        res_image2 = self.get_res_image(config2["animation"][0]["img"])
        # 获取两个背景图片颜色的平均值
        bg_color1 = self.get_bg_color(res_image1, banner["frames"][7])
        bg_color2 = self.get_bg_color(res_image2, banner["frames"][7])
        bg_color = tuple([(bg_color1[i] + bg_color2[i])//2 for i in range(3)])
        # 合成图片
        for frame in banner["frames"]:
            image1 = self.get_crop_image(res_image1, frame)
            image2 = self.get_crop_image(res_image2, frame)
            self.save_couple_png(image1, image2, bg_color)
        # 保存gif图片
        images = []
        image_range = range(23, 44) if self.repeat else range(self.index)
        for i in image_range:
            images.append(imageio.v3.imread(f"{self.couple_dir}/{i}.png"))
        imageio.mimsave("couple.gif", images, duration=self.duration/1000)

    def test(self):
        url1 = "http://s1.hdslb.com/bfs/static/baselabs/json/9562e7646ba4bf5961cc8278615c10d47499c1a6.json"
        url2 = "http://i0.hdslb.com/bfs/baselabs/a1c1d0406601836f9375543ae96f7c32fbee49b3.plain"
        config1 = cup.download_resouces(url1)
        config2 = cup.download_resouces(url2)
        self.save_avatar_gif(config2)
        self.save_banner_gif(config2)
        self.save_cheers_gif(config2)
        cup.save_couple_gif(config1, config2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CheersUP")
    parser.add_argument('--version', '-v', action='version',
                        version='version: v1.0.0',
                        help='查看当前版本号')
    parser.add_argument('--avatar', '-a',
                        action='store_true',
                        help='生成头像gif图片',
                        default=False)
    parser.add_argument('--banner', '-b',
                        action='store_true',
                        help='生成横幅gif图片',
                        default=False)
    parser.add_argument('--cheers', '-c',
                        action='store_true',
                        help='生成干杯gif图片',
                        default=False)
    parser.add_argument('--couple', '-cp',
                        action='store_true',
                        help='生成情侣gif图片',
                        default=False)
    parser.add_argument('--distance', '-dd',
                        type=int,
                        help='调整情侣gif人物之间的距离（负靠近，正远离）',
                        default=None)
    parser.add_argument('--repeat', '-r',
                        action='store_true',
                        help='重复显示干杯动画，生成cheers和couple动画时有效',
                        default=False)
    parser.add_argument('--urls', '-u',
                        nargs='+',
                        type=str,
                        help='配置文件地址',
                        default=None)
    args = parser.parse_args()

    if not args.urls:
        print("请输入配置文件地址")
        exit()

    cup = CheersUP()
    if args.repeat:
        cup.repeat = True
    if args.distance:
        cup.couple_distance = args.distance
    if args.avatar:
        config = cup.download_resouces(args.urls[0])
        cup.save_avatar_gif(config)
    if args.banner:
        config = cup.download_resouces(args.urls[0])
        cup.save_banner_gif(config)
    if args.cheers:
        config = cup.download_resouces(args.urls[0])
        cup.save_cheers_gif(config)
    if args.couple:
        if len(args.urls) < 2:
            print("请输入两个配置文件地址")
            exit()
        config1 = cup.download_resouces(args.urls[0])
        config2 = cup.download_resouces(args.urls[1])
        cup.save_couple_gif(config1, config2)

