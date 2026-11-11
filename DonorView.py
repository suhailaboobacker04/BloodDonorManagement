
import mysql.connector


class BloodDonorManager:

    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sapmmplm@mysql",
            database="blood_db_aug_26"
        )

        print("Database connected successfully!")

    # INSERT

    def post(self, **kwargs):
        try:
            self.cursor = self.connection.cursor()

            query = """
                INSERT INTO donor
                (name, blood_group, phone, city, last_donation)
                VALUES (%s, %s, %s, %s, %s)
            """

            values = (
                kwargs["name"],
                kwargs["blood_group"].upper(),
                kwargs["phone"],
                kwargs["city"],
                kwargs["last_donation"]
            )

            self.cursor.execute(query, values)
            self.connection.commit()
            self.cursor.close()

            return True, "Donor added successfully!"

        except Exception as e:
            self.connection.rollback()
            return False, f"Insert Error: {e}"

    # GET ALL RECORDS

    def get(self):
        try:
            self.cursor = self.connection.cursor()

            query = "SELECT * FROM donor"

            self.cursor.execute(query)
            records = self.cursor.fetchall()

            self.cursor.close()

            return records

        except Exception as e:
            print("Get Error:", e)
            return []

    # GET SINGLE RECORD

    def get_object(self, id):
        try:
            self.cursor = self.connection.cursor()

            query = "SELECT * FROM donor WHERE id=%s"

            self.cursor.execute(query, (id,))
            record = self.cursor.fetchone()

            self.cursor.close()

            return record

        except Exception as e:
            print("Get Object Error:", e)
            return None

    # UPDATE

    def put(self, id=None, **kwargs):
        try:
            record = self.get_object(id=id)

            if record is not None:

                allowed_columns = [
                    "name",
                    "blood_group",
                    "phone",
                    "city",
                    "last_donation"
                ]

                for k in kwargs.keys():
                    if k not in allowed_columns:
                        return False, "Invalid column name!"

                if not kwargs:
                    return False, "No update data provided!"

                if "blood_group" in kwargs:
                    kwargs["blood_group"] = kwargs["blood_group"].upper()

                # CHECK DUPLICATE PHONE

                if "phone" in kwargs:

                    self.cursor = self.connection.cursor()

                    query = """
                        SELECT id FROM donor
                        WHERE phone=%s AND id!=%s
                    """

                    self.cursor.execute(
                        query,
                        (kwargs["phone"], id)
                    )

                    duplicate = self.cursor.fetchone()
                    self.cursor.close()

                    if duplicate:
                        return False, "This phone number already belongs to another donor!"

                # CREATE UPDATE QUERY

                self.cursor = self.connection.cursor()

                placeholder = ""

                for k in kwargs.keys():
                    placeholder += k + "=%s, "

                placeholder = placeholder.rstrip(", ")

                query = f"UPDATE donor SET {placeholder} WHERE id=%s"

                values = list(kwargs.values())
                values.append(id)

                self.cursor.execute(query, values)

                self.connection.commit()
                self.cursor.close()

                return True, "Donor updated successfully!"

            else:
                return False, "Donor not found!"

        except Exception as e:
            self.connection.rollback()
            return False, f"Update Error: {e}"

    # CLOSE CONNECTION

    def close(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Database connection closed!")
