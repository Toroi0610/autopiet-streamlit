import csv

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

    m = Mondrian(color_dict=color_dict, property_dict=property_dict)

    name = st.sidebar.text_input('Name', 'User')
    if st.sidebar.button('Run'):
        image_out, _ = m.make_figure(0, name=name, save=True)
        st.image("./static/image/Mondrian_0_"+name+".png",
                 caption=f"Decompositoin by {name}'s AutoPiet",
                 #use_column_width=True,
                 width=600)

if __name__ == "__main__":
    main()