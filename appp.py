import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title(" NCR Data Scientist Company Job Market")

df = pd.read_excel("ds_company_preferences.xlsx")
df.columns = df.columns.str.strip()

df["PRIMARY SKILL"] = df["PRIMARY SKILL"].str.lower().str.strip()
df["PRIMARY SKILL"] = df["PRIMARY SKILL"].replace({
    "ml": "machine learning",
    "machine learning": "machine learning"
})

df["RATING"] = pd.to_numeric(df["RATING"], errors="coerce")
rating_bins = [0, 3.9, 4.4, 5.0]
rating_labels = ["Below 4.0", "4.0 - 4.4", "4.5 and above"]
df["RATING CATEGORY"] = pd.cut(
    df["RATING"],
    bins=rating_bins,
    labels=rating_labels
)

df["PACKAGE_NUM"] = df["PACKAGE(LPA)"].str.extract(r'(\d+\.?\d*)').astype(float)

st.sidebar.header("Filters")

location = st.sidebar.multiselect(
    "Select LOCATION",
    options=df["LOCATION"].unique(),
    default=df["LOCATION"].unique()
)

work_mode = st.sidebar.multiselect(
    "WORK MODE",
    options=df["WORK MODE"].unique(),
    default=df["WORK MODE"].unique()
)

role = st.sidebar.multiselect(
    "ROLE",
    options=df["ROLE"].unique(),
    default=df["ROLE"].unique()
)

filtered_df = df[
    (df["LOCATION"].isin(location)) &
    (df["WORK MODE"].isin(work_mode)) &
    (df["ROLE"].isin(role))
]

st.subheader("Company Metrics Overview")
k1, k2, k3, k4 = st.columns(4)

k1.metric("Total Companies", filtered_df.shape[0])
k2.metric("Avg Package (LPA)", f"{filtered_df['PACKAGE_NUM'].mean():.1f}" if not filtered_df.empty else "N/A")
k3.metric("Max Package (LPA)", f"{filtered_df['PACKAGE_NUM'].max():.1f}" if not filtered_df.empty else "N/A")
k4.metric("Min Package (LPA)", f"{filtered_df['PACKAGE_NUM'].min():.1f}" if not filtered_df.empty else "N/A")

st.divider()

st.subheader("Visual Insights")
col1, col2 = st.columns([1,1])

with col1:
    st.subheader("Primary Skill Distribution")
    if not filtered_df.empty:
        skill_count = filtered_df["PRIMARY SKILL"].value_counts()
        fig, ax = plt.subplots(figsize=(3.5,3.5))
        ax.pie(skill_count, labels=skill_count.index, autopct="%1.1f%%",  startangle=90)
        ax.axis("equal")
        st.pyplot(fig, use_container_width=False)
    else:
        st.write("No data")

with col2:
    st.markdown("Company Rating Distribution")
    rating_count = filtered_df["RATING CATEGORY"].value_counts().sort_index()

    if not rating_count.empty:
        fig2, ax2 = plt.subplots(figsize=(4.5,3))
        ax2.bar(rating_count.index, rating_count.values)
        ax2.set_xlabel("Rating Range")
        ax2.set_ylabel("Companies")
        st.pyplot(fig2, use_container_width=False)
    else:
        st.write("No rating data")

st.divider()

st.subheader("📊 Package vs Rating & Top Companies")

left, right = st.columns([1, 2])   

with left:
    st.markdown("📈 Package vs Rating")

    if not filtered_df.empty:
        fig, ax = plt.subplots(figsize=(3,3))  

        ax.scatter(
            filtered_df["RATING"],
            filtered_df["PACKAGE_NUM"]
        )

        ax.set_xlabel("Rating")
        ax.set_ylabel("Package (LPA)")
        ax.grid(True, alpha=0.3)

        st.pyplot(fig, use_container_width=True)
    else:
        st.write("No data")

with right:
    st.markdown("🏆 Top 10 Companies by Package")

    top_companies = filtered_df.sort_values(
        by="PACKAGE_NUM", ascending=False
    ).head(10)[["COMPANY NAME", "LOCATION", "PACKAGE(LPA)", "RATING"]]

    st.dataframe(top_companies, use_container_width=True)

st.subheader("🧠 Key Insights")

st.markdown("""
- 🔹 Hybrid work mode dominates NCR companies  
- 🔹 Higher package does not always mean higher rating  
- 🔹 Machine Learning is the most common primary skill  
- 🔹 Gurgaon & Noida show higher paying opportunities  
""")

if filtered_df.empty:
    st.warning("No companies match the selected filters")




