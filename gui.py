
import streamlit as st
import pandas as pd

from DonorView import BloodDonorManager


donor = BloodDonorManager()

blood_groups = [
    "A+", "A-", "B+", "B-",
    "O+", "O-", "AB+", "AB-"
]

tab1, tab2, tab3 = st.tabs([
    "Add Donor",
    "View Donors",
    "Update Donor"
])


# ADD DONOR

with tab1:

    st.header("Add New Donor")

    name = st.text_input("Enter Name", key="add_name")
    phone = st.text_input("Enter Phone", key="add_phone")

    group = st.selectbox(
        "Blood Group",
        blood_groups,
        key="add_group"
    )

    city = st.text_input("Enter City", key="add_city")

    date = st.date_input(
        "Last Donation Date",
        key="add_date"
    )

    if st.button("Submit", key="add_submit"):

        if name and phone and city:

            status, msg = donor.post(
                name=name,
                phone=phone,
                blood_group=group,
                city=city,
                last_donation=date
            )

            if status:
                st.success(msg)
                st.rerun()

            else:
                st.error(msg)

        else:
            st.warning("Please fill all fields!")


# VIEW DONORS

with tab2:

    st.header("View Donor Details")

    records = donor.get()

    if records:

        df = pd.DataFrame(
            records,
            columns=[
                "Donor ID",
                "Name",
                "Blood Group",
                "Phone",
                "City",
                "Last Donation"
            ]
        )

        df["Blood Group"] = df["Blood Group"].str.upper()

        st.dataframe(
            df,
            hide_index=True,
            use_container_width=True
        )

    else:
        st.warning("No donor records found!")


# UPDATE DONOR

with tab3:

    st.header("Update Donor Details")

    records = donor.get()

    if records:

        donor_ids = [r[0] for r in records]

        donor_id = st.selectbox(
            "Select Donor ID",
            donor_ids,
            key="select_donor_id"
        )

        record = donor.get_object(id=donor_id)

        if record:

            name = st.text_input(
                "Enter Name",
                value=record[1],
                key=f"update_name_{donor_id}"
            )

            group = st.selectbox(
                "Blood Group",
                blood_groups,
                index=blood_groups.index(
                    str(record[2]).strip().upper()
                ),
                key=f"update_group_{donor_id}"
            )

            phone = st.text_input(
                "Enter Phone",
                value=record[3],
                key=f"update_phone_{donor_id}"
            )

            city = st.text_input(
                "Enter City",
                value=record[4],
                key=f"update_city_{donor_id}"
            )

            date = st.date_input(
                "Last Donation Date",
                value=record[5],
                key=f"update_date_{donor_id}"
            )

            if st.button(
                "Update Donor",
                key=f"update_submit_{donor_id}"
            ):

                if name and phone and city:

                    status, msg = donor.put(
                        id=donor_id,
                        name=name,
                        blood_group=group,
                        phone=phone,
                        city=city,
                        last_donation=date
                    )

                    if status:
                        st.success(msg)
                        st.rerun()

                    else:
                        st.error(msg)

                else:
                    st.warning("Please fill all fields!")

        else:
            st.error("Donor not found!")

    else:
        st.warning("No donor records found!")
