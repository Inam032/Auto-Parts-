import streamlit as st
import pandas as pd

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Honda Spare Parts", page_icon="bycicle.png", layout="wide")

# ---- TITLE ----
st.title("Honda Spare Parts")
st.markdown("manage your spare parts inventory, and sales records.")

# ---- INITIAL DATA ----
if "parts_data" not in st.session_state:
    st.session_state.parts_data = pd.DataFrame(
        columns=["Part Number", "Part Name", "Category", "Quantity", "Price (PKR)", "Supplier"]
    )

# ---- SIDEBAR ----
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to:", ["Add New Part", "View Inventory", "Search Parts Number", "Update/Delete Parts", "About"])

# ---- ADD NEW PART ----
# ---- ADD NEW PART ----
# ---- ADD NEW PART ----
if page == "Add New Part":
    st.header("➕ Add New Spare Part")

    with st.form("add_form"):
        st.subheader("Add or Search Spare Part")

        # 🔍 Search existing part first
        search_part = st.text_input("🔍 Search by Part ID, Number, or Name")

        if search_part:
            filtered = st.session_state.parts_data[
                st.session_state.parts_data.applymap(str)
                .apply(lambda row: row.str.lower().str.contains(search_part.lower()).any(), axis=1)
            ]
            if not filtered.empty:
                st.info("Matching parts found:")
                st.dataframe(filtered, use_container_width=True)
            else:
                st.warning("No matching parts found.")

        st.divider()  # nice visual separator

        # 🧩 Add New Part
        part_id = st.text_input("Part ID")
        part_number = st.text_input("Part Number")
        part_name = st.text_input("Part Name")
        category = st.selectbox("Category", ["Engine", "Brakes", "Suspension", "Electrical", "Body", "Other"])
        quantity = st.number_input("Quantity", min_value=0, step=1)
        price = st.number_input("Price (USD)", min_value=0.0, step=0.1)
        supplier = st.text_input("Supplier Name")

        submitted = st.form_submit_button("Add Part")

    if submitted:
        if part_id and part_name:
            new_part = {
                "Part ID": part_id,
                "Part Number": part_number,
                "Part Name": part_name,
                "Category": category,
                "Quantity": quantity,
                "Price (USD)": price,
                "Supplier": supplier
            }

            st.session_state.parts_data = pd.concat(
                [st.session_state.parts_data, pd.DataFrame([new_part])],
                ignore_index=True
            )

            st.success(f"✅ '{part_name}' added successfully!")
        else:
            st.warning("⚠️ Please enter both Part ID and Part Name.")

# ---- VIEW INVENTORY ----
elif page == "View Inventory":
    st.header("📦 Spare Parts Inventory")
    st.dataframe(st.session_state.parts_data, use_container_width=True)

    total_value = (st.session_state.parts_data["Quantity"].astype(float) *
                   st.session_state.parts_data["Price (PKR)"].astype(float)).sum()
    st.metric("💰 Total Inventory Value (PKR)", f"${total_value:,.2f}")

# ---- SEARCH PARTS ----
elif page == "Search Parts":
    st.header("🔍 Search Spare Parts")
    query = st.text_input("Enter Part Name or ID to search:")
    if query:
        filtered = st.session_state.parts_data[
            st.session_state.parts_data.apply(lambda row: query.lower() in row.astype(str).str.lower().to_string(), axis=1)
        ]
        if not filtered.empty:
            st.dataframe(filtered, use_container_width=True)
        else:
            st.warning("No matching parts found.")

# ---- UPDATE / DELETE ----
elif page == "Update/Delete Parts":
    st.header("✏️ Update or Delete Spare Parts")

    if len(st.session_state.parts_data) == 0:
        st.info("No parts in inventory.")
    else:
        selected_id = st.selectbox("Select Part ID", st.session_state.parts_data["Part ID"])
        part = st.session_state.parts_data[st.session_state.parts_data["Part ID"] == selected_id].iloc[0]

        with st.form("update_form"):
            new_name = st.text_input("Part Name", value=part["Part Name"])
            new_category = st.selectbox("Category", ["Engine", "Brakes", "Suspension", "Electrical", "Body", "Other"], index=0)
            new_quantity = st.number_input("Quantity", min_value=0, step=1, value=int(part["Quantity"]))
            new_price = st.number_input("Price (USD)", min_value=0.0, step=0.1, value=float(part["Price (USD)"]))
            new_supplier = st.text_input("Supplier", value=part["Supplier"])

            col1, col2 = st.columns(2)
            update_btn = col1.form_submit_button("Update Part")
            delete_btn = col2.form_submit_button("Delete Part")

        if update_btn:
            idx = st.session_state.parts_data[st.session_state.parts_data["Part ID"] == selected_id].index[0]
            st.session_state.parts_data.loc[idx] = [selected_id, new_name, new_category, new_quantity, new_price, new_supplier]
            st.success("✅ Part updated successfully!")

        if delete_btn:
            st.session_state.parts_data = st.session_state.parts_data[st.session_state.parts_data["Part ID"] != selected_id]
            st.success("🗑️ Part deleted successfully!")

# ---- ABOUT ----
elif page == "About":
    st.header("ℹ️ About This App")
    st.markdown("""
    **Automobile Spare Parts App** is built with [Streamlit](https://streamlit.io/) using Python.  
    It helps workshops and dealers to manage:
    - 🧩 Spare parts inventory  
    - 🏷️ Pricing and supplier data  
    - 📈 Total stock value  
    - 🔍 Search and update features  

    **Developer:** OpenAI GPT-5 Demo  
    """)

