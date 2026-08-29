import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Women's Clothing Reviews Dashboard",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    .stApp {
        background-color: #f8f9fc;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1f1633 0%, #30244d 100%);
    }

    [data-testid="stSidebar"] * {
        color: white;
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #64748b;
        margin-bottom: 30px;
    }

    .insight-card {
        background: white;
        padding: 18px;
        border-radius: 15px;
        border-left: 5px solid #8b5cf6;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 15px;
    }

    .section-title {
        font-size: 26px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 15px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv("women_dresses_reviews.csv")

    # Remove unwanted spaces from column names
    df.columns = df.columns.str.strip()

    # Convert numeric columns
    numeric_columns = [
        "s.no",
        "age",
        "clothing_id",
        "alike_feedback_count",
        "rating",
        "recommend_index"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Clean text columns
    text_columns = [
        "division_name",
        "department_name",
        "class_name",
        "title",
        "review_text"
    ]

    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    # Create review length feature
    df["review_length"] = (
        df["review_text"]
        .astype(str)
        .apply(len)
    )

    # Create word count feature
    df["word_count"] = (
        df["review_text"]
        .astype(str)
        .str.split()
        .apply(len)
    )

    # Recommendation label
    df["recommendation"] = np.where(
        df["recommend_index"] == 1,
        "Recommended",
        "Not Recommended"
    )

    # Rating category
    df["rating_category"] = pd.cut(
        df["rating"],
        bins=[0, 2, 3, 4, 5],
        labels=[
            "Poor (1-2)",
            "Average (3)",
            "Good (4)",
            "Excellent (5)"
        ],
        include_lowest=True
    )

    # Age groups
    df["age_group"] = pd.cut(
        df["age"],
        bins=[
            0,
            20,
            30,
            40,
            50,
            60,
            70,
            100
        ],
        labels=[
            "Under 20",
            "21-30",
            "31-40",
            "41-50",
            "51-60",
            "61-70",
            "70+"
        ],
        include_lowest=True
    )

    return df


try:

    df = load_data()

except Exception as e:

    st.error("Unable to load the dataset.")

    st.code(str(e))

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="main-title">
        👗 Women's Clothing Reviews Analytics Dashboard
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="subtitle">
        Explore customer ratings, recommendations, product categories,
        age groups and review engagement through interactive analytics
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title("👗 Dashboard Controls")


page = st.sidebar.radio(

    "Select Analysis",

    [
        "📊 Overview",
        "⭐ Rating Analysis",
        "👍 Recommendation Analysis",
        "🏷️ Product Analysis",
        "🎂 Customer Age Analysis",
        "💬 Review Analysis",
        "🔥 Popular Products",
        "🔬 Advanced Analytics",
        "🔎 Review Explorer"
    ]

)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.markdown("---")

st.sidebar.subheader("🎛️ Filters")


# ------------------------------------------------------------
# DIVISION FILTER
# ------------------------------------------------------------

divisions = sorted(
    df["division_name"]
    .dropna()
    .unique()
)


selected_divisions = st.sidebar.multiselect(

    "🏢 Select Division",

    options=divisions,

    default=divisions

)


# ------------------------------------------------------------
# DEPARTMENT FILTER
# ------------------------------------------------------------

departments = sorted(
    df["department_name"]
    .dropna()
    .unique()
)


selected_departments = st.sidebar.multiselect(

    "🏷️ Select Department",

    options=departments,

    default=departments

)


# ------------------------------------------------------------
# CLASS FILTER
# ------------------------------------------------------------

classes = sorted(
    df["class_name"]
    .dropna()
    .unique()
)


selected_classes = st.sidebar.multiselect(

    "👗 Select Clothing Class",

    options=classes,

    default=classes

)


# ------------------------------------------------------------
# AGE FILTER
# ------------------------------------------------------------

age_data = df["age"].dropna()


min_age = int(age_data.min())
max_age = int(age_data.max())


age_range = st.sidebar.slider(

    "🎂 Customer Age Range",

    min_value=min_age,

    max_value=max_age,

    value=(
        min_age,
        max_age
    )

)


# ------------------------------------------------------------
# RATING FILTER
# ------------------------------------------------------------

rating_range = st.sidebar.slider(

    "⭐ Rating Range",

    min_value=1,

    max_value=5,

    value=(1, 5)

)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()


filtered_df = filtered_df[
    filtered_df["division_name"]
    .isin(selected_divisions)
]


filtered_df = filtered_df[
    filtered_df["department_name"]
    .isin(selected_departments)
]


filtered_df = filtered_df[
    filtered_df["class_name"]
    .isin(selected_classes)
]


filtered_df = filtered_df[
    filtered_df["age"]
    .between(
        age_range[0],
        age_range[1]
    )
]


filtered_df = filtered_df[
    filtered_df["rating"]
    .between(
        rating_range[0],
        rating_range[1]
    )
]


# ============================================================
# EMPTY DATA CHECK
# ============================================================

if filtered_df.empty:

    st.warning(
        "No reviews found for the selected filters."
    )

    st.stop()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_reviews = len(filtered_df)

average_rating = filtered_df[
    "rating"
].mean()


recommendation_rate = (
    filtered_df["recommend_index"]
    .mean()
    * 100
)


average_age = filtered_df[
    "age"
].mean()


average_feedback = filtered_df[
    "alike_feedback_count"
].mean()


# ============================================================
# OVERVIEW PAGE
# ============================================================

if page == "📊 Overview":

    st.subheader(
        "📊 Customer Reviews Overview"
    )


    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "💬 Total Reviews",
        f"{total_reviews:,}"
    )


    col2.metric(
        "⭐ Average Rating",
        f"{average_rating:.2f} / 5"
    )


    col3.metric(
        "👍 Recommendation Rate",
        f"{recommendation_rate:.1f}%"
    )


    col4.metric(
        "🎂 Average Customer Age",
        f"{average_age:.1f}"
    )


    st.markdown("---")


    # --------------------------------------------------------
    # RATING DISTRIBUTION
    # --------------------------------------------------------

    rating_counts = (

        filtered_df["rating"]

        .value_counts()

        .sort_index()

        .reset_index()

    )


    rating_counts.columns = [
        "Rating",
        "Reviews"
    ]


    fig_ratings = px.bar(

        rating_counts,

        x="Rating",

        y="Reviews",

        title="⭐ Customer Rating Distribution",

        text="Reviews"

    )


    # --------------------------------------------------------
    # RECOMMENDATION DISTRIBUTION
    # --------------------------------------------------------

    recommendation_counts = (

        filtered_df["recommendation"]

        .value_counts()

        .reset_index()

    )


    recommendation_counts.columns = [
        "Recommendation",
        "Reviews"
    ]


    fig_recommendation = px.pie(

        recommendation_counts,

        names="Recommendation",

        values="Reviews",

        hole=0.55,

        title="👍 Customer Recommendation Distribution"

    )


    c1, c2 = st.columns(2)


    c1.plotly_chart(
        fig_ratings,
        use_container_width=True
    )


    c2.plotly_chart(
        fig_recommendation,
        use_container_width=True
    )


    # --------------------------------------------------------
    # TOP PRODUCT CLASSES
    # --------------------------------------------------------

    class_counts = (

        filtered_df["class_name"]

        .value_counts()

        .head(15)

        .reset_index()

    )


    class_counts.columns = [
        "Clothing Class",
        "Reviews"
    ]


    fig_classes = px.bar(

        class_counts,

        x="Reviews",

        y="Clothing Class",

        orientation="h",

        title="👗 Top Clothing Categories by Review Volume"

    )


    fig_classes.update_layout(
        yaxis={
            "categoryorder":
            "total ascending"
        }
    )


    st.plotly_chart(
        fig_classes,
        use_container_width=True
    )


    # --------------------------------------------------------
    # KEY INSIGHTS
    # --------------------------------------------------------

    st.subheader(
        "💡 Key Customer Insights"
    )


    top_class = (
        filtered_df["class_name"]
        .value_counts()
        .idxmax()
    )


    top_class_reviews = (
        filtered_df["class_name"]
        .value_counts()
        .max()
    )


    most_common_rating = (
        filtered_df["rating"]
        .mode()
        .iloc[0]
    )


    highest_feedback_row = filtered_df.loc[
        filtered_df[
            "alike_feedback_count"
        ].idxmax()
    ]


    c1, c2, c3 = st.columns(3)


    with c1:

        st.markdown(

            f"""
            <div class="insight-card">

            <h4>⭐ Most Common Rating</h4>

            <p>

            The most frequently given rating is

            <b>{most_common_rating:.0f} / 5</b>.

            </p>

            </div>
            """,

            unsafe_allow_html=True

        )


    with c2:

        st.markdown(

            f"""
            <div class="insight-card">

            <h4>👗 Most Reviewed Category</h4>

            <p>

            <b>{top_class}</b>

            has the highest number of reviews with

            <b>{top_class_reviews:,}</b> customer reviews.

            </p>

            </div>
            """,

            unsafe_allow_html=True

        )


    with c3:

        st.markdown(

            f"""
            <div class="insight-card">

            <h4>🔥 Most Helpful Review</h4>

            <p>

            The highest review engagement is

            <b>{highest_feedback_row["alike_feedback_count"]:,.0f}</b>

            likes/feedback interactions.

            </p>

            </div>
            """,

            unsafe_allow_html=True

        )


# ============================================================
# RATING ANALYSIS
# ============================================================

elif page == "⭐ Rating Analysis":

    st.subheader(
        "⭐ Customer Rating Analysis"
    )


    # Rating distribution by department

    fig_department_rating = px.box(

        filtered_df,

        x="department_name",

        y="rating",

        title="⭐ Rating Distribution by Department"

    )


    st.plotly_chart(
        fig_department_rating,
        use_container_width=True
    )


    # Average rating by clothing class

    class_rating = (

        filtered_df

        .groupby("class_name")

        .agg(

            Average_Rating=(
                "rating",
                "mean"
            ),

            Reviews=(
                "rating",
                "count"
            )

        )

        .reset_index()

        .sort_values(
            "Average_Rating",
            ascending=False
        )

    )


    fig_class_rating = px.bar(

        class_rating,

        x="class_name",

        y="Average_Rating",

        size="Reviews",

        hover_data=["Reviews"],

        title="🏆 Average Rating by Clothing Class"

    )


    st.plotly_chart(
        fig_class_rating,
        use_container_width=True
    )


    # Rating by division

    division_rating = (

        filtered_df

        .groupby("division_name")

        .agg(

            Average_Rating=(
                "rating",
                "mean"
            ),

            Reviews=(
                "rating",
                "count"
            )

        )

        .reset_index()

    )


    fig_division_rating = px.bar(

        division_rating,

        x="division_name",

        y="Average_Rating",

        text="Reviews",

        title="⭐ Average Rating by Division"

    )


    st.plotly_chart(
        fig_division_rating,
        use_container_width=True
    )


    st.dataframe(

        class_rating.round(2),

        use_container_width=True,

        hide_index=True

    )


# ============================================================
# RECOMMENDATION ANALYSIS
# ============================================================

elif page == "👍 Recommendation Analysis":

    st.subheader(
        "👍 Customer Recommendation Analysis"
    )


    recommendation_by_rating = (

        filtered_df

        .groupby("rating")

        .agg(

            Recommendation_Rate=(
                "recommend_index",
                "mean"
            ),

            Reviews=(
                "recommend_index",
                "count"
            )

        )

        .reset_index()

    )


    recommendation_by_rating[
        "Recommendation_Rate"
    ] = (
        recommendation_by_rating[
            "Recommendation_Rate"
        ]
        * 100
    )


    fig_recommend_rating = px.bar(

        recommendation_by_rating,

        x="rating",

        y="Recommendation_Rate",

        text="Recommendation_Rate",

        title="👍 Recommendation Rate by Rating"

    )


    st.plotly_chart(
        fig_recommend_rating,
        use_container_width=True
    )


    # Recommendation by department

    department_recommendation = (

        filtered_df

        .groupby("department_name")

        .agg(

            Recommendation_Rate=(
                "recommend_index",
                "mean"
            ),

            Reviews=(
                "recommend_index",
                "count"
            )

        )

        .reset_index()

    )


    department_recommendation[
        "Recommendation_Rate"
    ] = (
        department_recommendation[
            "Recommendation_Rate"
        ]
        * 100
    )


    fig_department_recommendation = px.bar(

        department_recommendation,

        x="department_name",

        y="Recommendation_Rate",

        hover_data=["Reviews"],

        title="👍 Recommendation Rate by Department"

    )


    st.plotly_chart(
        fig_department_recommendation,
        use_container_width=True
    )


    # Recommendation by class

    class_recommendation = (

        filtered_df

        .groupby("class_name")

        .agg(

            Recommendation_Rate=(
                "recommend_index",
                "mean"
            ),

            Reviews=(
                "recommend_index",
                "count"
            )

        )

        .reset_index()

    )


    class_recommendation[
        "Recommendation_Rate"
    ] = (
        class_recommendation[
            "Recommendation_Rate"
        ]
        * 100
    )


    fig_class_recommendation = px.scatter(

        class_recommendation,

        x="Reviews",

        y="Recommendation_Rate",

        size="Reviews",

        hover_name="class_name",

        title="📊 Review Volume vs Recommendation Rate"

    )


    st.plotly_chart(
        fig_class_recommendation,
        use_container_width=True
    )


# ============================================================
# PRODUCT ANALYSIS
# ============================================================

elif page == "🏷️ Product Analysis":

    st.subheader(
        "🏷️ Product Category Analysis"
    )


    category_stats = (

        filtered_df

        .groupby("class_name")

        .agg(

            Reviews=(
                "rating",
                "count"
            ),

            Average_Rating=(
                "rating",
                "mean"
            ),

            Recommendation_Rate=(
                "recommend_index",
                "mean"
            ),

            Average_Feedback=(
                "alike_feedback_count",
                "mean"
            )

        )

        .reset_index()

    )


    category_stats[
        "Recommendation_Rate"
    ] = (
        category_stats[
            "Recommendation_Rate"
        ]
        * 100
    )


    fig_product_volume = px.bar(

        category_stats,

        x="class_name",

        y="Reviews",

        title="👗 Review Volume by Clothing Category"

    )


    st.plotly_chart(
        fig_product_volume,
        use_container_width=True
    )


    fig_product_rating = px.scatter(

        category_stats,

        x="Average_Rating",

        y="Recommendation_Rate",

        size="Reviews",

        hover_name="class_name",

        title="⭐ Product Rating vs Recommendation Rate"

    )


    st.plotly_chart(
        fig_product_rating,
        use_container_width=True
    )


    st.dataframe(

        category_stats.round(2),

        use_container_width=True,

        hide_index=True

    )


# ============================================================
# CUSTOMER AGE ANALYSIS
# ============================================================

elif page == "🎂 Customer Age Analysis":

    st.subheader(
        "🎂 Customer Demographic Analysis"
    )


    c1, c2 = st.columns(2)


    # Age distribution

    fig_age = px.histogram(

        filtered_df,

        x="age",

        nbins=30,

        title="🎂 Customer Age Distribution"

    )


    # Age group distribution

    age_counts = (

        filtered_df["age_group"]

        .value_counts()

        .sort_index()

        .reset_index()

    )


    age_counts.columns = [
        "Age Group",
        "Reviews"
    ]


    fig_age_group = px.bar(

        age_counts,

        x="Age Group",

        y="Reviews",

        title="👥 Customer Reviews by Age Group"

    )


    c1.plotly_chart(
        fig_age,
        use_container_width=True
    )


    c2.plotly_chart(
        fig_age_group,
        use_container_width=True
    )


    # Rating by age group

    age_rating = (

        filtered_df

        .groupby("age_group", observed=True)

        .agg(

            Average_Rating=(
                "rating",
                "mean"
            ),

            Recommendation_Rate=(
                "recommend_index",
                "mean"
            ),

            Reviews=(
                "rating",
                "count"
            )

        )

        .reset_index()

    )


    age_rating[
        "Recommendation_Rate"
    ] = (
        age_rating[
            "Recommendation_Rate"
        ]
        * 100
    )


    fig_age_rating = px.line(

        age_rating,

        x="age_group",

        y="Average_Rating",

        markers=True,

        title="⭐ Average Rating by Customer Age Group"

    )


    st.plotly_chart(
        fig_age_rating,
        use_container_width=True
    )


    fig_age_recommend = px.bar(

        age_rating,

        x="age_group",

        y="Recommendation_Rate",

        title="👍 Recommendation Rate by Age Group"

    )


    st.plotly_chart(
        fig_age_recommend,
        use_container_width=True
    )


# ============================================================
# REVIEW ANALYSIS
# ============================================================

elif page == "💬 Review Analysis":

    st.subheader(
        "💬 Customer Review Text Analysis"
    )


    c1, c2 = st.columns(2)


    fig_review_length = px.histogram(

        filtered_df,

        x="review_length",

        nbins=50,

        title="📝 Review Length Distribution"

    )


    fig_word_count = px.histogram(

        filtered_df,

        x="word_count",

        nbins=50,

        title="🔤 Review Word Count Distribution"

    )


    c1.plotly_chart(
        fig_review_length,
        use_container_width=True
    )


    c2.plotly_chart(
        fig_word_count,
        use_container_width=True
    )


    # Review length vs rating

    fig_length_rating = px.box(

        filtered_df,

        x="rating",

        y="word_count",

        title="💬 Review Length by Rating"

    )


    st.plotly_chart(
        fig_length_rating,
        use_container_width=True
    )


    # Feedback vs rating

    fig_feedback_rating = px.scatter(

        filtered_df,

        x="rating",

        y="alike_feedback_count",

        size="word_count",

        hover_data=[
            "class_name",
            "department_name"
        ],

        title="🔥 Review Engagement vs Rating"

    )


    st.plotly_chart(
        fig_feedback_rating,
        use_container_width=True
    )


    # Most helpful reviews

    st.subheader(
        "🔥 Most Helpful Customer Reviews"
    )


    helpful_reviews = (

        filtered_df

        .sort_values(
            "alike_feedback_count",
            ascending=False
        )

        .head(20)

    )


    display_columns = [

        "title",
        "class_name",
        "rating",
        "recommendation",
        "alike_feedback_count",
        "review_text"

    ]


    st.dataframe(

        helpful_reviews[
            display_columns
        ],

        use_container_width=True,

        height=600

    )


# ============================================================
# POPULAR PRODUCTS
# ============================================================

elif page == "🔥 Popular Products":

    st.subheader(
        "🔥 Popular Product Analysis"
    )


    product_stats = (

        filtered_df

        .groupby("clothing_id")

        .agg(

            Reviews=(
                "rating",
                "count"
            ),

            Average_Rating=(
                "rating",
                "mean"
            ),

            Recommendation_Rate=(
                "recommend_index",
                "mean"
            ),

            Total_Feedback=(
                "alike_feedback_count",
                "sum"
            ),

            Average_Age=(
                "age",
                "mean"
            )

        )

        .reset_index()

    )


    product_stats[
        "Recommendation_Rate"
    ] = (
        product_stats[
            "Recommendation_Rate"
        ]
        * 100
    )


    ranking_option = st.selectbox(

        "Rank Products By",

        [
            "Reviews",
            "Average Rating",
            "Recommendation Rate",
            "Total Feedback"
        ]

    )


    ranking_map = {

        "Reviews": "Reviews",

        "Average Rating": "Average_Rating",

        "Recommendation Rate":
        "Recommendation_Rate",

        "Total Feedback":
        "Total_Feedback"

    }


    ranking_column = ranking_map[
        ranking_option
    ]


    top_products = (

        product_stats

        .sort_values(

            ranking_column,

            ascending=False

        )

        .head(25)

    )


    fig_top_products = px.bar(

        top_products,

        x=ranking_column,

        y="clothing_id",

        orientation="h",

        hover_data=[

            "Reviews",
            "Average_Rating",
            "Recommendation_Rate",
            "Total_Feedback"

        ],

        title=f"🏆 Top Products by {ranking_option}"

    )


    fig_top_products.update_layout(
        yaxis={
            "categoryorder":
            "total ascending"
        }
    )


    st.plotly_chart(
        fig_top_products,
        use_container_width=True
    )


    st.dataframe(

        top_products.round(2),

        use_container_width=True,

        hide_index=True

    )


# ============================================================
# ADVANCED ANALYTICS
# ============================================================

elif page == "🔬 Advanced Analytics":

    st.subheader(
        "🔬 Advanced Customer Analytics"
    )


    numeric_columns = [

        "age",
        "clothing_id",
        "alike_feedback_count",
        "rating",
        "recommend_index",
        "review_length",
        "word_count"

    ]


    correlation_data = (

        filtered_df[
            numeric_columns
        ]

        .dropna()

    )


    corr = correlation_data.corr()


    fig_corr = px.imshow(

        corr,

        text_auto=".2f",

        aspect="auto",

        title="📊 Customer Review Feature Correlation Heatmap"

    )


    fig_corr.update_layout(
        height=650
    )


    st.plotly_chart(
        fig_corr,
        use_container_width=True
    )


    # Rating correlation

    rating_corr = (

        corr["rating"]

        .drop("rating")

        .sort_values()

        .reset_index()

    )


    rating_corr.columns = [

        "Feature",
        "Correlation"

    ]


    fig_rating_corr = px.bar(

        rating_corr,

        x="Correlation",

        y="Feature",

        orientation="h",

        title="⭐ Features Associated with Customer Ratings"

    )


    st.plotly_chart(
        fig_rating_corr,
        use_container_width=True
    )


    # Statistical summary

    st.subheader(
        "📋 Statistical Summary"
    )


    summary = (

        filtered_df[
            numeric_columns
        ]

        .describe()

        .T

    )


    st.dataframe(

        summary.round(3),

        use_container_width=True

    )


    # Missing values analysis

    st.subheader(
        "🧹 Data Quality Analysis"
    )


    missing_data = (

        filtered_df

        .isnull()

        .sum()

        .reset_index()

    )


    missing_data.columns = [

        "Column",
        "Missing Values"

    ]


    missing_data = (

        missing_data

        .sort_values(

            "Missing Values",

            ascending=False

        )

    )


    fig_missing = px.bar(

        missing_data,

        x="Missing Values",

        y="Column",

        orientation="h",

        title="⚠️ Missing Values Analysis"

    )


    fig_missing.update_layout(
        yaxis={
            "categoryorder":
            "total ascending"
        }
    )


    st.plotly_chart(
        fig_missing,
        use_container_width=True
    )


# ============================================================
# REVIEW EXPLORER
# ============================================================

elif page == "🔎 Review Explorer":

    st.subheader(
        "🔎 Explore Customer Reviews"
    )


    search = st.text_input(
        "🔍 Search Review Text or Title"
    )


    display_df = filtered_df.copy()


    if search:

        search_mask = (

            display_df[
                "title"
            ]

            .astype(str)

            .str.contains(

                search,

                case=False,

                na=False

            )

            |

            display_df[
                "review_text"
            ]

            .astype(str)

            .str.contains(

                search,

                case=False,

                na=False

            )

        )


        display_df = display_df[
            search_mask
        ]


    default_columns = [

        "age",
        "division_name",
        "department_name",
        "class_name",
        "clothing_id",
        "rating",
        "recommendation",
        "alike_feedback_count",
        "title",
        "review_text"

    ]


    selected_columns = st.multiselect(

        "Select Columns to Display",

        options=display_df.columns.tolist(),

        default=default_columns

    )


    if selected_columns:

        st.dataframe(

            display_df[
                selected_columns
            ],

            use_container_width=True,

            height=600

        )


    csv = display_df.to_csv(
        index=False
    ).encode(
        "utf-8"
    )


    st.download_button(

        label="📥 Download Filtered Reviews",

        data=csv,

        file_name="filtered_clothing_reviews.csv",

        mime="text/csv"

    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")


st.markdown(

    """
    <div style="text-align:center;color:#64748b;padding:20px;">

    👗 Women's Clothing Reviews Analytics Dashboard

    <br>

    Built with Python • Streamlit • Pandas • NumPy • Plotly

    </div>
    """,

    unsafe_allow_html=True

)
