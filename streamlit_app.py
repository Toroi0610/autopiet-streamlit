import csv
from os import remove
from PIL import ImageColor

import streamlit as st
from Mondrian import Mondrian

st.set_page_config(
     page_title='Auto Piet',
     layout="wide",
     initial_sidebar_state="expanded",
)

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

    st.sidebar.image("./static/image/sample.jpeg",
        caption=f"ex) Decompositoin by Candy's AutoPiet",
        #use_column_width=True,
        width=200)

    name = st.text_input('Name', 'User')

    col1, col2, col3 = st.columns(3)
    with col1:
        color_1 = st.color_picker("Color 1", value="#CE2E2E", key=None, help=None, on_change=None, args=None, kwargs=None)
    with col2:
        color_2 = st.color_picker("Color 2", value="#0A24CA", key=None, help=None, on_change=None, args=None, kwargs=None)
    with col3:
        color_3 = st.color_picker("Color 3", value="#F7D31E", key=None, help=None, on_change=None, args=None, kwargs=None)

    color_dict["Color_1"] = [float(p/255) for p in list(ImageColor.getcolor(color_1, "RGB"))]
    color_dict["Color_2"] = [float(p/255) for p in list(ImageColor.getcolor(color_2, "RGB"))]
    color_dict["Color_3"] = [float(p/255) for p in list(ImageColor.getcolor(color_3, "RGB"))]

    property_dict["color_list"] = ["Color_1", "Color_2", "Color_3"]

    width = st.slider("Width", min_value=800, max_value=1600, value=1200, step=80, format=None, key=None, help=None, on_change=None, args=None, kwargs=None)
    height = st.slider("Height", min_value=800, max_value=1600, value=1200, step=80, format=None, key=None, help=None, on_change=None, args=None, kwargs=None)

    property_dict["size"] = [int(height/20), int(width/20)]

    m = Mondrian(color_dict=color_dict, property_dict=property_dict)

    if st.button('Run'):
        default = False
        image_out, _, stream_item = m.make_figure(0, name=name)
        st.image(image_out,
                 caption=f"Decomposition by {name}'s AutoPiet",
                 use_column_width=True,
                 output_format="PNG",
                 width=width)
        # remove("./static/image/Mondrian_0_"+name+".png")
        st.download_button("Download Image", stream_item,
                           file_name=f"{name.replace(' ', '_')}_Decomposition_by_AutoPiet.png",
                           mime=None, key=None,
                           help=None, on_click=None,
                           args=None, kwargs=None)

if __name__ == "__main__":
    main()
