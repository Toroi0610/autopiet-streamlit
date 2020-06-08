# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 21:06:42 2018

@author: Toroi
"""

import csv

# import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
fp_name = FontProperties(fname=r'./static/fonts/BRADHITC.TTF', size=25)
import sys
sys.setrecursionlimit(10000)

class Mondrian():
    def __init__(self, color_dict, property_dict, name=None):
        """

        キャンバス作り

        1. すべて0の配列によって真っ白の画像を作成
        2. 画像の縁に色を付ける．(line_colorによって色は変わる．)
        3. 配列上のどこかにランダムに点を置く．
        4. 置いた点から上下左右の4方向，あるいはそのうちの一つを除いた3方向に線を伸ばす．
        5. num_pointの数だけそれらを行う．

        この時点で，白い画像の上に色のついた線がいくつか伸びており，四角形の領域がいくつか出来る．

        塗りつぶし

        6. 画像上のどこかにランダムに点を置く．
        7. その点が含まれる四角形の領域全体をcolorlistの色で塗る．
        8. sum(num_color_reigion)の数だけそれらを繰り返す．

        終了

        """

        # 節の数
        self.num_point = int(property_dict["num_cross_point"][0])

        # 黒線が伸びる方向に応じた発生確率
        self.prob_shape = list(map(float, property_dict["prob_shape"]))

        # 画像の各画素の情報
        self.matsize = list(map(int, property_dict["size"]))

        # 画像の大きさ
        self.figsize = list(map(float, property_dict["figure_size"]))

        # 線の色
        self.line_color = color_dict[property_dict["color_of_line"][0]]

        # 線の太さ
        self.line_width = int(property_dict["line_width"][0])

        # 四角形の中を塗りつぶす色のリスト
        self.colorlist = [color_dict[color] for color in property_dict["color_list"]]

        # 色を付ける領域の数(colorlistの順番に対応)
        self.num_color_region = list(map(int, property_dict["num_color"]))

        # 四隅を削る大きさ
        self.diamond_length = int(property_dict["diamond_length"][0])

        # 分断線の太さ
        self.devide_line_width = list(map(float, property_dict["devide_line_width"]))

        # 分断線の太さ
        self.prob_devide = list(map(float, property_dict["prob_devide"]))

        # 名前
        if name == None:
            self.name = property_dict["name"][0]
        else:
            self.name = name


    def decide_shape(self):
        sumation = sum(self.prob_shape)
        prob = np.cumsum(np.array(self.prob_shape)/sumation)
        rand = np.random.rand(self.num_point)
        return np.array([np.argmin(value>prob) for value in rand])


    def decide_line_width(self):
        # 横線の太さ，縦線の太さ
        # これを節の数だけ作る．
        # 確率を長さに変換
        # 2* num_pointのnumpy array
        sumation = sum(self.prob_devide)
        prob = np.cumsum(np.array(self.prob_devide)/sumation)
        rand = np.random.rand(2 * self.num_point)
        decision = np.array([np.argmin(value>prob) for value in rand])
        return decision.reshape([2, self.num_point])


    def make_property(self):
        points = np.c_[np.random.randint(0, self.matsize[0]-max(self.devide_line_width),size=(self.num_point)),
                       np.random.randint(0, self.matsize[1]-max(self.devide_line_width),size=(self.num_point))]
        shapes = self.decide_shape()
        width = self.decide_line_width()

        return np.c_[points, np.c_[shapes, width]]


    def decide_point(self, fig_mat):
        point = np.r_[np.random.randint(2,self.matsize[0]-2),np.random.randint(2,self.matsize[1]-2)]
        if np.sum(fig_mat[point[0],point[1]]) == 3:
            return point
        else:
            return self.decide_point(fig_mat)


    def decide_region(self,fig_mat, point):
        #上端
        row_upper = self.decide_line(fig_mat, np.copy(point[0]), np.copy(point[1]), "upper")
        row_lower = self.decide_line(fig_mat, np.copy(point[0]), np.copy(point[1]), "lower")
        col_left = self.decide_line(fig_mat, np.copy(point[0]), np.copy(point[1]), "left")
        col_right = self.decide_line(fig_mat, np.copy(point[0]), np.copy(point[1]), "right")

        return row_upper, row_lower, col_left, col_right


    def decide_line(self, fig_mat, row, col, sup = "upper"):
        if sup == "upper":
            if np.sum(fig_mat[row, col] == self.line_color)!=3:
                return self.decide_line(fig_mat, row-1, col, sup)
            else:
                return row+1
        if sup == "lower":
            if np.sum(fig_mat[row, col] == self.line_color)!=3:
                return self.decide_line(fig_mat, row+1, col, sup)
            else:
                return row
        if sup == "left":
            if np.sum(fig_mat[row, col] == self.line_color)!=3:
                return self.decide_line(fig_mat, row, col-1, sup)
            else:
                return col+1
        if sup == "right":
            if np.sum(fig_mat[row, col] == self.line_color)!=3:
                return self.decide_line(fig_mat, row, col+1, sup)
            else:
                return col


    def set_color(self, fig_mat):
        color_and_num_list = []
        for k, num_color in enumerate(self.num_color_region):
            for i in range(num_color):
                color_and_num_list.append(self.colorlist[k])

        for i in range(len(color_and_num_list)):
            point = self.decide_point(fig_mat)
            r_u, r_l, c_l, c_r = self.decide_region(fig_mat, point)
            s = np.ones([r_l-r_u, c_r-c_l])
            fig_mat[r_u:r_l, c_l:c_r, 0] = s*color_and_num_list[i][0]
            fig_mat[r_u:r_l, c_l:c_r, 1] = s*color_and_num_list[i][1]
            fig_mat[r_u:r_l, c_l:c_r, 2] = s*color_and_num_list[i][2]


        return fig_mat


    def set_diamond(self, fig_mat):
        for i in range(self.diamond_length):
            for j in range(self.diamond_length-i):
                fig_mat[i,j] = [0,0,0]
                fig_mat[i,self.matsize[1]-j-1] = [0,0,0]
                fig_mat[self.matsize[0]-i-1,j] = [0,0,0]
                fig_mat[self.matsize[0]-i-1,self.matsize[1]-j-1] = [0,0,0]
        return fig_mat



    def make_figure(self, image_num, mongon="", save=True):
        fig_mat = np.ones([self.matsize[0],self.matsize[1], 3], dtype='float32')
        points_and_shapes = self.make_property()
        row_line = np.ones([1, self.matsize[1],3])*self.line_color
        column_line = np.ones([self.matsize[0], 1, 3])*self.line_color

        fig_mat[:self.line_width] = row_line
        fig_mat[-self.line_width-1:] = row_line
        fig_mat[:,:self.line_width] = column_line
        fig_mat[:,-self.line_width-1:] = column_line

        """
        plt.figure(figsize=self.figsize, frameon=False)
        plt.imshow(fig_mat)
        plt.axis('off')
        plt.tight_layout(pad=0)
        plt.savefig("../images/Mondrian_"+str(image_num)+mongon+str(aaa)+".png", transparent = True, bbox_inches = 'tight', pad_inches = 0)
        plt.show()
        """
        aaa = self.line_width

        for point_and_shape in points_and_shapes:
            if point_and_shape[2] == 0:
                fig_mat[point_and_shape[0]:point_and_shape[0]+point_and_shape[3]] = row_line
                fig_mat[:,point_and_shape[1]:point_and_shape[1]+point_and_shape[4]] = column_line
            if point_and_shape[2] == 1:
                fig_mat[point_and_shape[0]:point_and_shape[0]+point_and_shape[3]] = row_line
                fig_mat[point_and_shape[0]:,point_and_shape[1]:point_and_shape[1]+point_and_shape[4]] = column_line[point_and_shape[0]:]
            if point_and_shape[2] == 2:
                fig_mat[point_and_shape[0]:point_and_shape[0]+point_and_shape[3],:point_and_shape[1]] = row_line[:, :point_and_shape[1]]
                fig_mat[:,point_and_shape[1]:point_and_shape[1]+point_and_shape[4]] = column_line
            if point_and_shape[2] == 3:
                fig_mat[point_and_shape[0]:point_and_shape[0]+point_and_shape[3]] = row_line
                fig_mat[:point_and_shape[0],point_and_shape[1]:point_and_shape[1]+point_and_shape[4]] = column_line[:point_and_shape[0]]
            if point_and_shape[2] == 4:
                fig_mat[point_and_shape[0]:point_and_shape[0]+point_and_shape[3],point_and_shape[1]:] = row_line[: ,point_and_shape[1]:]
                fig_mat[:,point_and_shape[1]:point_and_shape[1]+point_and_shape[4]] = column_line
            """
            plt.imshow(fig_mat)
            plt.axis('off')
            plt.tight_layout(pad=0)
            plt.savefig("../images/Mondrian_"+str(image_num)+mongon+str(aaa)+".png", transparent = True, bbox_inches = 'tight', pad_inches = 0)
            plt.show()
            """
            aaa += 1

        fig_mat = self.set_color(fig_mat)
        fig_mat = self.set_diamond(fig_mat)

        if save:
            fig, ax = plt.subplots(1, 1, figsize=self.figsize, frameon=False)
            ax.imshow(fig_mat)

            if self.name != None:
                ax.text(0.01*self.matsize[1], 0.95*self.matsize[0], self.name, color="black", fontproperties=fp_name)

            plt.axis('off')
            plt.tight_layout(pad=0)
            plt.savefig("./static/image/Mondrian_"+str(image_num)+mongon+".png", transparent = True, bbox_inches = 'tight', pad_inches = 0)
            plt.close()

        return fig_mat, points_and_shapes


if __name__ == '__main__':
    path_pallete="./inputs/palette.csv",
    path_property="./inputs/property.csv"
    
    color_dict = {}
    with open(path_pallete, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for i, row in enumerate(spamreader):
            if i!=0:
                row_sep = row[0].split(",")
                color_dict[row_sep[0]] = list(map(float, row_sep[1:]))

    property_dict = {}
    with open(path_property, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for i, row in enumerate(spamreader):
            if i!=0:
                row_sep = row[0].split(",")
                property_dict[row_sep[0]] = row_sep[1:]


    m = Mondrian(color_dict=color_dict, property_dict=property_dict)

    for i in range(5):
        print(i)
        a, b = m.make_figure(i, "_user", save=False)
