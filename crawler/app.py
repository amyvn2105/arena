import streamlit as st
import pandas as pd
from crawler.handler import Handler, DESTINATION, PREFIX
from datetime import datetime


def crawl_tiki_product(handler):
    handler._crawl()
    handler._transform()
    handler._export_to_excel()
    handler._load()

def get_path(product):
    date = datetime.now().strftime('%Y/%m/%d')
    path = f'{PREFIX}/{DESTINATION}/{date}/{product}.xlsx'
    return path

if __name__ == "__main__":
    handler = Handler()

    st.set_page_config(page_title='Smart Crawler')
    st.title('Smart Crawler')
    # st.subheader('I can crawl all products on Tiki')
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

    product_input = st.text_input('Please enter a product')
    st.markdown('----------------')

    if product_input:
        handler.product = product_input
        crawl_tiki_product(handler=handler)
        path = get_path(product=product_input)
        df = pd.read_excel(path, engine='openpyxl')
        st.dataframe(df)

