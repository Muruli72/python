import time
import joblib
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Scam Guard NLP",
    page_icon="🛡️",
    layout="wide"
)

@st.cache_resource
def load_model():
    vectorizer = joblib.load("models/tfidf_vectorizer.pkl")
    model = joblib.load("models/scam_model.pkl")
    return vectorizer, model

@st.cache_data
def load_dataset():
    url = "https://raw.githubusercontent.com/justmarkham/DAT8/master/data/sms.tsv"
    df = pd.read_csv(url, sep="\t", header=None, names=["label", "message"])
    df["label"] = df["label"].map({"ham": "Legitimate", "spam": "Spam"})
    df["character_count"] = df["message"].str.len()
    df["word_count"] = df["message"].str.split().str.len()
    df["avg_word_length"] = df["character_count"] / df["word_count"].replace(0, np.nan)
    return df

def get_top_spam_features(model, vectorizer, top_n=10):
    feature_names = vectorizer.get_feature_names_out()
    coefficients = model.coef_[0]
    top_indices = np.argsort(coefficients)[-top_n:][::-1]
    return pd.DataFrame({
        "Feature": feature_names[top_indices],
        "Importance": coefficients[top_indices]
    })

try:
    vectorizer, model = load_model()
    model_available = True
except Exception:
    vectorizer = None
    model = None
    model_available = False

df = load_dataset()

st.title("🛡️ Real-Time Scam & Spam Detection")
st.markdown(
    """
    An NLP machine learning application that classifies
    SMS messages as **legitimate or spam** using **TF-IDF and Logistic Regression**.
    """
)

tab1, tab2 = st.tabs(["🔍 Real-Time Detector", "📊 EDA Insights"])

# =========================================================
# TAB 1 — REAL-TIME DETECTOR
# =========================================================
with tab1:
    st.header("Analyze a Message")
    user_input = st.text_area(
        "Enter your message:",
        placeholder="Example: Congratulations! You have won a free prize...",
        height=150
    )

    if st.button("Analyze Message", type="primary"):
        if not model_available:
            st.error("Model files not found. Run `python train.py` first.")
        elif not user_input.strip():
            st.warning("Please enter a message.")
        else:
            start_time = time.perf_counter()
            transformed_text = vectorizer.transform([user_input])
            prediction = model.predict(transformed_text)[0]
            probabilities = model.predict_proba(transformed_text)[0]
            latency = (time.perf_counter() - start_time) * 1000

            st.divider()
            if prediction == 1:
                spam_probability = probabilities[1]
                st.error("🚨 Potential Spam Detected")
                st.metric("Predicted Spam Probability", f"{spam_probability * 100:.2f}%")
            else:
                ham_probability = probabilities[0]
                st.success("✅ Message Classified as Legitimate")
                st.metric("Predicted Legitimate Probability", f"{ham_probability * 100:.2f}%")

            st.caption(f"⚡ Inference latency: {latency:.2f} ms")

# =========================================================
# TAB 2 — EDA
# =========================================================
with tab2:
    st.header("📊 Exploratory Data Analysis")
    st.write("Explore the SMS dataset used to train the machine learning model.")

    st.subheader("📌 Dataset Overview")
    total_messages = len(df)
    spam_messages = (df["label"] == "Spam").sum()
    legitimate_messages = (df["label"] == "Legitimate").sum()
    spam_percentage = (spam_messages / total_messages) * 100
    legitimate_percentage = (legitimate_messages / total_messages) * 100

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Messages", f"{total_messages:,}")
    col2.metric("Legitimate", f"{legitimate_messages:,}")
    col3.metric("Spam", f"{spam_messages:,}")
    col4.metric("Spam Rate", f"{spam_percentage:.2f}%")

    st.caption(
        f"The dataset contains {legitimate_percentage:.2f}% legitimate messages and {spam_percentage:.2f}% spam messages."
    )
    st.divider()

    st.subheader("1️⃣ Message Class Distribution")
    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(7, 5))
        counts = df["label"].value_counts()
        ax.bar(counts.index, counts.values)
        ax.set_title("Legitimate vs Spam Messages")
        ax.set_xlabel("Message Type")
        ax.set_ylabel("Number of Messages")

        for i, value in enumerate(counts.values):
            ax.text(i, value + 50, f"{value:,}", ha="center")

        st.pyplot(fig)
        plt.close(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.pie(counts.values, labels=counts.index, autopct="%1.1f%%", startangle=90)
        ax.set_title("Dataset Class Percentage")
        st.pyplot(fig)
        plt.close(fig)

    st.info("The dataset is imbalanced: legitimate messages are much more common than spam messages.")
    st.divider()

    st.subheader("2️⃣ Message Length Analysis")
    feature = st.radio("Select a measurement:", ["Character Count", "Word Count"], horizontal=True)

    selected_feature = "character_count" if feature == "Character Count" else "word_count"
    x_label = "Number of Characters" if feature == "Character Count" else "Number of Words"

    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(data=df, x=selected_feature, hue="label", bins=30, kde=True, ax=ax)
        ax.set_title(f"{feature}: Legitimate vs Spam")
        ax.set_xlabel(x_label)
        ax.set_ylabel("Number of Messages")
        st.pyplot(fig)
        plt.close(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.boxplot(data=df, x="label", y=selected_feature, ax=ax)
        ax.set_title(f"{feature} by Message Type")
        ax.set_xlabel("Message Type")
        ax.set_ylabel(x_label)
        st.pyplot(fig)
        plt.close(fig)

    st.divider()

    st.subheader("3️⃣ Average Message Length")
    length_summary = (
        df.groupby("label")
        .agg(
            Average_Characters=("character_count", "mean"),
            Average_Words=("word_count", "mean")
        )
        .round(2)
    )
    st.dataframe(length_summary, use_container_width=True)
    st.divider()

    st.subheader("4️⃣ Top Spam Indicators")
    if model_available:
        top_n = st.slider("Number of spam indicators:", min_value=5, max_value=20, value=10)
        features = get_top_spam_features(model, vectorizer, top_n)

        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.barplot(data=features, x="Importance", y="Feature", hue="Feature", legend=False, ax=ax)
            ax.set_title("Features Most Associated With Spam")
            st.pyplot(fig)
            plt.close(fig)

        with col2:
            st.write("### Top Indicators")
            display_features = features.copy()
            display_features["Importance"] = display_features["Importance"].round(3)
            st.dataframe(display_features, hide_index=True, use_container_width=True)
    else:
        st.warning("Train the model first to view spam indicators.")

    st.divider()

    st.subheader("5️⃣ Explore the Dataset")
    selected_class = st.selectbox("Choose message type:", ["All", "Legitimate", "Spam"])

    sample_df = df if selected_class == "All" else df[df["label"] == selected_class]
    st.dataframe(
        sample_df[["label", "message", "character_count", "word_count"]].head(20),
        hide_index=True,
        use_container_width=True
    )