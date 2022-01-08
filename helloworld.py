import csv
from os import remove
from PIL import ImageColor

import streamlit as st
from Mondrian import Mondrian


st.sidebar.title("AutoPiet")

def main():
    # Download best configuration
    # To do : Inputs config from Web Page
    path_pallete="./inputs/palette.csv"
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

    st.sidebar.image("./static/image/Mondrian_4_Candy.png",
        caption=f"ex) Decompositoin by Candy's AutoPiet",
        #use_column_width=True,
        width=200)

    name = st.sidebar.text_input('Name', 'User')
    color_1 = st.sidebar.color_picker("Color 1", value="#CE2E2E", key=None, help=None, on_change=None, args=None, kwargs=None)
    color_2 = st.sidebar.color_picker("Color 2", value="#0A24CA", key=None, help=None, on_change=None, args=None, kwargs=None)
    color_3 = st.sidebar.color_picker("Color 3", value="#F7D31E", key=None, help=None, on_change=None, args=None, kwargs=None)

    color_dict["Color_1"] = [float(p/255) for p in list(ImageColor.getcolor(color_1, "RGB"))]
    color_dict["Color_2"] = [float(p/255) for p in list(ImageColor.getcolor(color_2, "RGB"))]
    color_dict["Color_3"] = [float(p/255) for p in list(ImageColor.getcolor(color_3, "RGB"))]

    property_dict["color_list"] = ["Color_1", "Color_2", "Color_3"]

    m = Mondrian(color_dict=color_dict, property_dict=property_dict)

    if st.sidebar.button('Run'):
        default = False
        image_out, _ = m.make_figure(0, name=name, save=True)
        st.image("./static/image/Mondrian_0_"+name+".png",
                 caption=f"Decompositoin by {name}'s AutoPiet",
                 #use_column_width=True,
                 width=600)
        remove("./static/image/Mondrian_0_"+name+".png")

if __name__ == "__main__":
    main()