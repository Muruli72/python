# # import streamlit as st
# # import pandas as pd 
# # import numpy as np

# # ## Title for the applications
# # st.title("Hello streamlit")
# # st.write("Welcome to my first app")

# import streamlit as st

# st.title("My First Streamlit App")

# name = st.text_input("Enter your name")


# age=st.slider("Select you age:",0,100,15)

# if name:
#     st.success(f"Hello, {name}! ")
import streamlit as st
import numpy as np
import pandas as pd

data = np.random.randn(10, 3)

df = pd.DataFrame(data, columns=["A", "B", "C"])

st.dataframe(df)

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["Python", "Java", "C++"]
)

# st.line_chart(chart_data)
# st.bar_chart(chart_data)
# st.area_chart(chart_data)
chart_type = st.selectbox(
    "Select Chart",
    ["Line", "Bar", "Area"]
)

if chart_type == "Line":
    st.line_chart(chart_data)

elif chart_type == "Bar":
    st.bar_chart(chart_data)

else:
    st.area_chart(chart_data)

language = st.radio(
    "Choose a language",
    ["Python", "Java", "C++"]
)

st.write("You selected:", language)

if st.button("Click Me"):
    st.balloons()