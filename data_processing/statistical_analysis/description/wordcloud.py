from random import randint

import numpy as np
import pandas as pd
from os import path
from PIL import Image
import wordcloud

import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt

file_path = "description.txt"


def random_color_func(word=None, font_size=None, position=None,  orientation=None, font_path=None, random_state=None):
        h  = randint(130, 270)
        s = int(100.0 * 255.0 / 255.0)
        l = int(100.0 * float(randint(60, 120)) / 255.0)
        return "hsl({}, {}%, {}%)".format(h, s, l)


def read_and_sum_lines(file_path):
    # 初始化一个空字符串，用于存储每一行的内容
    lines_sum = ""

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # 去除行末尾的换行符，并将当前行内容追加到总字符串中
                lines_sum += line.strip()

    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None

    return lines_sum


if __name__ == '__main__':

    s = read_and_sum_lines(file_path)

    w = wordcloud.WordCloud(width=1000, height=500,
                            stopwords=wordcloud.STOPWORDS.union(["de", "en"]),
                            collocations=False,
                            max_font_size=150,
                            random_state=30,
                            # color_func=random_color_func,
                            background_color="white")
    w.generate(s)
    w.to_file('wordcloud.pdf')