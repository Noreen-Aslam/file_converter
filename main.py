import streamlit as st
import pandas as pd
from io import BytesIO

# Page config - Streamlit icon removed
st.set_page_config(page_title="📁 File Converter", page_icon=None, layout="wide")

# Title
st.title("📁 File Converter")
st.write("Upload your CSV or Excel files to clean the data 🧹")  

# File uploader
files = st.file_uploader(
    "⬆️ Upload CSV or Excel files",
    type=["csv", "xlsx"],
    accept_multiple_files=True
)

if files:
    for file in files:
        ext = file.name.split(".")[-1]

        # Read file
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        # Preview
        st.subheader(f"{file.name} - Preview")
        st.dataframe(df.head())

        # Fill missing values
        if st.checkbox(f" Fill missing values - {file.name}"):
            df.fillna(df.select_dtypes(include="number").mean(), inplace=True)
            st.success("✅ Missing values filled successfully")
            st.dataframe(df.head())

            # Select columns
            selected_columns = st.multiselect(
                f"📋 Select columns - {file.name}",
                df.columns,
                default=df.columns
            )
            df = df[selected_columns]
            st.dataframe(df.head())

            # Show chart
            if st.checkbox(f"📊 Show Chart - {file.name}") and not df.select_dtypes(include="number").empty:
                st.bar_chart(df.select_dtypes(include="number"))

        # File conversion format choice
        format_choice = st.radio(
            f"🔄 Convert {file.name} to:",
            ["csv", "Excel"],
            key=f"radio_{file.name}"
        )

        # Download button
        if st.button(f"💾 Download {file.name} as {format_choice}", key=f"btn_{file.name}"):
            output = BytesIO()
            if format_choice == "csv":
                df.to_csv(output, index=False)
                mime = "text/csv"
                new_name = file.name.rsplit(".", 1)[0] + ".csv"
            else:
                df.to_excel(output, index=False)
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.rsplit(".", 1)[0] + ".xlsx"

            # Reset pointer
            output.seek(0)

            # Download
            st.download_button(
                label="⬇️ Download File",
                file_name=new_name,
                data=output,
                mime=mime
            )
            st.success("🎉 Processing Complete!")
