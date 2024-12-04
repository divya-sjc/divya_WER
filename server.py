import streamlit as st
from datetime import datetime, date
import pandas as pd
import json
import psycopg2
from psycopg2 import IntegrityError, OperationalError
import re
import os
import hashlib
import yaml
import argparse


def read_config(file_path):
    with open(file_path, "r") as f:
        yaml_config = yaml.safe_load(f)

    with open(yaml_config["sql"]["store"]["creds"], "r") as json_file:
        config = json.load(json_file)

    return config


def establish_connection():
    args = _parse_args()
    # print(f'ENV Value: {args.env}')
    file_path = f"./configs/{args.env}/data-updation-static.yaml"
    # print(file_path)
    config = read_config(file_path)
    try:
        conn = psycopg2.connect(
            host=config["host"],
            port=config["port"],
            user=config["user"],
            password=config["password"],
            database=config["database"],
        )
        return conn
    except OperationalError as e:
        st.write(f"Error: {e}")
        return None


def create_user(conn, username, password):
    with conn.cursor() as c:
        c.execute(
            'INSERT INTO public."users" (username, password) VALUES (%s, %s)',
            (username, password),
        )
        conn.commit()


def check_key_exists(conn, table_name, key):
    with conn.cursor() as c:
        c.execute(
            'SELECT COUNT(*) FROM public."' + table_name + '" WHERE "keywords" = %s',
            (key,),
        )
        result = c.fetchone()
        return result[0] > 0


def check_key_exists_column(conn, table_name, col_name, key):
    with conn.cursor() as c:
        c.execute(
            'SELECT COUNT(*) FROM "' + table_name + '" WHERE "' + col_name + '" = %s',
            (key,),
        )
        result = c.fetchone()
        return result[0] > 0


def check_synonym_doesnt_exist(conn, table_name, synonym):
    with conn.cursor() as c:
        c.execute(
            'SELECT COUNT(*) FROM public."' + table_name + '" WHERE "keywords" = %s',
            (synonym,),
        )
        result = c.fetchone()
        return result[0] < 1


def check_no_duplicate(conn, table_name, col_name, value):
    with conn.cursor() as c:
        c.execute(
            'SELECT COUNT(*) FROM public."'
            + table_name
            + '" WHERE "'
            + col_name
            + '" = %s',
            (value,),
        )
        result = c.fetchone()
        return result[0] < 1


def normalize_str(string):
    string = re.sub(
        r'[!"#$*+,\/:;<=>?@[\]^_`{|}~()]+', " ", string
    )  # noqa  Remove special characters
    string = re.sub(r"\s\s", " ", string)
    return string.strip().lower()


def insert_synonyms(conn, table_name, key, synonym, type1, username, timestamp):
    with conn.cursor() as c:
        c.execute(
            'INSERT INTO public."'
            + table_name
            + '" (keywords, synonym, type, username, timestamp) VALUES (%s, %s, %s, %s, %s)',
            (key, synonym, type1, username, timestamp),
        )
        conn.commit()


def insert_synonym_table(
    conn, key, synonym, type1, username, timestamp, table_name1, table_name2
):
    if not check_key_exists(conn, table_name2, key):
        st.warning("Invalid key value " + table_name2 + "! Please enter a valid key.")
        return
    if not check_synonym_doesnt_exist(conn, table_name2, synonym):
        st.warning(
            "Synonym value is a key " + table_name2 + "! Please enter a valid synonym."
        )
        return
    col_name = "synonym"
    value = synonym
    if not check_no_duplicate(conn, table_name1, col_name, value):
        st.warning(
            "Synonym already exists in "
            + table_name1
            + "!Please enter a valid synonym."
        )
        return
    try:
        insert_synonyms(conn, table_name1, key, synonym, type1, username, timestamp)
        st.success("Synonym added successfully to " + table_name1 + "!")
    except IntegrityError as e:
        st.write(f"Error: {e}")


def insert_synonym_table(conn, key, synonym, type1, username, timestamp, table_name1):
    col_name = "synonym"
    value = synonym
    if not check_no_duplicate(conn, table_name1, col_name, value):
        st.warning(
            "Synonym already exists in "
            + table_name1
            + "!Please enter a valid synonym."
        )
        return
    try:
        insert_synonyms(conn, table_name1, key, synonym, type1, username, timestamp)
        st.success("Synonym added successfully to " + table_name1 + "!")
    except IntegrityError as e:
        st.write(f"Error: {e}")


def insert_global_synonym_table(
    conn, key, synonym, type1, username, timestamp, table_name1, table_name2
):
    if table_name1 == "bus_global_syn":
        if not (
            check_key_exists_column(conn, table_name2, "terminal_name", key)
            or check_key_exists_column(conn, table_name2, "city_name", key)
            or check_key_exists_column(conn, table_name2, "province_name", key)
            or check_key_exists_column(conn, table_name2, "country_name", key)
        ):
            st.warning(
                "Invalid key value " + table_name2 + "! Please enter a valid key."
            )
            return
        if (
            check_key_exists_column(conn, table_name2, "terminal_name", synonym)
            or check_key_exists_column(conn, table_name2, "city_name", synonym)
            or check_key_exists_column(conn, table_name2, "province_name", synonym)
            or check_key_exists_column(conn, table_name2, "country_name", synonym)
        ):
            st.warning(
                "Synonym value is a key "
                + table_name2
                + "! Please enter a valid synonym."
            )
            return
        col_name = "synonym"
        if not check_no_duplicate(conn, table_name1, col_name, synonym):
            st.warning(
                "Synonym already exists "
                + table_name1
                + "! Please enter a valid synonym."
            )
            return
        try:
            insert_synonyms(conn, table_name1, key, synonym, type1, username, timestamp)
            st.success("Synonym added to " + table_name1 + " set successfully!")
        except IntegrityError as e:
            st.write(f"Error: {e}")
    else:
        if not (
            check_key_exists_column(conn, table_name2, "SKUName", key)
            or check_key_exists_column(conn, table_name2, "ProductType", key)
            or check_key_exists_column(conn, table_name2, "Brand", key)
        ):
            st.warning(
                "Invalid key value " + table_name2 + "! Please enter a valid key."
            )
            return
        if (
            check_key_exists_column(conn, table_name2, "SKUName", synonym)
            or check_key_exists_column(conn, table_name2, "ProductType", synonym)
            or check_key_exists_column(conn, table_name2, "Brand", synonym)
        ):
            st.warning(
                "Synonym value is a key "
                + table_name2
                + "! Please enter a valid synonym."
            )
            return
        col_name = "synonym"
        if not check_no_duplicate(conn, table_name1, col_name, synonym):
            st.warning(
                "Synonym already exists "
                + table_name1
                + "! Please enter a valid synonym."
            )
            return
        try:
            insert_synonyms(conn, table_name1, key, synonym, type1, username, timestamp)
            st.success("Synonym added to " + table_name1 + " set successfully!")
        except IntegrityError as e:
            st.write(f"Error: {e}")


def insert_global_lang_table(
    conn, key, synonym, lang1, type1, username, timestamp, table_name, table_name1
):
    if table_name == "bus_global_lang":
        if not (
            check_key_exists_column(conn, table_name1, "terminal_name", key)
            or check_key_exists_column(conn, table_name1, "city_name", key)
            or check_key_exists_column(conn, table_name1, "province_name", key)
            or check_key_exists_column(conn, table_name1, "country_name", key)
        ):
            st.warning(
                "Invalid key value " + table_name1 + "! Please enter a valid key."
            )
            return
        col_name = "translation"
        if synonym != "":
            if not check_no_duplicate(conn, table_name, col_name, synonym):
                st.warning(
                    "Language already exists "
                    + table_name
                    + "! Please enter a valid Language hint."
                )
                return
        try:
            insert_lang(
                conn, table_name, key, synonym, lang1, type1, username, timestamp
            )
            st.success("Language hints added successfully into " + table_name)
        except IntegrityError as e:
            st.write(f"Error: {e}")
    else:
        if not (
            check_key_exists_column(conn, table_name1, "SKUName", key)
            or check_key_exists_column(conn, table_name1, "ProductType", key)
            or check_key_exists_column(conn, table_name1, "Brand", key)
        ):
            st.warning(
                "Invalid key value " + table_name1 + "! Please enter a valid key."
            )
            return
        col_name = "translation"
        if synonym != "":
            if not check_no_duplicate(conn, table_name, col_name, synonym):
                st.warning(
                    "Language already exists "
                    + table_name
                    + "! Please enter a valid Language hint."
                )
                return
        try:
            insert_lang(
                conn, table_name, key, synonym, lang1, type1, username, timestamp
            )
            st.success("Language hints added successfully into " + table_name)
        except IntegrityError as e:
            st.write(f"Error: {e}")


def download_sku(conn, df):
    container_height = min(len(df) * 50, 300)
    mf = df
    mf.fillna("", inplace=True)
    with st.container():
        st.dataframe(mf, height=container_height)
    st.download_button(
        label="Download data as CSV",
        data=df.to_csv(index=False, header=True).rstrip(os.linesep),
        file_name="SKU_File.csv",
        mime="text/csv",
    )


def download_syn(conn, df):
    container_height = min(len(df) * 50, 300)
    with st.container():
        st.dataframe(df, height=container_height)
    st.download_button(
        label="Download data as CSV",
        data=df.to_csv(index=False, header=True).rstrip(os.linesep),
        file_name="synonym.csv",
        mime="text/csv",
    )


def download_lang(conn, df):
    container_height = min(len(df) * 50, 300)
    mf = df
    mf.fillna("", inplace=True)
    with st.container():
        st.dataframe(mf, height=container_height)
    st.download_button(
        label="Download data as CSV",
        data=df.to_csv(index=False, header=True).rstrip(os.linesep),
        file_name="lang_File.csv",
        mime="text/csv",
    )


def show_synonym_table(conn, table_name):
    with conn.cursor() as c:
        c.execute(
            'CREATE OR REPLACE VIEW my_syn_view AS SELECT "keywords", "synonym", "type" FROM public."'
            + table_name
            + '" ORDER BY "timestamp" DESC'
        )
        c.execute("SELECT * FROM my_syn_view")
        result = c.fetchall()
        df = pd.DataFrame(result, columns=["key", "synonym", "type"])
        download_syn(conn, df)


def show_sku_table(conn, table_name):
    with conn.cursor() as c:
        c.execute(
            'CREATE OR REPLACE VIEW my_sku_view AS SELECT "SKUID", "SKUName", "ProductType", "Brand", "Category", "SubCategory" FROM public."'
            + table_name
            + '" ORDER BY "timestamp" DESC'
        )
        c.execute("SELECT * FROM my_sku_view")
        result = c.fetchall()
        df = pd.DataFrame(
            result,
            columns=[
                "sku id",
                "SKU Name",
                "Product type",
                "Brand",
                "category",
                "sub category",
            ],
        )
        download_sku(conn, df)


def show_stock_sku_table(conn, table_name):
    with conn.cursor() as c:
        c.execute(
            'CREATE OR REPLACE VIEW my_sku_view AS SELECT * FROM public."'
            + table_name
            + '" ORDER BY "timestamp" DESC'
        )
        c.execute("SELECT * FROM my_sku_view")
        result = c.fetchall()
        df = pd.DataFrame(
            result,
            columns=[
                "Security_name",
                "Bse_code",
                "Nse_code",
                "isin",
                "customer_id",
                "market_cap",
                "username",
                "timestamp",
            ],
        )
        download_sku(conn, df)


def show_iciciNavigation_table(conn, table_name):
    with conn.cursor() as c:
        c.execute(
            'CREATE OR REPLACE VIEW my_sku_view AS SELECT * FROM public."'
            + table_name
            + '"'
        )
        c.execute("SELECT * FROM my_sku_view")
        result = c.fetchall()
        df = pd.DataFrame(result, columns=["key"])
        download_sku(conn, df)


def show_iciciPortfolio_table(conn, table_name):
    with conn.cursor() as c:
        c.execute(
            'CREATE OR REPLACE VIEW my_sku_view AS SELECT "outlook_types", "instruments", "action_targets", "portfolio_types" FROM public."'
            + table_name
            + '"'
        )
        c.execute("SELECT * FROM my_sku_view")
        result = c.fetchall()
        df = pd.DataFrame(
            result,
            columns=[
                "outlook_types",
                "instruments",
                "action_targets",
                "portfolio_types",
            ],
        )
        download_sku(conn, df)


def show_bussku_table(conn, table_name):
    with conn.cursor() as c:
        c.execute(
            'CREATE OR REPLACE VIEW my_bussku_view AS SELECT "terminal_name", "city_name", "province_name", "country_name" FROM public."'
            + table_name
            + '" ORDER BY "timestamp" DESC'
        )
        c.execute("SELECT * FROM my_bussku_view")
        result = c.fetchall()
        df = pd.DataFrame(
            result,
            columns=["terminal_name", "city_name", "province_name", "country_name"],
        )
        download_sku(conn, df)


def show_lang_table(conn, table_name):
    with conn.cursor() as c:
        c.execute(
            'CREATE OR REPLACE VIEW my_lang_view AS SELECT "keywords", "translation", "language", "type" FROM public."'
            + table_name
            + '" ORDER BY "timestamp" DESC'
        )
        c.execute("SELECT * FROM my_lang_view")
        result = c.fetchall()
        df = pd.DataFrame(result, columns=["key", "translation", "language", "type"])
        download_lang(conn, df)


def show_lang_table_username(conn, table_name):
    with conn.cursor() as c:
        with st.form(key="lang_table_user_form", clear_on_submit=True):
            username = st.text_input(
                "Enter the username", value="", key="lang_username_value_input"
            )
            search = st.form_submit_button(label="Search")

        if search:
            if not check_key_exists_column(conn, "users", "username", username):
                st.warning("Invalid Username")
                return
            c.execute(
                'CREATE OR REPLACE VIEW my_lang_view_username AS SELECT "keywords", "translation", "language", "type", "username", "timestamp" FROM public."'
                + table_name
                + '" WHERE "username"=%s ORDER BY "timestamp" DESC',
                (username,),
            )
            c.execute("SELECT * FROM my_lang_view_username")
            result = c.fetchall()
            df = pd.DataFrame(
                result,
                columns=[
                    "key",
                    "translation",
                    "language",
                    "type",
                    "username",
                    "timestamp",
                ],
            )
            mf = df
            mf.fillna("", inplace=True)
            container_height = min(len(mf) * 50, 300)
            with st.container():
                st.dataframe(mf, height=container_height)


def show_lang_table_date(conn, table_name):
    with conn.cursor() as c:
        with st.form(key="lang_table_date_form", clear_on_submit=True):
            from_date = str(
                st.date_input(
                    "Select a date", date.today(), key="from_date_lang_value_input"
                )
            )
            to_date = str(
                st.date_input(
                    "Select a date", date.today(), key="to_date_s_value_input"
                )
            )
            search = st.form_submit_button(label="Search")
        if search:
            c.execute(
                'CREATE OR REPLACE VIEW my_lang_view_date AS SELECT "keywords", "translation", "language", "type", "username", "timestamp" FROM public."'
                + table_name
                + '" WHERE timestamp <> %s AND CAST(timestamp AS DATE) >= %s AND CAST(timestamp AS DATE) <= %s ORDER BY "timestamp" DESC',
                ("0", from_date, to_date),
            )
            c.execute("SELECT * FROM my_lang_view_date")
            result = c.fetchall()
            df = pd.DataFrame(
                result,
                columns=[
                    "key",
                    "translation",
                    "language",
                    "type",
                    "username",
                    "timestamp",
                ],
            )
            mf = df
            mf.fillna("", inplace=True)
            container_height = min(len(mf) * 50, 300)
            with st.container():
                st.dataframe(mf, height=container_height)


def show_lang_table_today(conn, table_name, username):
    with conn.cursor() as c:
        c.execute(
            'CREATE OR REPLACE VIEW my_lang_view_today AS SELECT ""keywords", "translation", "language", "type", "username", "timestamp" FROM public."'
            + table_name
            + '" WHERE username=%s AND CAST(timestamp AS DATE) = %s ORDER BY "timestamp" DESC',
            (username, date.today()),
        )
        c.execute("SELECT * FROM my_lang_view_today")
        result = c.fetchall()
        df = pd.DataFrame(
            result,
            columns=["key", "translation", "language", "type", "username", "timestamp"],
        )
        mf = df
        mf.fillna("", inplace=True)
        container_height = min(len(mf) * 50, 300)
        with st.container():
            st.dataframe(mf, height=container_height)


def show_sku_table_username(conn, table_name):
    with conn.cursor() as c:
        with st.form(key="sku_table_user_form", clear_on_submit=True):
            username = st.text_input(
                "Enter the username", value="", key="sku_username_value_input"
            )
            search = st.form_submit_button(label="Search")

        if search:
            if not check_key_exists_column(conn, "users", "username", username):
                st.warning("Invalid Username")
                return
            c.execute(
                'CREATE OR REPLACE VIEW my_sku_view_username AS SELECT "SKUID", "SKUName", "ProductType", "Brand", "Category", "SubCategory", "username", "timestamp" FROM public."'
                + table_name
                + '" WHERE "username"=%s ORDER BY "timestamp" DESC',
                (username,),
            )
            c.execute("SELECT * FROM my_sku_view_username")
            result = c.fetchall()
            df = pd.DataFrame(
                result,
                columns=[
                    "sku id",
                    "SKU Name",
                    "Product type",
                    "Brand",
                    "category",
                    "sub category",
                    "username",
                    "timestamp",
                ],
            )
            mf = df
            mf.fillna("", inplace=True)
            container_height = min(len(mf) * 50, 300)
            with st.container():
                st.dataframe(mf, height=container_height)


def show_sku_table_date(conn, table_name):
    with conn.cursor() as c:
        with st.form(key="sku_table_date_form", clear_on_submit=True):
            from_date = str(
                st.date_input(
                    "Select a date", date.today(), key="from_date_sku_value_input"
                )
            )
            to_date = str(
                st.date_input(
                    "Select a date", date.today(), key="to_date_s_value_input"
                )
            )
            search = st.form_submit_button(label="Search")
        if search:
            c.execute(
                'CREATE OR REPLACE VIEW my_sku_view_date AS SELECT "SKUID", "SKUName", "ProductType", "Brand", "Category", "SubCategory", "username", "timestamp" FROM public."'
                + table_name
                + '" WHERE timestamp <> %s AND CAST(timestamp AS DATE) >= %s AND CAST(timestamp AS DATE) <= %s ORDER BY "timestamp" DESC',
                ("0", from_date, to_date),
            )
            c.execute("SELECT * FROM my_sku_view_date")
            result = c.fetchall()
            df = pd.DataFrame(
                result,
                columns=[
                    "sku id",
                    "SKU Name",
                    "Product type",
                    "Brand",
                    "category",
                    "sub category",
                    "username",
                    "timestamp",
                ],
            )
            mf = df
            mf.fillna("", inplace=True)
            container_height = min(len(mf) * 50, 300)
            with st.container():
                st.dataframe(mf, height=container_height)


def show_stock_sku_table_username(conn, table_name):
    with conn.cursor() as c:
        with st.form(key="sku_table_user_form", clear_on_submit=True):
            username = st.text_input(
                "Enter the username", value="", key="sku_username_value_input"
            )
            search = st.form_submit_button(label="Search")

        if search:
            if not check_key_exists_column(conn, "users", "username", username):
                st.warning("Invalid Username")
                return
            c.execute(
                'CREATE OR REPLACE VIEW my_sku_view_username AS SELECT * FROM public."'
                + table_name
                + '" WHERE "username"=%s ORDER BY "timestamp" DESC',
                (username,),
            )
            c.execute("SELECT * FROM my_sku_view_username")
            result = c.fetchall()
            df = pd.DataFrame(
                result,
                columns=[
                    "sku id",
                    "Security_name",
                    "Bse_code",
                    "nse_code",
                    "isin",
                    "customer_id",
                    "market_cap" "username",
                    "timestamp",
                ],
            )
            mf = df
            mf.fillna("", inplace=True)
            container_height = min(len(mf) * 50, 300)
            with st.container():
                st.dataframe(mf, height=container_height)


def show_stock_sku_table_date(conn, table_name):
    with conn.cursor() as c:
        with st.form(key="sku_table_date_form", clear_on_submit=True):
            from_date = str(
                st.date_input(
                    "Select a date", date.today(), key="from_date_sku_value_input"
                )
            )
            to_date = str(
                st.date_input(
                    "Select a date", date.today(), key="to_date_s_value_input"
                )
            )
            search = st.form_submit_button(label="Search")
        if search:
            c.execute(
                'CREATE OR REPLACE VIEW my_sku_view_date AS SELECT * FROM public."'
                + table_name
                + '" WHERE timestamp <> %s AND CAST(timestamp AS DATE) >= %s AND CAST(timestamp AS DATE) <= %s ORDER BY "timestamp" DESC',
                ("0", from_date, to_date),
            )
            c.execute("SELECT * FROM my_sku_view_date")
            result = c.fetchall()
            df = pd.DataFrame(
                result,
                columns=[
                    "sku id",
                    "Security_name",
                    "Bse_code",
                    "nse_code",
                    "isin",
                    "customer_id",
                    "market_cap" "username",
                    "timestamp",
                ],
            )
            mf = df
            mf.fillna("", inplace=True)
            container_height = min(len(mf) * 50, 300)
            with st.container():
                st.dataframe(mf, height=container_height)


def show_sku_table_today(conn, table_name, username):
    with conn.cursor() as c:
        c.execute(
            'CREATE OR REPLACE VIEW my_sku_view_date AS SELECT "SKUID", "SKUName", "ProductType", "Brand", "Category", "SubCategory", "username", "timestamp" FROM public."'
            + table_name
            + '" WHERE username=%s AND CAST(timestamp AS DATE) = %s ORDER BY "timestamp" DESC',
            (username, date.today()),
        )
        c.execute("SELECT * FROM my_sku_view_date")
        result = c.fetchall()
        df = pd.DataFrame(
            result,
            columns=[
                "sku id",
                "SKU Name",
                "Product type",
                "Brand",
                "category",
                "sub category",
                "username",
                "timestamp",
            ],
        )
        mf = df
        mf.fillna("", inplace=True)
        container_height = min(len(mf) * 50, 300)
        with st.container():
            st.dataframe(mf, height=container_height)


def show_stock_sku_table_today(conn, table_name, username):
    with conn.cursor() as c:
        c.execute(
            'CREATE OR REPLACE VIEW my_sku_view_date AS SELECT * FROM public."'
            + table_name
            + '" WHERE username=%s AND CAST(timestamp AS DATE) = %s ORDER BY "timestamp" DESC',
            (username, date.today()),
        )
        c.execute("SELECT * FROM my_sku_view_date")
        result = c.fetchall()
        df = pd.DataFrame(
            result,
            columns=[
                "security_name",
                "bse_code",
                "nse_code",
                "isin",
                "customer_id",
                "market_cap",
                "username",
                "timestamp",
            ],
        )
        mf = df
        mf.fillna("", inplace=True)
        container_height = min(len(mf) * 50, 300)
        with st.container():
            st.dataframe(mf, height=container_height)


def show_bussku_table_username(conn, table_name):
    with conn.cursor() as c:
        with st.form(key="sku_table_user_form", clear_on_submit=True):
            username = st.text_input(
                "Enter the username", value="", key="sku_username_value_input"
            )
            search = st.form_submit_button(label="Search")

        if search:
            if not check_key_exists_column(conn, "users", "username", username):
                st.warning("Invalid Username")
                return
            c.execute(
                'CREATE OR REPLACE VIEW my_sku_view_username AS SELECT "terminal_name", "city_name", "province_name", "country_name", "username", "timestamp" FROM public."'
                + table_name
                + '" WHERE "username"=%s ORDER BY "timestamp" DESC',
                (username,),
            )
            c.execute("SELECT * FROM my_sku_view_username")
            result = c.fetchall()
            df = pd.DataFrame(
                result,
                columns=[
                    "terminal_name",
                    "city_name",
                    "province_name",
                    "country_name",
                    "username",
                    "timestamp",
                ],
            )
            mf = df
            mf.fillna("", inplace=True)
            container_height = min(len(mf) * 50, 300)
            with st.container():
                st.dataframe(mf, height=container_height)


def show_bussku_table_date(conn, table_name):
    with conn.cursor() as c:
        with st.form(key="sku_table_date_form", clear_on_submit=True):
            from_date = str(
                st.date_input(
                    "Select a date", date.today(), key="from_date_sku_value_input"
                )
            )
            to_date = str(
                st.date_input(
                    "Select a date", date.today(), key="to_date_s_value_input"
                )
            )
            search = st.form_submit_button(label="Search")
        if search:
            c.execute(
                'CREATE OR REPLACE VIEW my_sku_view_date AS SELECT "terminal_name", "city_name", "province_name", "country_name", "username", "timestamp" FROM public."'
                + table_name
                + '" WHERE timestamp <> %s AND CAST(timestamp AS DATE) >= %s AND CAST(timestamp AS DATE) <= %s ORDER BY "timestamp" DESC',
                ("0", from_date, to_date),
            )
            c.execute("SELECT * FROM my_sku_view_date")
            result = c.fetchall()
            df = pd.DataFrame(
                result,
                columns=[
                    "terminal_name",
                    "city_name",
                    "province_name",
                    "country_name",
                    "username",
                    "timestamp",
                ],
            )
            mf = df
            mf.fillna("", inplace=True)
            container_height = min(len(mf) * 50, 300)
            with st.container():
                st.dataframe(mf, height=container_height)


def show_bussku_table_today(conn, table_name, username):
    with conn.cursor() as c:
        c.execute(
            'CREATE OR REPLACE VIEW my_sku_view_date AS SELECT "terminal_name", "city_name", "province_name", "country_name", "username", "timestamp" FROM public."'
            + table_name
            + '" WHERE username=%s AND CAST(timestamp AS DATE) = %s ORDER BY "timestamp" DESC',
            (username, date.today()),
        )
        c.execute("SELECT * FROM my_sku_view_date")
        result = c.fetchall()
        df = pd.DataFrame(
            result,
            columns=[
                "terminal_name",
                "city_name",
                "province_name",
                "country_name",
                "username",
                "timestamp",
            ],
        )
        mf = df
        mf.fillna("", inplace=True)
        container_height = min(len(mf) * 50, 300)
        with st.container():
            st.dataframe(mf, height=container_height)


def show_syn_table_username(conn, table_name):
    with conn.cursor() as c:
        with st.form(key="syn_table_user_form", clear_on_submit=True):
            username = st.text_input(
                "Enter the username", value="", key="syn_username_value_input"
            )
            search = st.form_submit_button(label="Search")
        if search:
            if not check_key_exists_column(conn, "users", "username", username):
                st.warning("Invalid Username")
                return
            c.execute(
                'CREATE OR REPLACE VIEW my_syn_view_username AS SELECT "keywords", "synonym", "type", "username", "timestamp" FROM public."'
                + table_name
                + '" WHERE "username"=%s ORDER BY "timestamp" DESC',
                (username,),
            )
            c.execute("SELECT * FROM my_syn_view_username")
            result = c.fetchall()
            df = pd.DataFrame(
                result, columns=["keywords", "synonym", "type", "username", "timestamp"]
            )
            mf = df
            mf.fillna("", inplace=True)
            container_height = min(len(mf) * 50, 300)
            with st.container():
                st.dataframe(mf, height=container_height)


def show_syn_table_date(conn, table_name):
    with conn.cursor() as c:
        with st.form(key="syn_table_date_form", clear_on_submit=True):
            from_date = str(
                st.date_input(
                    "Select a date", date.today(), key="from_date_syn_value_input"
                )
            )
            to_date = str(
                st.date_input(
                    "Select a date", date.today(), key="to_date_syn_value_input"
                )
            )
            search = st.form_submit_button(label="Search")
        if search:
            c.execute(
                'CREATE OR REPLACE VIEW my_syn_view_date AS SELECT "keywords", "synonym", "type", "username", "timestamp" FROM public."'
                + table_name
                + '" WHERE timestamp <> %s AND CAST(timestamp AS DATE) >= %s AND CAST(timestamp AS DATE) <= %s ORDER BY "timestamp" DESC',
                ("0", from_date, to_date),
            )
            c.execute("SELECT * FROM my_syn_view_date")
            result = c.fetchall()
            df = pd.DataFrame(
                result, columns=["keywords", "synonym", "type", "username", "timestamp"]
            )
            mf = df
            mf.fillna("", inplace=True)
            container_height = min(len(mf) * 50, 300)
            with st.container():
                st.dataframe(mf, height=container_height)


def show_syn_table_today(conn, table_name, username):
    with conn.cursor() as c:
        c.execute(
            'CREATE OR REPLACE VIEW my_syn_view_date AS SELECT "keywords", "synonym", "type", "username", "timestamp" FROM public."'
            + table_name
            + '" WHERE username=%s AND CAST(timestamp AS DATE) = %s ORDER BY "timestamp" DESC',
            (username, date.today()),
        )
        c.execute("SELECT * FROM my_syn_view_date")
        result = c.fetchall()
        df = pd.DataFrame(
            result, columns=["keywords", "synonym", "type", "username", "timestamp"]
        )
        mf = df
        mf.fillna("", inplace=True)
        container_height = min(len(mf) * 50, 300)
        with st.container():
            st.dataframe(mf, height=container_height)


def validate_credentials(conn, username, password):
    with conn.cursor() as c:
        c.execute(
            "SELECT * FROM users WHERE username = %s AND password = %s",
            (username, password),
        )
        return c.fetchone() is not None


def register_page(conn):
    st.header("Register")
    new_username = st.text_input("Username", key="new_user_input")
    new_password = st.text_input("Password", type="password", key="new_pass_input")
    salt = "2Ld4"
    hash1 = hashlib.md5(salt.encode("utf-8") + new_password.encode("utf-8")).hexdigest()
    if st.button("Register"):
        if new_username == "" or new_password == "":
            st.error("Invalid username or password")
            return
        if not check_key_exists_column(conn, "users", "username", new_username):
            create_user(conn, new_username, hash1)
            st.success("User registered successfully!")
        else:
            st.error("Username already exists")
            return


def login_page(conn):
    st.header("")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    salt = "2Ld4"
    hash1 = hashlib.md5(salt.encode("utf-8") + password.encode("utf-8")).hexdigest()
    if st.button("Login"):
        if not check_key_exists_column(conn, "users", "username", username):
            st.warning("Invalid Username")
            return
        if not check_key_exists_column(conn, "users", "password", hash1):
            st.warning("Invalid password")
            return
        if validate_credentials(conn, username, hash1):
            st.success("Logged in successfully!")
            st.session_state["page"] = "dashboard"
            st.session_state["value_from_main"] = username
            return True
        else:
            st.error("Invalid username or password.")
            st.experimental_rerun()
    return False


def sku_search(conn, table_name2, sku_value, table_name1):
    with conn.cursor() as c:
        c.execute(
            'SELECT "Brand" FROM public."' + table_name1 + '" WHERE "Brand" = %s',
            (sku_value,),
        )
        result = c.fetchall()
        if result:
            df = pd.DataFrame(result, columns=["Brand"])
            container_height = min(len(df) * 50, 300)
            with st.container():
                st.dataframe(df, height=container_height)
            return
        c.execute(
            'SELECT "ProductType" FROM public."'
            + table_name1
            + '" WHERE "ProductType" = %s',
            (sku_value,),
        )
        result = c.fetchall()
        if result:
            df = pd.DataFrame(result, columns=["Product Type"])
            container_height = min(len(df) * 50, 300)
            with st.container():
                st.dataframe(df, height=container_height)
            return
        c.execute(
            'SELECT * FROM public."' + table_name2 + '" WHERE "keywords" = %s',
            (sku_value,),
        )
        result = c.fetchall()
        if result:
            df = pd.DataFrame(result, columns=["Variants"])
            container_height = min(len(df) * 50, 300)
            with st.container():
                st.dataframe(df, height=container_height)
        else:
            st.error("Data not found")


def stock_sku_search(conn, table_name, security_name):
    with conn.cursor() as c:
        c.execute(
            'SELECT * FROM public."' + table_name + '" WHERE "Security_Name" = %s',
            (security_name,),
        )
        result = c.fetchall()
        if result:
            df = pd.DataFrame(
                result,
                columns=[
                    "Security_name",
                    "BSE_code",
                    "NSE_code",
                    "ISIN",
                    "Customer_id",
                    "market_cap",
                    "username",
                    "timestamp",
                ],
            )
            container_height = min(len(df) * 50, 300)
            with st.container():
                st.dataframe(df, height=container_height)
            return
        else:
            st.error("Data not found")


def bussku_search(
    conn, table_name1, terminal_value, city_value, province_value, country_value
):
    with conn.cursor() as c:
        if terminal_value != "" and city_value != "" and province_value != "":
            c.execute(
                'SELECT * FROM public."'
                + table_name1
                + '" WHERE terminal_name=%s and city_name=%s and province_name=%s',
                (terminal_value, city_value, province_value),
            )
            result = c.fetchall()
            if result:
                df = pd.DataFrame(
                    result,
                    columns=[
                        "terminal_name",
                        "city_name",
                        "province_name",
                        "country_name",
                        "username",
                        "timestamp",
                    ],
                )
                mf = df
                mf.fillna("", inplace=True)
                container_height = min(len(mf) * 50, 300)
                with st.container():
                    st.dataframe(df, height=container_height)
        elif city_value != "" and province_value != "":
            c.execute(
                'SELECT * FROM public."'
                + table_name1
                + '" WHERE city_name=%s and province_name=%s',
                (city_value, province_value),
            )
            result = c.fetchall()
            if result:
                df = pd.DataFrame(
                    result,
                    columns=[
                        "terminal_name",
                        "city_name",
                        "province_name",
                        "country_name",
                        "username",
                        "timestamp",
                    ],
                )
                mf = df
                mf.fillna("", inplace=True)
                container_height = min(len(mf) * 50, 300)
                with st.container():
                    st.dataframe(df, height=container_height)
        elif (
            terminal_value == ""
            and city_value != ""
            and province_value == ""
            and country_value != ""
        ):
            c.execute(
                'SELECT * FROM public."'
                + table_name1
                + '" WHERE terminal_value=%s and city_name=%s and province_name=%s and country_name=%s',
                ("", city_value, "", country_value),
            )
            result = c.fetchall()
            if result:
                df = pd.DataFrame(
                    result,
                    columns=[
                        "terminal_name",
                        "city_name",
                        "province_name",
                        "country_name",
                        "username",
                        "timestamp",
                    ],
                )
                mf = df
                mf.fillna("", inplace=True)
                container_height = min(len(mf) * 50, 300)
                with st.container():
                    st.dataframe(df, height=container_height)
        elif (
            terminal_value != ""
            and city_value == ""
            and province_value == ""
            and country_value == ""
        ):
            c.execute(
                'SELECT * FROM public."'
                + table_name1
                + '" WHERE terminal_name=%s or city_name=%s or province_name=%s or country_name=%s',
                (terminal_value, terminal_value, terminal_value, terminal_value),
            )
            result = c.fetchall()
            if result:
                df = pd.DataFrame(
                    result,
                    columns=[
                        "terminal_name",
                        "city_name",
                        "province_name",
                        "country_name",
                        "username",
                        "timestamp",
                    ],
                )
                mf = df
                mf.fillna("", inplace=True)
                container_height = min(len(mf) * 50, 300)
                with st.container():
                    st.dataframe(df, height=container_height)
            else:
                st.error("Data not found")
        elif (
            terminal_value == ""
            and city_value != ""
            and province_value == ""
            and country_value == ""
        ):
            c.execute(
                'SELECT * FROM public."'
                + table_name1
                + '" WHERE terminal_name=%s or city_name=%s or province_name=%s or country_name=%s',
                (city_value, city_value, city_value, city_value),
            )
            result = c.fetchall()
            if result:
                df = pd.DataFrame(
                    result,
                    columns=[
                        "terminal_name",
                        "city_name",
                        "province_name",
                        "country_name",
                        "username",
                        "timestamp",
                    ],
                )
                mf = df
                mf.fillna("", inplace=True)
                container_height = min(len(mf) * 50, 300)
                with st.container():
                    st.dataframe(df, height=container_height)
            else:
                st.error("Data not found")
        elif (
            terminal_value == ""
            and city_value == ""
            and province_value != ""
            and country_value == ""
        ):
            c.execute(
                'SELECT * FROM public."'
                + table_name1
                + '" WHERE terminal_name=%s or city_name=%s or province_name=%s or country_name=%s',
                (province_value, province_value, province_value, province_value),
            )
            result = c.fetchall()
            if result:
                df = pd.DataFrame(
                    result,
                    columns=[
                        "terminal_name",
                        "city_name",
                        "province_name",
                        "country_name",
                        "username",
                        "timestamp",
                    ],
                )
                mf = df
                mf.fillna("", inplace=True)
                container_height = min(len(mf) * 50, 300)
                with st.container():
                    st.dataframe(df, height=container_height)
            else:
                st.error("Data not found")
        elif (
            terminal_value == ""
            and city_value == ""
            and province_value == ""
            and country_value != ""
        ):
            c.execute(
                'SELECT * FROM public."'
                + table_name1
                + '" WHERE terminal_name=%s or city_name=%s or province_name=%s or country_name=%s',
                (country_value, country_value, country_value, country_value),
            )
            result = c.fetchall()
            if result:
                df = pd.DataFrame(
                    result,
                    columns=[
                        "terminal_name",
                        "city_name",
                        "province_name",
                        "country_name",
                        "username",
                        "timestamp",
                    ],
                )
                mf = df
                mf.fillna("", inplace=True)
                container_height = min(len(mf) * 50, 300)
                with st.container():
                    st.dataframe(df, height=container_height)
            else:
                st.error("Data not found")


def global_search(conn, table_name, sku_value):
    with conn.cursor() as c:
        try:
            c.execute(
                'SELECT "SKUName" FROM public."'
                + table_name
                + '" WHERE "SKUName" = %s',
                (sku_value,),
            )
            result = c.fetchall()
            if result:
                df = pd.DataFrame(result, columns=["Variants"])
                container_height = min(len(df) * 50, 300)
                with st.container():
                    st.dataframe(df, height=container_height)
                return
        except ValueError as e:
            st.error(e)
        try:
            c.execute(
                'SELECT "ProductType" FROM public."'
                + table_name
                + '" WHERE "ProductType" = %s',
                (sku_value,),
            )
            result = c.fetchall()
            if result:
                df = pd.DataFrame(result, columns=["Product Type"])
                container_height = min(len(df) * 50, 300)
                with st.container():
                    st.dataframe(df, height=container_height)
                return
        except ValueError as e:
            st.error(e)
        try:
            c.execute(
                'SELECT "Brand" FROM public."' + table_name + '" WHERE "Brand" = %s',
                (sku_value,),
            )
            result = c.fetchall()
            if result:
                df = pd.DataFrame(result, columns=["Brand"])
                container_height = min(len(df) * 50, 300)
                with st.container():
                    st.dataframe(df, height=container_height)
                return
        except ValueError as e:
            st.error(e)
        else:
            st.error("Data not found")


def remove_global_sku(conn, table_name, sku_value, type2):
    with conn.cursor() as c:
        if table_name == "b&c_global":
            if check_key_exists_column(conn, "b&c_global_syn", "keywords", sku_value):
                st.warning(
                    "The word exists in b&c synonyms table, Hence can not be deleted here"
                )
                return
            if check_key_exists_column(conn, "b&c_global_lang", "keywords", sku_value):
                st.warning(
                    "The word exists in b&c language table, Hence can not be deleted here"
                )
                return
            if check_key_exists_column(conn, "NykaaUniqueWords", "keywords", sku_value):
                st.warning(
                    "The word exists in Nykaa SKU, Hence can not be deleted here"
                )
                return
        if table_name == "grocery_global":
            if check_key_exists_column(
                conn, "grocery_global_syn", "keywords", sku_value
            ):
                st.warning(
                    "The word exists in grocery synonyms table, Hence can not be deleted here"
                )
                return
            if check_key_exists_column(
                conn, "grocery_global_lang", "keywords", sku_value
            ):
                st.warning(
                    "The word exists in grocery language table, Hence can not be deleted here"
                )
                return
            if check_key_exists_column(
                conn, "ApnaklubUniqueWords", "keywords", sku_value
            ):
                st.warning(
                    "The word exists in Apnaklub SKU, Hence can not be deleted here"
                )
                return
            if check_key_exists_column(conn, "OtipyUniqueWords", "keywords", sku_value):
                st.warning(
                    "The word exists in Zepto SKU, Hence can not be deleted here"
                )
                return
        if table_name == "fashion_global":
            if check_key_exists_column(
                conn, "fashion_global_syn", "keywords", sku_value
            ):
                st.warning(
                    "The word exists in grocery synonyms table, Hence can not be deleted here"
                )
                return
            if check_key_exists_column(
                conn, "fashion_global_lang", "keywords", sku_value
            ):
                st.warning(
                    "The word exists in grocery language table, Hence can not be deleted here"
                )
                return
            if check_key_exists_column(
                conn, "FashionUniqueWords", "keywords", sku_value
            ):
                st.warning(
                    "The word exists in Apnaklub SKU, Hence can not be deleted here"
                )
                return
        if table_name == "pharmacy_global":
            if check_key_exists_column(
                conn, "pharmacy_global_syn", "keywords", sku_value
            ):
                st.warning(
                    "The word exists in grocery synonyms table, Hence can not be deleted here"
                )
                return
            if check_key_exists_column(
                conn, "pharmacy_global_lang", "keywords", sku_value
            ):
                st.warning(
                    "The word exists in grocery language table, Hence can not be deleted here"
                )
                return
            if check_key_exists_column(
                conn, "PharmacyUniqueWords", "keywords", sku_value
            ):
                st.warning(
                    "The word exists in Apnaklub SKU, Hence can not be deleted here"
                )
                return
        if type2 == "sku":
            col_name = "SKUName"
            if not check_key_exists_column(conn, table_name, col_name, sku_value):
                st.warning("The word does not exist in SKU Name column")
                return
            try:
                c.execute(
                    'UPDATE public."'
                    + table_name
                    + '" SET "SKUName"=NULL WHERE "SKUName"=%s',
                    (sku_value,),
                )
                conn.commit()
                st.success("Successful deletion of the given SKU")
            except IntegrityError as e:
                st.error(e)
        elif type2 == "product_type":
            col_name = "ProductType"
            if not check_key_exists_column(conn, table_name, col_name, sku_value):
                st.warning("The word does not exist in product type column")
                return
            try:
                c.execute(
                    'UPDATE public."'
                    + table_name
                    + '" SET "ProductType"=NULL WHERE "ProductType"=%s',
                    (sku_value,),
                )
                conn.commit()
                st.success("Successful deletion of the given product type")
            except IntegrityError as e:
                st.error(e)
        elif type2 == "brand":
            col_name = "Brand"
            if not check_key_exists_column(conn, table_name, col_name, sku_value):
                st.warning("The word does not exist in brand column")
                return
            try:
                c.execute(
                    'UPDATE public."'
                    + table_name
                    + '" SET "Brand"=NULL WHERE "Brand"=%s',
                    (sku_value,),
                )
                conn.commit()
                st.success("Successful deletion of the given brand")
            except IntegrityError as e:
                st.error(e)

        c.execute(
            'DELETE from public."'
            + table_name
            + '" WHERE "SKUName" is NULL and "ProductType" is NULL and "Brand" is NULL'
        )
        conn.commit()


def remove_global_bussku(
    conn, table_name1, terminal_value, city_value, province_value, country_value
):
    with conn.cursor() as c:
        if (
            terminal_value != ""
            and city_value != ""
            and province_value != ""
            and country_value != ""
        ):
            try:
                c.execute(
                    'DELETE from public."'
                    + table_name1
                    + '" WHERE "terminal_name"=%s and "city_name"=%s and "province_name"=%s and "country_name"=%s',
                    (terminal_value, city_value, province_value, country_value),
                )
                conn.commit()
                st.success("Successful deletion of the record")
            except IntegrityError as e:
                st.error("Invalid values to delete")
        elif terminal_value != "" and city_value != "" and province_value != "":
            try:
                c.execute(
                    'DELETE from public."'
                    + table_name1
                    + '" WHERE "terminal_name"=%s and "city_name"=%s and "province_name"=%s',
                    (terminal_value, city_value, province_value),
                )
                conn.commit()
                st.success("Successful deletion of the record")
            except IntegrityError as e:
                st.error("Invalid values to delete")
        elif terminal_value == "" and city_value != "" and province_value != "":
            try:
                c.execute(
                    'DELETE from public."'
                    + table_name1
                    + '" WHERE "terminal_name"=%s and "city_name"=%s and "province_name"=%s',
                    ("", city_value, province_value),
                )
                conn.commit()
                st.success("Successful deletion of the record")
            except IntegrityError as e:
                st.error("Invalid values to delete")
        elif terminal_value != "":
            if not check_key_exists_column(
                conn, table_name1, "terminal_name", terminal_value
            ):
                st.warning("The word does not exist in Ternimal Name column")
                return 0
            try:
                c.execute(
                    'UPDATE public."'
                    + table_name1
                    + '" SET "terminal_name"=%s WHERE "terminal_name"=%s',
                    (
                        "",
                        terminal_value,
                    ),
                )
                conn.commit()
                st.success("Successful deletion of the given terminal name")
            except IntegrityError as e:
                st.error(e)

        c.execute(
            'DELETE from public."{}" WHERE "terminal_name" = \'{}\' and "city_name" = \'{}\' and "province_name" = \'{}\' and "country_name" = \'{}\''.format(
                table_name1, "", "", "", ""
            )
        )
        conn.commit()


def remove_sku(conn, table_name, sku_value, type2):
    with conn.cursor() as c:
        if type2 == "variant":
            col_name = "SKUName"
            if not check_key_exists_column(conn, table_name, col_name, sku_value):
                st.warning("The word does not exist in SKU Name column")
                return 0
            try:
                c.execute(
                    'UPDATE public."'
                    + table_name
                    + '" SET "SKUName"=NULL WHERE "SKUName"=%s',
                    (sku_value,),
                )
                conn.commit()
                st.success("Successful deletion of the given SKU")
            except IntegrityError as e:
                st.error(e)
        elif type2 == "product_type":
            col_name = "ProductType"
            if not check_key_exists_column(conn, table_name, col_name, sku_value):
                st.warning("The word does not exist in product type column")
                return 0
            try:
                c.execute(
                    'UPDATE public."'
                    + table_name
                    + '" SET "ProductType"=NULL WHERE "ProductType"=%s',
                    (sku_value,),
                )
                conn.commit()
                st.success("Successful deletion of the given product type")
            except IntegrityError as e:
                st.error(e)
        elif type2 == "brand":
            col_name = "Brand"
            if not check_key_exists_column(conn, table_name, col_name, sku_value):
                st.warning("The word does not exist in brand column")
                return 0
            try:
                c.execute(
                    'UPDATE public."'
                    + table_name
                    + '" SET "Brand"=NULL WHERE "Brand"=%s',
                    (sku_value,),
                )
                conn.commit()
                st.success("Successful deletion of the given brand")
            except IntegrityError as e:
                st.error(e)

        c.execute(
            'DELETE from public."'
            + table_name
            + '" WHERE "SKUName" is NULL and "ProductType" is NULL and "Brand" is NULL'
        )
        conn.commit()


def remove_stock_sku(conn, table_name, security_name):
    with conn.cursor() as c:
        if not check_key_exists_column(
            conn, table_name, "Security_Name", security_name
        ):
            st.warning("The word does not exist in SKU Name column")
            return 0
        try:
            c.execute(
                'DELETE from public."' + table_name + '" WHERE "Security_Name"=%s',
                (security_name,),
            )
            conn.commit()
            st.success("Successful deletion of the given SKU")
        except IntegrityError as e:
            st.error(e)


def remove_sku_unique(conn, table_name, sku_value):
    with conn.cursor() as c:
        if table_name == "NykaaUniqueWords":
            t1 = "nykaa_synonyms"
            t2 = "nykaa_lang"
        elif table_name == "OtipyUniqueWords":
            t1 = "otipy_synonyms"
            t2 = "otipy_lang"
        elif table_name == "ApnaklubUniqueWords":
            t1 = "apnaklub_synonyms"
            t2 = "apnaklub_lang"
        elif table_name == "MedibikriUniqueWords":
            t1 = "medibikri_synonyms"
            t2 = "medibikri_lang"
        if not check_no_duplicate(conn, t1, "keywords", sku_value):
            st.warning("SKU exist in Synonym sheet! Hence can not delete here. ")
            return 0
        if not check_no_duplicate(conn, t2, "keywords", sku_value):
            st.warning("SKU exist in language sheet! Hence can not delete here. ")
            return 0
        try:
            c.execute(
                'SELECT COUNT(*) FROM public."' + table_name + '" WHERE "keywords"=%s',
                (sku_value,),
            )
            result = c.fetchall()
            if result[0][0] > 0:
                try:
                    c.execute(
                        'delete from public."' + table_name + '" WHERE "keywords"=%s',
                        (sku_value,),
                    )
                    conn.commit()
                    return 1
                except IntegrityError as e:
                    st.error(e)
        except IntegrityError as e:
            st.error(e)


def add_sku(conn, table_name, sku_value, type2, username):
    with conn.cursor() as c:
        if (
            check_key_exists_column(conn, table_name, "SKUName", sku_value)
            or check_key_exists_column(conn, table_name, "ProductType", sku_value)
            or check_key_exists_column(conn, table_name, "Brand", sku_value)
        ):
            st.warning(
                "SKU Value already exists in the "
                + table_name
                + " table! Please enter a valid SKU."
            )
            return
        if type2 == "variant":
            try:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                c.execute(
                    'INSERT INTO public."'
                    + table_name
                    + '" ("SKUName", "username", "timestamp") VALUES (%s, %s, %s)',
                    (sku_value, username, timestamp),
                )
                conn.commit()
                st.success(
                    "SKU inserted successful into SKU Name column in the table "
                    + table_name
                    + ""
                )
            except IntegrityError as e:
                st.error("SKU alredy exist in " + table_name)
        elif type2 == "product_type":
            try:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                c.execute(
                    'INSERT INTO public."'
                    + table_name
                    + '" ("ProductType", "username", "timestamp") VALUES (%s, %s, %s)',
                    (sku_value, username, timestamp),
                )
                conn.commit()
                st.success(
                    "SKU inserted successful into product type columnin the table "
                    + table_name
                    + ""
                )
            except IntegrityError as e:
                st.error("SKU alredy exist in " + table_name)
        elif type2 == "brand":
            try:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                c.execute(
                    'INSERT INTO public."'
                    + table_name
                    + '" ("Brand", "username", "timestamp") VALUES (%s, %s, %s)',
                    (sku_value, username, timestamp),
                )
                conn.commit()
                st.success(
                    "SKU inserted successful into brands in the table "
                    + table_name
                    + ""
                )
            except IntegrityError as e:
                st.error("SKU alredy exist in " + table_name)


def add_sku_stock(
    conn,
    table_name,
    security_name,
    bse_code,
    nse_code,
    isin,
    customer_id,
    market_cap,
    username,
):
    with conn.cursor() as c:
        if (
            check_key_exists_column(conn, table_name, "Security_Name", security_name)
            or check_key_exists_column(conn, table_name, "BSE_code", bse_code)
            or check_key_exists_column(conn, table_name, "NSE_Code", nse_code)
            or check_key_exists_column(conn, table_name, "ISIN", isin)
        ):
            st.warning(
                "Stock Value already exists in the "
                + table_name
                + " table! Please enter a valid stock."
            )
            return
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute(
                'INSERT INTO public."'
                + table_name
                + '" ("Security_Name","BSE_code", "NSE_Code", "ISIN", "Custom_id", "Market_Cap", "username", "timestamp") VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                (
                    security_name,
                    bse_code,
                    nse_code,
                    isin,
                    customer_id,
                    market_cap,
                    username,
                    timestamp,
                ),
            )
            conn.commit()
            st.success("Stock inserted successful into " + table_name + "")
        except IntegrityError as e:
            st.error("Stock alredy exist in " + table_name)


def add_bussku(
    conn,
    table_name1,
    terminal_value,
    city_value,
    province_value,
    country_value,
    username,
):
    with conn.cursor() as c:
        if (
            terminal_value != ""
            and city_value == ""
            and province_value == ""
            and country_value == ""
        ):
            if check_key_exists_column(
                conn, table_name1, "terminal_name", terminal_value
            ):
                st.warning(
                    "Given details Value already exists in the "
                    + table_name1
                    + " table! Please enter a valid detail."
                )
                return
        if (
            terminal_value == ""
            and city_value != ""
            and province_value == ""
            and country_value == ""
        ):
            if check_key_exists_column(conn, table_name1, "city_name", city_value):
                st.warning(
                    "Given details Value already exists in the "
                    + table_name1
                    + " table! Please enter a valid detail."
                )
                return
        if (
            terminal_value == ""
            and city_value == ""
            and province_value != ""
            and country_value == ""
        ):
            if check_key_exists_column(
                conn, table_name1, "province_name", province_value
            ):
                st.warning(
                    "Given details Value already exists in the "
                    + table_name1
                    + " table! Please enter a valid detail."
                )
                return
        if (
            terminal_value == ""
            and city_value == ""
            and province_value == ""
            and country_value != ""
        ):
            if check_key_exists_column(
                conn, table_name1, "country_name", country_value
            ):
                st.warning(
                    "Given details Value already exists in the "
                    + table_name1
                    + " table! Please enter a valid detail."
                )
                return
        if terminal_value == "" and city_value != "" and province_value != "":
            try:
                c.execute(
                    'SELECT COUNT(*) FROM public."'
                    + table_name1
                    + '" WHERE "terminal_name"=%s and "city_name"= %s and "province_name"= %s and "country_name"= %s',
                    ("", city_value, province_value, "india"),
                )
                result = c.fetchone()
                if result[0] > 0:
                    st.warning(
                        "Given details Value already exists in the "
                        + table_name1
                        + " table! Please enter a valid detail."
                    )
                    return
            except IntegrityError as e:
                st.error("Details could not be inserted in " + table_name1)
        if terminal_value != "" and city_value != "" and province_value != "":
            try:
                c.execute(
                    'SELECT COUNT(*) FROM public."'
                    + table_name1
                    + '" WHERE "terminal_name"= %s and "city_name"= %s and "province_name"= %s and "country_name"= %s',
                    (terminal_value, city_value, province_value, country_value),
                )
                result = c.fetchone()
                if result[0] > 0:
                    st.warning(
                        "Given details Value already exists in the "
                        + table_name1
                        + " table! Please enter a valid detail."
                    )
                    return
            except IntegrityError as e:
                st.error("Details could not be inserted in " + table_name1)
        if terminal_value != "":
            if check_key_exists_column(
                conn, table_name1, "terminal_name", terminal_value
            ):
                st.warning(
                    "Given details Value already exists in the "
                    + table_name1
                    + " table! Please enter a valid detail."
                )
                return

        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute(
                'INSERT INTO public."'
                + table_name1
                + '" ("terminal_name", "city_name", "province_name", "country_name", "username", "timestamp") VALUES (%s, %s, %s, %s, %s, %s)',
                (
                    terminal_value,
                    city_value,
                    province_value,
                    country_value,
                    username,
                    timestamp,
                ),
            )
            conn.commit()
            st.success("Details inserted successful into the table " + table_name1 + "")
        except IntegrityError as e:
            st.error("Details could not be inserted in " + table_name1)


def add_sku_unique(conn, table_name, sku_value):
    with conn.cursor() as c:
        if not check_no_duplicate(conn, table_name, "keywords", sku_value):
            st.warning(sku_value + " already exists in " + table_name)
        else:
            try:
                c.execute(
                    'INSERT INTO public."' + table_name + '" ("keywords") VALUES (%s)',
                    (sku_value,),
                )
                conn.commit()
            except IntegrityError as e:
                st.error("Value already exists in the UniqueWords")


def validate_input(input_text):
    pattern = r'^[A-Za-z0-9 !@#$%^&*(),.?":{}|<>]+$'
    if not re.match(pattern, input_text):
        raise ValueError("Only English alphabets, numbers, and symbols are allowed.")
    return input_text


def validate_input_lang(input_text):
    pattern = r"^[A-Za-z]+$"
    if re.match(pattern, input_text):
        raise ValueError("English alphabets are not allowed.")
    return input_text


def skufix(username, table_name1, table_name2):
    conn = establish_connection()
    if conn is None:
        return
    with st.form(key="sku_form", clear_on_submit=True):
        sku_value = st.text_input("Enter the sku word", value="", key="sku_value_input")
        sku_value = sku_value.lower()
        sku_value = normalize_str(sku_value)
        option_name = ["variant", "product_type", "brand"]
        type2 = st.radio(
            "Choose the Type (Optional for search)", option_name, key="radio_options"
        )
        col1, col2, col3, col4 = st.columns(4)
        search = col1.form_submit_button(label="Search")
        add = col2.form_submit_button(label="Add-Local+Global")
        gd = col3.form_submit_button(label="Add-Global_Only")
        remove = col4.form_submit_button(label="Remove")
    if search:
        sku_search(conn, table_name2, sku_value, table_name1)
    elif add:
        sku_value = normalize_str(sku_value)
        if sku_value == "":
            st.error("Invalid SKU! Enter a valid SKU")
        else:
            try:
                sku_value = validate_input(sku_value)
                if table_name1 == "nykaa_sku":
                    r = add_sku(conn, "b&c_global", sku_value, type2, username)
                elif table_name1 == "apnaklub_sku" or table_name1 == "otipy_sku":
                    r = add_sku(conn, "grocery_global", sku_value, type2, username)
                elif table_name1 == "medibikri_sku":
                    r = add_sku(conn, "pharmacy_global", sku_value, type2, username)
                r = add_sku(conn, table_name1, sku_value, type2, username)
                if r != 0:
                    add_sku_unique(conn, table_name2, sku_value)
                    show_sku_table_today(conn, table_name1, username)
            except ValueError as e:
                st.error(str(e))
    elif gd:
        sku_value = normalize_str(sku_value)
        try:
            sku_value = validate_input(sku_value)
            if table_name1 == "nykaa_sku":
                r = add_sku(conn, "b&c_global", sku_value, type2, username)
            elif table_name1 == "apnaklub_sku" or table_name1 == "otipy_sku":
                r = add_sku(conn, "grocery_global", sku_value, type2, username)
            elif table_name1 == "medibikri_sku":
                r = add_sku(conn, "pharmacy_global", sku_value, type2, username)
        except ValueError as e:
            st.error(str(e))
    elif remove:
        r = remove_sku_unique(conn, table_name2, sku_value)
        if r == 1:
            remove_sku(conn, table_name1, sku_value, type2)


def skufix_stock(username, table_name):
    conn = establish_connection()
    if conn is None:
        return
    with st.form(key="stock_form", clear_on_submit=True):
        security_name = st.text_input(
            "Enter the security_name", value="", key="security_name_value_input"
        )
        bse_code = st.text_input(
            "Enter the BSE code", value="", key="bse_code_value_input"
        )
        nse_code = st.text_input(
            "Enter the NSE code", value="", key="nse_code_value_input"
        )
        isin = st.text_input("Enter the ISISN", value="", key="isin_value_input")
        customer_id = st.text_input(
            "Enter the customer_id", value="", key="customer_id_value_input"
        )
        market_cap = st.text_input(
            "Enter the market cap", value="", key="market_cap_value_input"
        )
        security_name = security_name.lower()
        security_name = normalize_str(security_name)
        col1, col2, col3 = st.columns(3)
        search = col1.form_submit_button(label="Search")
        add = col2.form_submit_button(label="Add")
        remove = col3.form_submit_button(label="Remove")
    if search:
        stock_sku_search(conn, table_name, security_name)
    elif add:
        sku_value = normalize_str(security_name)
        if sku_value == "":
            st.error("Invalid SKU! Enter a valid SKU")
        else:
            try:
                security_name = validate_input(security_name)
                r = add_sku_stock(
                    conn,
                    table_name,
                    security_name,
                    bse_code,
                    nse_code,
                    isin,
                    customer_id,
                    market_cap,
                    username,
                )
                show_stock_sku_table_today(conn, table_name, username)
            except ValueError as e:
                st.error(str(e))
    elif remove:
        remove_stock_sku(conn, table_name, security_name)


def busskufix(username, table_name1, table_name2):
    conn = establish_connection()
    if conn is None:
        return
    with st.form(key="sku_form", clear_on_submit=True):
        terminal_value = st.text_input(
            "Enter the terminal name", value="", key="terminal_value_input"
        )
        terminal_value = terminal_value.lower()
        terminal_value = normalize_str(terminal_value)
        city_value = st.text_input(
            "Enter the city name", value="", key="city_value_input"
        )
        city_value = city_value.lower()
        city_value = normalize_str(city_value)
        province_value = st.text_input(
            "Enter the province name", value="", key="province_value_input"
        )
        province_value = province_value.lower()
        province_value = normalize_str(province_value)
        country_value = st.text_input(
            "Enter the country name", value="", key="country_value_input"
        )
        country_value = country_value.lower()
        country_value = normalize_str(country_value)
        col1, col2, col3, col4 = st.columns(4)
        search = col1.form_submit_button(label="Search")
        add = col2.form_submit_button(label="Add-Local+Global")
        gd = col3.form_submit_button(label="Add-Global_Only")
        remove = col4.form_submit_button(label="Remove")
    if search:
        bussku_search(
            conn, table_name1, terminal_value, city_value, province_value, country_value
        )
    elif add:
        if (
            terminal_value == ""
            and city_value == ""
            and province_value == ""
            and country_value == ""
        ):
            st.error("Invalid datails! Enter a valid values")
        else:
            try:
                terminal_value = validate_input(terminal_value)
                city_value = validate_input(city_value)
                province_value = validate_input(province_value)
                country_value = validate_input(country_value)
                add_bussku(
                    conn,
                    table_name1,
                    terminal_value,
                    city_value,
                    province_value,
                    country_value,
                    username,
                )
                add_bussku(
                    conn,
                    "bus_global",
                    terminal_value,
                    city_value,
                    province_value,
                    country_value,
                    username,
                )
                if terminal_value != "":
                    add_sku_unique(conn, table_name2, terminal_value)
                if city_value != "":
                    add_sku_unique(conn, table_name2, city_value)
                if province_value != "":
                    add_sku_unique(conn, table_name2, province_value)
                if country_value != "":
                    add_sku_unique(conn, table_name2, country_value)
            except ValueError as e:
                st.error(str(e))
    elif gd:
        try:
            terminal_value = validate_input(terminal_value)
            city_value = validate_input(city_value)
            province_value = validate_input(province_value)
            country_value = validate_input(country_value)
            add_bussku(
                conn,
                "bus_global",
                terminal_value,
                city_value,
                province_value,
                country_value,
                username,
            )
        except ValueError as e:
            st.error(str(e))
    elif remove:
        if terminal_value != "":
            r = remove_sku_unique(conn, table_name2, terminal_value)
            remove_global_bussku(
                conn,
                table_name1,
                terminal_value,
                city_value,
                province_value,
                country_value,
            )


def global_sku_fix(conn, username, table_name1):
    with st.form(key="global_form", clear_on_submit=True):
        sku_value = st.text_input("Enter the sku word", value="", key="sku_value_input")
        sku_value = sku_value.lower()
        sku_value = normalize_str(sku_value)
        option_name = ["variant", "product_type", "brand"]
        type2 = st.radio(
            "Choose the Type (Optional for search)", option_name, key="radio_options"
        )
        col1, col2, col3 = st.columns(3)
        search = col1.form_submit_button(label="Search")
        add = col2.form_submit_button(label="Add")
        remove = col3.form_submit_button(label="Remove")
    if search:
        global_search(conn, table_name1, sku_value)
    elif add:
        if sku_value == "":
            st.error("Invalid SKU! Enter a valid SKU")
        else:
            try:
                sku_value = validate_input(sku_value)
                r = add_sku(conn, table_name1, sku_value, type2, username)
                show_sku_table_today(conn, table_name1, username)
            except ValueError as e:
                st.error(str(e))
    elif remove:
        remove_global_sku(conn, table_name1, sku_value, type2)


def global_bussku_fix(conn, username, table_name1):
    with st.form(key="global_bus_form", clear_on_submit=True):
        terminal_value = st.text_input(
            "Enter the terminal name", value="", key="terminal_value_input"
        )
        terminal_value = terminal_value.lower()
        terminal_value = normalize_str(terminal_value)
        city_value = st.text_input(
            "Enter the city name", value="", key="city_value_input"
        )
        city_value = city_value.lower()
        city_value = normalize_str(city_value)
        province_value = st.text_input(
            "Enter the province name", value="", key="province_value_input"
        )
        province_value = province_value.lower()
        province_value = normalize_str(province_value)
        country_value = st.text_input(
            "Enter the country name", value="", key="country_value_input"
        )
        country_value = country_value.lower()
        country_value = normalize_str(country_value)
        col1, col2, col3 = st.columns(3)
        search = col1.form_submit_button(label="Search")
        add = col2.form_submit_button(label="Add")
        remove = col3.form_submit_button(label="Remove")
    if search:
        bussku_search(
            conn, table_name1, terminal_value, city_value, province_value, country_value
        )
    elif add:
        if (
            terminal_value == ""
            and city_value == ""
            and province_value == ""
            and country_value == ""
        ):
            st.error(
                "Invalid values! Atleast one of the input textbox must have a value"
            )
        else:
            try:
                terminal_value = validate_input(terminal_value)
                city_value = validate_input(city_value)
                province_value = validate_input(province_value)
                country_value = validate_input(country_value)
                r = add_bussku(
                    conn,
                    table_name1,
                    terminal_value,
                    city_value,
                    province_value,
                    country_value,
                    username,
                )
                show_bussku_table_today(conn, table_name1, username)
            except ValueError as e:
                st.error(str(e))
    elif remove:
        remove_global_bussku(
            conn, table_name1, terminal_value, city_value, province_value, country_value
        )


def global_syn_fix(conn, username, table_name1, table_name2):
    with st.form(key="global_syn_form", clear_on_submit=True):
        key = st.text_input("Global Key", value="", key="gkey_input")
        key = key.lower()
        key = normalize_str(key)
        synonym = st.text_input("Global Synonym", value="", key="gsynonym_input")
        synonym = synonym.lower()
        synonym = normalize_str(synonym)
        if table_name1 == "bus_global_syn":
            option_name = [
                "terminal_name",
                "city_name",
                "province_name",
                "country_name",
            ]
        else:
            option_name = ["brand", "product_type", "variant"]
        type1 = st.radio(
            "Choose the Type (Optional for search and remove)",
            option_name,
            key="radio_options",
        )
        col1, col2, col3 = st.columns(3)
        search = col1.form_submit_button(label="Search")
        add = col2.form_submit_button(label="Add")
        remove = col3.form_submit_button(label="Remove")
    if search:
        synonym_search(conn, table_name1, key, synonym)
    elif add:
        if synonym != "":
            try:
                key = validate_input(key)
                synonym = validate_input(synonym)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                insert_global_synonym_table(
                    conn,
                    key,
                    synonym,
                    type1,
                    username,
                    timestamp,
                    table_name1,
                    table_name2,
                )
                show_syn_table_today(conn, table_name1, username)
            except ValueError as e:
                st.error(str(e))
        else:
            st.error("synonyms must have a value to be added! ")
    elif remove:
        if synonym != "" or key != "":
            remove_synonym(conn, table_name1, key, synonym)
        else:
            st.error("Key and synonyms must have valid values to delete! ")


def global_lang_fix(conn, username, table_name, table_name1):
    with st.form(key="global_lang_form", clear_on_submit=True):
        key = st.text_input("Key", value="", key="key_input")
        key = key.lower()
        key = normalize_str(key)
        synonym = st.text_input("Lang synonym", value="", key="synonym_input")
        lang1 = st.radio("Choose the language", ["hi-IN", "en-IN", "ka-IN"])
        if table_name == "bus_global_lang":
            option_name = [
                "terminal_name",
                "city_name",
                "province_name",
                "country_name",
            ]
        else:
            option_name = ["brand", "product_type", "variant"]
        type1 = st.radio(
            "Choose the Type (Optional for search and remove)",
            option_name,
            key="radio_options",
        )
        col1, col2, col3 = st.columns(3)
        search = col1.form_submit_button(label="Search")
        add = col2.form_submit_button(label="Add")
        remove = col3.form_submit_button(label="Remove")
    if search:
        lang_search(conn, table_name, key, synonym)
    elif add:
        try:
            key = validate_input(key)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            insert_global_lang_table(
                conn,
                key,
                synonym,
                lang1,
                type1,
                username,
                timestamp,
                table_name,
                table_name1,
            )
            show_lang_table_today(conn, table_name, username)
        except ValueError as e:
            st.error(str(e))
    elif remove:
        if synonym != "" or key != "":
            remove_lang(conn, table_name, key, synonym)
        else:
            st.error("Key and synonyms must have valid values to delete! ")


def synonym_search(conn, table_name, key, synonym):
    with conn.cursor() as c:
        c.execute(
            'SELECT * FROM public."' + table_name + '" WHERE keywords=%s or synonym=%s',
            (key, synonym),
        )
        result = c.fetchall()
        if result:
            df = pd.DataFrame(
                result, columns=["keywords", "synonym", "type", "username", "timestamp"]
            )
            container_height = min(len(df) * 50, 500)
            with st.container():
                st.dataframe(df, height=container_height)
        else:
            st.error("Data not found")


def remove_synonym(conn, table_name, key, synonym):
    with conn.cursor() as c:
        c.execute(
            'SELECT COUNT(*) FROM public."'
            + table_name
            + '" WHERE keywords=%s and synonym=%s',
            (key, synonym),
        )
        result = c.fetchall()
        if result[0][0] > 0:
            c.execute(
                'DELETE FROM public."'
                + table_name
                + '" WHERE keywords=%s and synonym=%s',
                (key, synonym),
            )
            conn.commit()
            st.success("Deletion successful")
        else:
            st.error("Synonym not found")


def remove_lang(conn, table_name, key, synonym):
    with conn.cursor() as c:
        c.execute(
            'SELECT COUNT(*) FROM public."'
            + table_name
            + '" WHERE keywords=%s and translation=%s',
            (key, synonym),
        )
        result = c.fetchall()
        if result[0][0] > 0:
            if synonym == "":
                c.execute(
                    'DELETE FROM public."'
                    + table_name
                    + '" WHERE keywords=%s and translation is NULL',
                    (key,),
                )
                conn.commit()
                st.success("Deletion successful")
            else:
                c.execute(
                    'DELETE FROM public."'
                    + table_name
                    + '" WHERE keywords=%s and translation=%s',
                    (key, synonym),
                )
                conn.commit()
                st.success("Deletion successful")
        else:
            st.error("Synonym not found")


def Synonymfix(username, table_name1, table_name2):
    conn = establish_connection()
    if conn is None:
        return
    with st.form(key="syn_form", clear_on_submit=True):
        key = st.text_input("Key", value="", key="key_input")
        key = key.lower()
        key = normalize_str(key)
        synonym = st.text_input("Synonym", value="", key="synonym_input")
        option_name = ["brand", "product_type", "variant"]
        type1 = st.radio(
            "Choose the Type (Optional for search and remove)",
            option_name,
            key="radio_options",
        )
        col1, col2, col3, col4 = st.columns(4)
        search = col1.form_submit_button(label="Search")
        addtype = col2.radio(
            "Choose the add option", ["Local-only", "Global-only", "Both"]
        )
        add = col3.form_submit_button(label="Add")
        remove = col4.form_submit_button(label="Remove")
    if search:
        synonym_search(conn, table_name1, key, synonym)
    elif add:
        if synonym != "":
            try:
                key = validate_input(key)
                if addtype == "Local-only":
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    insert_synonym_table(
                        conn,
                        key,
                        synonym,
                        type1,
                        username,
                        timestamp,
                        table_name1,
                        table_name2,
                    )
                    show_syn_table_today(conn, table_name1, username)
                elif addtype == "Global-only":
                    if table_name1 == "nykaa_synonyms":
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        insert_global_synonym_table(
                            conn,
                            key,
                            synonym,
                            type1,
                            username,
                            timestamp,
                            "b&c_global_syn",
                            "b&c_global",
                        )
                        show_syn_table_today(conn, "b&c_global_syn", username)
                    elif (
                        table_name1 == "apnaklub_synonyms"
                        or table_name1 == "otipy_synonyms"
                    ):
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        insert_global_synonym_table(
                            conn,
                            key,
                            synonym,
                            type1,
                            username,
                            timestamp,
                            "grocery_global_syn",
                            "grocery_global",
                        )
                        show_syn_table_today(conn, "grocery_global_syn", username)
                    elif table_name1 == "medibikri_synonyms":
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        insert_global_synonym_table(
                            conn,
                            key,
                            synonym,
                            type1,
                            username,
                            timestamp,
                            "pharmacy_global_syn",
                            "pharmacy_global",
                        )
                        show_syn_table_today(conn, "pharmacy_global_syn", username)
                    else:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        insert_synonym_table(
                            conn, key, synonym, type1, username, timestamp, table_name1
                        )
                        show_syn_table_today(conn, table_name1, username)
                elif addtype == "Both":
                    if table_name1 == "nykaa_synonyms":
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        insert_synonym_table(
                            conn,
                            key,
                            synonym,
                            type1,
                            username,
                            timestamp,
                            table_name1,
                            table_name2,
                        )
                        insert_global_synonym_table(
                            conn,
                            key,
                            synonym,
                            type1,
                            username,
                            timestamp,
                            "b&c_global_syn",
                            "b&c_global",
                        )
                        show_syn_table_today(conn, table_name1, username)
                    elif (table_name1 == "apnaklub_synonyms") or (
                        table_name1 == "otipy_synonyms"
                    ):
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        insert_synonym_table(
                            conn,
                            key,
                            synonym,
                            type1,
                            username,
                            timestamp,
                            table_name1,
                            table_name2,
                        )
                        insert_global_synonym_table(
                            conn,
                            key,
                            synonym,
                            type1,
                            username,
                            timestamp,
                            "grocery_global_syn",
                            "grocery_global",
                        )
                        show_syn_table_today(conn, table_name1, username)
                    elif table_name1 == "medibikri_synonyms":
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        insert_synonym_table(
                            conn,
                            key,
                            synonym,
                            type1,
                            username,
                            timestamp,
                            table_name1,
                            table_name2,
                        )
                        insert_global_synonym_table(
                            conn,
                            key,
                            synonym,
                            type1,
                            username,
                            timestamp,
                            "pharmacy_global_syn",
                            "pharmacy_global",
                        )
                        show_syn_table_today(conn, table_name1, username)
                    else:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        insert_synonym_table(
                            conn, key, synonym, type1, username, timestamp, table_name1
                        )
                        show_syn_table_today(conn, table_name1, username)
            except ValueError as e:
                st.error(str(e))
        else:
            st.error("synonyms must have a value to be added! ")
    elif remove:
        if synonym != "" or key != "":
            remove_synonym(conn, table_name1, key, synonym)
        else:
            st.error("Key and synonyms must have valid values to delete! ")


def Synonymfix1(username, table_name1):
    conn = establish_connection()
    if conn is None:
        return
    with st.form(key="syn_form", clear_on_submit=True):
        key = st.text_input("Key", value="", key="key_input")
        key = key.lower()
        key = normalize_str(key)
        synonym = st.text_input("Synonym", value="", key="synonym_input")
        type1 = st.text_input("Type", value="", key="Type_input")
        col1, col2, col3 = st.columns(3)
        search = col1.form_submit_button(label="Search")
        add = col2.form_submit_button(label="Add")
        remove = col3.form_submit_button(label="Remove")
    if search:
        synonym_search(conn, table_name1, key, synonym)
    elif add:
        if synonym != "":
            try:
                key = validate_input(key)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                insert_synonym_table(
                    conn, key, synonym, type1, username, timestamp, table_name1
                )
                show_syn_table_today(conn, table_name1, username)
            except ValueError as e:
                st.error(str(e))
        else:
            st.error("synonyms must have a value to be added! ")
    elif remove:
        if synonym != "" or key != "":
            remove_synonym(conn, table_name1, key, synonym)
        else:
            st.error("Key and synonyms must have valid values to delete! ")


def show_lang_table_today(conn, table_name, username):
    with conn.cursor() as c:
        c.execute(
            'CREATE OR REPLACE VIEW my_syn_view_date AS SELECT "keywords", "translation", "language", "type", "username", "timestamp" FROM public."'
            + table_name
            + '" WHERE username=%s AND CAST(timestamp AS DATE) = %s ORDER BY "timestamp" DESC',
            (username, date.today()),
        )
        c.execute("SELECT * FROM my_syn_view_date")
        result = c.fetchall()
        df = pd.DataFrame(
            result,
            columns=[
                "keywords",
                "translation",
                "language",
                "type",
                "username",
                "timestamp",
            ],
        )
        mf = df
        mf.fillna("", inplace=True)
        container_height = min(len(mf) * 50, 300)
        with st.container():
            st.dataframe(df, height=container_height)


def insert_lang(conn, table_name, key, synonym, lang1, type1, username, timestamp):
    with conn.cursor() as c:
        c.execute(
            'INSERT INTO public."'
            + table_name
            + '" (keywords, translation, language, type, username, timestamp) VALUES (%s, %s, %s, %s, %s, %s)',
            (key, synonym, lang1, type1, username, timestamp),
        )
        conn.commit()


def insert_lang_table(
    conn, key, synonym, lang1, type1, username, timestamp, table_name1, table_name2
):
    if not check_key_exists(conn, table_name2, key):
        st.warning(
            "Invalid key value in " + table_name2 + ", Please enter a valid key."
        )
        return
    col_name = "translation"
    value = synonym
    if value != "":
        if not check_no_duplicate(conn, table_name1, col_name, value):
            st.warning(
                "Language hint already exists in "
                + table_name1
                + ", Please enter a valid Language hint."
            )
            return
    try:
        insert_lang(conn, table_name1, key, synonym, lang1, type1, username, timestamp)
        st.success("Language hints added successfully in " + table_name1)
    except IntegrityError as e:
        st.write(f"Error: {e}")


def insert_lang_table(
    conn, key, synonym, lang1, type1, username, timestamp, table_name1
):
    col_name = "translation"
    value = synonym
    if value != "":
        if not check_no_duplicate(conn, table_name1, col_name, value):
            st.warning(
                "Language hint already exists in "
                + table_name1
                + ", Please enter a valid Language hint."
            )
            return
    try:
        insert_lang(conn, table_name1, key, synonym, lang1, type1, username, timestamp)
        st.success("Language hints added successfully in " + table_name1)
    except IntegrityError as e:
        st.write(f"Error: {e}")


def lang_search(conn, table_name, key, synonym):
    with conn.cursor() as c:
        if synonym:
            c.execute(
                'SELECT * FROM public."'
                + table_name
                + '" WHERE keywords=%s or translation=%s',
                (key, synonym),
            )
            result = c.fetchall()
        else:
            c.execute(
                'SELECT * FROM public."' + table_name + '" WHERE keywords=%s', (key,)
            )
            result = c.fetchall()
        if result:
            df = pd.DataFrame(
                result,
                columns=[
                    "keywords",
                    "translation",
                    "language",
                    "type",
                    "username",
                    "timestamp",
                ],
            )
            mf = df
            mf.fillna("", inplace=True)
            container_height = min(len(mf) * 50, 500)
            with st.container():
                st.dataframe(mf, height=container_height)
        else:
            st.error("Data not found")


def langfix(username, table_name1, table_name2):
    conn = establish_connection()
    if conn is None:
        return
    with st.form(key="lang_form", clear_on_submit=True):
        key = st.text_input("Key", value="", key="key_input")
        key = key.lower()
        key = normalize_str(key)
        synonym = st.text_input("Lang synonym", value="", key="synonym_input")
        lang1 = st.radio("Choose the language", ["hi-IN", "en-IN", "ka-IN"])
        if table_name1 == "rb_lang":
            option_name = [
                "terminal_name",
                "city_name",
                "province_name",
                "country_name",
            ]
        else:
            option_name = ["brand", "product_type", "variant"]
        type1 = st.radio(
            "Choose the Type (Optional for search and remove)",
            option_name,
            key="radio_options",
        )
        col1, col2, col3, col4 = st.columns(4)
        search = col1.form_submit_button(label="Search")
        addtype = col2.radio(
            "Choose the add option", ["Local-only", "Global-only", "Both"]
        )
        add = col3.form_submit_button(label="Add")
        remove = col4.form_submit_button(label="Remove")
    if search:
        lang_search(conn, table_name1, key, synonym)
    elif add:
        if key != "":
            try:
                key = validate_input(key)
                if addtype == "Local-only":
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    insert_lang_table(
                        conn,
                        key,
                        synonym,
                        lang1,
                        type1,
                        username,
                        timestamp,
                        table_name1,
                        table_name2,
                    )
                    show_lang_table_today(conn, table_name1, username)
                elif addtype == "Global-only":
                    if table_name1 == "nykaa_lang":
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        insert_global_lang_table(
                            conn,
                            key,
                            synonym,
                            lang1,
                            type1,
                            username,
                            timestamp,
                            "b&c_global_lang",
                            "b&c_global",
                        )
                        show_lang_table_today(conn, "b&c_global_lang", username)
                    elif table_name1 == "apnaklub_lang" or table_name1 == "otipy_lang":
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        insert_global_lang_table(
                            conn,
                            key,
                            synonym,
                            lang1,
                            type1,
                            username,
                            timestamp,
                            "grocery_global_lang",
                            "grocery_global",
                        )
                        show_lang_table_today(conn, "grocery_global_lang", username)
                    elif table_name1 == "medibikri_lang":
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        insert_global_lang_table(
                            conn,
                            key,
                            synonym,
                            lang1,
                            type1,
                            username,
                            timestamp,
                            "pharmacy_global_lang",
                            "pharmacy_global",
                        )
                        show_lang_table_today(conn, "bus_global_lang", username)
                    else:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        insert_lang_table(
                            conn,
                            key,
                            synonym,
                            lang1,
                            type1,
                            username,
                            timestamp,
                            table_name1,
                        )
                        show_lang_table_today(conn, table_name1, username)
                elif addtype == "Both":
                    st.write("inside both")
                    if table_name1 == "nykaa_lang":
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        insert_lang_table(
                            conn,
                            key,
                            synonym,
                            lang1,
                            type1,
                            username,
                            timestamp,
                            table_name1,
                            table_name2,
                        )
                        insert_global_lang_table(
                            conn,
                            key,
                            synonym,
                            lang1,
                            type1,
                            username,
                            timestamp,
                            "b&c_global_lang",
                            "b&c_global",
                        )
                        show_lang_table_today(conn, table_name1, username)
                    elif (table_name1 == "apnaklub_lang") or (
                        table_name1 == "otipy_lang"
                    ):
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        insert_lang_table(
                            conn,
                            key,
                            synonym,
                            lang1,
                            type1,
                            username,
                            timestamp,
                            table_name1,
                            table_name2,
                        )
                        insert_global_lang_table(
                            conn,
                            key,
                            synonym,
                            lang1,
                            type1,
                            username,
                            timestamp,
                            "grocery_global_lang",
                            "grocery_global",
                        )
                        show_lang_table_today(conn, table_name1, username)
                    elif table_name1 == "medibikri_lang":
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        insert_lang_table(
                            conn,
                            key,
                            synonym,
                            lang1,
                            type1,
                            username,
                            timestamp,
                            table_name1,
                            table_name2,
                        )
                        insert_global_lang_table(
                            conn,
                            key,
                            synonym,
                            lang1,
                            type1,
                            username,
                            timestamp,
                            "pharmacy_global_lang",
                            "pharmacy_global",
                        )
                        show_lang_table_today(conn, table_name1, username)
                    else:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        insert_lang_table(
                            conn,
                            key,
                            synonym,
                            lang1,
                            type1,
                            username,
                            timestamp,
                            table_name1,
                        )
                        show_lang_table_today(conn, table_name1, username)
            except ValueError as e:
                st.error(str(e))
    elif remove:
        if synonym != "" or key != "":
            remove_lang(conn, table_name1, key, synonym)
        else:
            st.error("Key and synonyms must have valid values to delete! ")


def langfix1(username, table_name1):
    conn = establish_connection()
    if conn is None:
        return
    with st.form(key="lang_form", clear_on_submit=True):
        key = st.text_input("Key", value="", key="key_input")
        key = key.lower()
        key = normalize_str(key)
        synonym = st.text_input("Lang synonym", value="", key="synonym_input")
        lang1 = st.radio("Choose the language", ["hi-IN", "en-IN", "ka-IN"])
        type1 = st.text_input("Type", value="", key="type_input")
        col1, col2, col3 = st.columns(3)
        search = col1.form_submit_button(label="Search")
        add = col2.form_submit_button(label="Add")
        remove = col3.form_submit_button(label="Remove")
    if search:
        lang_search(conn, table_name1, key, synonym)
    elif add:
        if key != "":
            try:
                key = validate_input(key)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                insert_lang_table(
                    conn, key, synonym, lang1, type1, username, timestamp, table_name1
                )
                show_lang_table_today(conn, table_name1, username)
            except ValueError as e:
                st.error(str(e))
    elif remove:
        if synonym != "" or key != "":
            remove_lang(conn, table_name1, key, synonym)
        else:
            st.error("Key and synonyms must have valid values to delete! ")


def dashboard_page(username):
    conn = establish_connection()
    if conn is None:
        return
    choice = st.sidebar.selectbox(
        "Choose a customer",
        (
            "Nykaa",
            "Otipy",
            "ApnaKlub",
            "medibikri",
            "ICICIDirect_stock",
            "ICICIDirect_trading",
        ),
    )

    if choice == "Nykaa":
        sub_option = st.sidebar.selectbox(
            "Select a table", ["Synonyms", "SKU", "Language"]
        )
        if sub_option == "Synonyms":
            table_name = "nykaa_synonyms"
            cols1, cols2 = st.columns([2, 2])
            ch = cols1.radio("Choose an operation", ["Edit table", "Show table"])
            if ch == "Edit table":
                st.subheader("Nykaa Synonyms Data")
                Synonymfix(username, "nykaa_synonyms", "NykaaUniqueWords")
            elif ch == "Show table":
                ch1 = cols2.selectbox(
                    "Select an option",
                    [
                        "",
                        "Version History - Username",
                        "Version History - Date",
                        "Show Full Table",
                    ],
                )
                if ch1 == "Version History - Username":
                    show_syn_table_username(conn, table_name)
                elif ch1 == "Version History - Date":
                    show_syn_table_date(conn, table_name)
                elif ch1 == "Show Full Table":
                    show_synonym_table(conn, table_name)

        elif sub_option == "SKU":
            table_name = "nykaa_sku"
            cols1, cols2 = st.columns([2, 2])
            ch = cols1.radio("Choose an operation", ["Edit table", "Show table"])
            if ch == "Edit table":
                st.subheader("Nykaa SKU Data")
                skufix(username, "nykaa_sku", "NykaaUniqueWords")
            elif ch == "Show table":
                ch1 = cols2.selectbox(
                    "Select an option",
                    [
                        "",
                        "Version History - Username",
                        "Version History - Date",
                        "Show Full Table",
                    ],
                )
                if ch1 == "Version History - Username":
                    show_sku_table_username(conn, table_name)
                elif ch1 == "Version History - Date":
                    show_sku_table_date(conn, table_name)
                elif ch1 == "Show Full Table":
                    show_sku_table(conn, table_name)

        elif sub_option == "Language":
            table_name = "nykaa_lang"
            cols1, cols2 = st.columns([2, 2])
            ch = cols1.radio("Choose an operation", ["Edit table", "Show table"])
            if ch == "Edit table":
                st.subheader("Nykaa Language Data")
                langfix(username, "nykaa_lang", "NykaaUniqueWords")
            elif ch == "Show table":
                ch1 = cols2.selectbox(
                    "Select an option",
                    [
                        "",
                        "Version History - Username",
                        "Version History - Date",
                        "Show Full Table",
                    ],
                )
                if ch1 == "Version History - Username":
                    show_lang_table_username(conn, table_name)
                elif ch1 == "Version History - Date":
                    show_lang_table_date(conn, table_name)
                elif ch1 == "Show Full Table":
                    show_lang_table(conn, table_name)

    elif choice == "Otipy":
        sub_option = st.sidebar.selectbox(
            "Select a table", ["Synonyms", "SKU", "Language"]
        )
        if sub_option == "Synonyms":
            table_name = "otipy_synonyms"
            cols1, cols2 = st.columns([2, 2])
            ch = cols1.radio("Choose an operation", ["Edit table", "Show table"])
            if ch == "Edit table":
                st.subheader("otipy Synonyms Data")
                Synonymfix(username, "otipy_synonyms", "OtipyUniqueWords")
            elif ch == "Show table":
                ch1 = cols2.selectbox(
                    "Select an option",
                    [
                        "",
                        "Version History - Username",
                        "Version History - Date",
                        "Show Full Table",
                    ],
                )
                if ch1 == "Version History - Username":
                    show_syn_table_username(conn, table_name)
                elif ch1 == "Version History - Date":
                    show_syn_table_date(conn, table_name)
                elif ch1 == "Show Full Table":
                    show_synonym_table(conn, table_name)

        elif sub_option == "SKU":
            table_name = "otipy_sku"
            cols1, cols2 = st.columns([2, 2])
            ch = cols1.radio("Choose an operation", ["Edit table", "Show table"])
            if ch == "Edit table":
                st.subheader("Otipy SKU Data")
                skufix(username, "otipy_sku", "OtipyUniqueWords")
            elif ch == "Show table":
                ch1 = cols2.selectbox(
                    "Select an option",
                    [
                        "",
                        "Version History - Username",
                        "Version History - Date",
                        "Show Full Table",
                    ],
                )
                if ch1 == "Version History - Username":
                    show_sku_table_username(conn, table_name)
                elif ch1 == "Version History - Date":
                    show_sku_table_date(conn, table_name)
                elif ch1 == "Show Full Table":
                    show_sku_table(conn, table_name)

        elif sub_option == "Language":
            table_name = "otipy_lang"
            cols1, cols2 = st.columns([2, 2])
            ch = cols1.radio("Choose an operation", ["Edit table", "Show table"])
            if ch == "Edit table":
                st.subheader("Otipy Language Data")
                langfix(username, "apnaklub_lang", "OtipyUniqueWords")
            elif ch == "Show table":
                ch1 = cols2.selectbox(
                    "Select an option",
                    [
                        "",
                        "Version History - Username",
                        "Version History - Date",
                        "Show Full Table",
                    ],
                )
                if ch1 == "Version History - Username":
                    show_lang_table_username(conn, table_name)
                elif ch1 == "Version History - Date":
                    show_lang_table_date(conn, table_name)
                elif ch1 == "Show Full Table":
                    show_lang_table(conn, table_name)

    elif choice == "ApnaKlub":
        sub_option = st.sidebar.selectbox(
            "Select a table", ["Synonyms", "SKU", "Language"]
        )
        if sub_option == "Synonyms":
            table_name = "apnaklub_synonyms"
            cols1, cols2 = st.columns([2, 2])
            ch = cols1.radio("Choose an operation", ["Edit table", "Show table"])
            if ch == "Edit table":
                st.subheader("Apnaklub Synonyms Data")
                Synonymfix(username, "apnaklub_synonyms", "ApnaklubUniqueWords")
            elif ch == "Show table":
                ch1 = cols2.selectbox(
                    "Select an option",
                    [
                        "",
                        "Version History - Username",
                        "Version History - Date",
                        "Show Full Table",
                    ],
                )
                if ch1 == "Version History - Username":
                    show_syn_table_username(conn, table_name)
                elif ch1 == "Version History - Date":
                    show_syn_table_date(conn, table_name)
                elif ch1 == "Show Full Table":
                    show_synonym_table(conn, table_name)

        elif sub_option == "SKU":
            table_name = "apnaklub_sku"
            cols1, cols2 = st.columns([2, 2])
            ch = cols1.radio("Choose an operation", ["Edit table", "Show table"])
            if ch == "Edit table":
                st.subheader("Apnaklub SKU Data")
                skufix(username, "apnaklub_sku", "ApnaklubUniqueWords")
            elif ch == "Show table":
                ch1 = cols2.selectbox(
                    "Select an option",
                    [
                        "",
                        "Version History - Username",
                        "Version History - Date",
                        "Show Full Table",
                    ],
                )
                if ch1 == "Version History - Username":
                    show_sku_table_username(conn, table_name)
                elif ch1 == "Version History - Date":
                    show_sku_table_date(conn, table_name)
                elif ch1 == "Show Full Table":
                    show_sku_table(conn, table_name)

        elif sub_option == "Language":
            table_name = "apnaklub_lang"
            cols1, cols2 = st.columns([2, 2])
            ch = cols1.radio("Choose an operation", ["Edit table", "Show table"])
            if ch == "Edit table":
                st.subheader("Apnaklub Language Data")
                langfix(username, "apnaklub_lang", "ApnaklubUniqueWords")
            elif ch == "Show table":
                ch1 = cols2.selectbox(
                    "Select an option",
                    [
                        "",
                        "Version History - Username",
                        "Version History - Date",
                        "Show Full Table",
                    ],
                )
                if ch1 == "Version History - Username":
                    show_lang_table_username(conn, table_name)
                elif ch1 == "Version History - Date":
                    show_lang_table_date(conn, table_name)
                elif ch1 == "Show Full Table":
                    show_lang_table(conn, table_name)

    elif choice == "medibikri":
        sub_option = st.sidebar.selectbox(
            "Select a table", ["Synonyms", "SKU", "Language"]
        )
        if sub_option == "Synonyms":
            table_name = "medibikri_synonyms"
            cols1, cols2 = st.columns([2, 2])
            ch = cols1.radio("Choose an operation", ["Edit table", "Show table"])
            if ch == "Edit table":
                st.subheader("Medibikri Synonyms Data")
                Synonymfix(username, "medibikri_synonyms", "MedibikriUniqueWords")
            elif ch == "Show table":
                ch1 = cols2.selectbox(
                    "Select an option",
                    [
                        "",
                        "Version History - Username",
                        "Version History - Date",
                        "Show Full Table",
                    ],
                )
                if ch1 == "Version History - Username":
                    show_syn_table_username(conn, table_name)
                elif ch1 == "Version History - Date":
                    show_syn_table_date(conn, table_name)
                elif ch1 == "Show Full Table":
                    show_synonym_table(conn, table_name)

        elif sub_option == "SKU":
            table_name = "medibikri_sku"
            cols1, cols2 = st.columns([2, 2])
            ch = cols1.radio("Choose an operation", ["Edit table", "Show table"])
            if ch == "Edit table":
                st.subheader("Medibikri SKU Data")
                skufix(username, "medibikri_sku", "MedibikriUniqueWords")
            elif ch == "Show table":
                ch1 = cols2.selectbox(
                    "Select an option",
                    [
                        "",
                        "Version History - Username",
                        "Version History - Date",
                        "Show Full Table",
                    ],
                )
                if ch1 == "Version History - Username":
                    show_sku_table_username(conn, table_name)
                elif ch1 == "Version History - Date":
                    show_sku_table_date(conn, table_name)
                elif ch1 == "Show Full Table":
                    show_sku_table(conn, table_name)

        elif sub_option == "Language":
            table_name = "medibikri_lang"
            cols1, cols2 = st.columns([2, 2])
            ch = cols1.radio("Choose an operation", ["Edit table", "Show table"])
            if ch == "Edit table":
                st.subheader("Medibikri Language Data")
                langfix(username, "medibikri_lang", "MedibikriUniqueWords")
            elif ch == "Show table":
                ch1 = cols2.selectbox(
                    "Select an option",
                    [
                        "",
                        "Version History - Username",
                        "Version History - Date",
                        "Show Full Table",
                    ],
                )
                if ch1 == "Version History - Username":
                    show_lang_table_username(conn, table_name)
                elif ch1 == "Version History - Date":
                    show_lang_table_date(conn, table_name)
                elif ch1 == "Show Full Table":
                    show_lang_table(conn, table_name)

    if choice == "ICICIDirect_stock":
        sub_option = st.sidebar.selectbox(
            "Select a table", ["Synonyms", "SKU", "Language"]
        )
        if sub_option == "Synonyms":
            table_name = "icicistock_synonyms"
            cols1, cols2 = st.columns([2, 2])
            ch = cols1.radio("Choose an operation", ["Edit table", "Show table"])
            if ch == "Edit table":
                st.subheader("ICICIstock Synonyms Data")
                Synonymfix1(username, "icicistock_synonyms")
            elif ch == "Show table":
                ch1 = cols2.selectbox(
                    "Select an option",
                    [
                        "",
                        "Version History - Username",
                        "Version History - Date",
                        "Show Full Table",
                    ],
                )
                if ch1 == "Version History - Username":
                    show_syn_table_username(conn, table_name)
                elif ch1 == "Version History - Date":
                    show_syn_table_date(conn, table_name)
                elif ch1 == "Show Full Table":
                    show_synonym_table(conn, table_name)

        elif sub_option == "SKU":
            table_name = "icicistock_sku"
            cols1, cols2 = st.columns([2, 2])
            ch = cols1.radio("Choose an operation", ["Edit table", "Show table"])
            if ch == "Edit table":
                st.subheader("ICICI Stock SKU Data")
                skufix_stock(username, "icicistock_sku")
            elif ch == "Show table":
                ch1 = cols2.selectbox(
                    "Select an option",
                    [
                        "",
                        "Version History - Username",
                        "Version History - Date",
                        "Show Full Table",
                    ],
                )
                if ch1 == "Version History - Username":
                    show_stock_sku_table_username(conn, table_name)
                elif ch1 == "Version History - Date":
                    show_stock_sku_table_date(conn, table_name)
                elif ch1 == "Show Full Table":
                    show_stock_sku_table(conn, table_name)

        elif sub_option == "Language":
            table_name = "icicistock_lang"
            cols1, cols2 = st.columns([2, 2])
            ch = cols1.radio("Choose an operation", ["Edit table", "Show table"])
            if ch == "Edit table":
                st.subheader("ICICIstock Language Data")
                langfix1(username, "icicistock_lang")
            elif ch == "Show table":
                ch1 = cols2.selectbox(
                    "Select an option",
                    [
                        "",
                        "Version History - Username",
                        "Version History - Date",
                        "Show Full Table",
                    ],
                )
                if ch1 == "Version History - Username":
                    show_lang_table_username(conn, table_name)
                elif ch1 == "Version History - Date":
                    show_lang_table_date(conn, table_name)
                elif ch1 == "Show Full Table":
                    show_lang_table(conn, table_name)

    if choice == "ICICIDirect_trading":
        sub_option = st.sidebar.selectbox(
            "Select a table", ["Synonyms", "SKU", "Language"]
        )
        if sub_option == "Synonyms":
            table_name = "icicitrading_synonym"
            cols1, cols2 = st.columns([2, 2])
            ch = cols1.radio("Choose an operation", ["Edit table", "Show table"])
            if ch == "Edit table":
                st.subheader("ICICIDirect Synonyms Data")
                Synonymfix1(username, "icicidirect_synonyms")
            elif ch == "Show table":
                ch1 = cols2.selectbox(
                    "Select an option",
                    [
                        "",
                        "Version History - Username",
                        "Version History - Date",
                        "Show Full Table",
                    ],
                )
                if ch1 == "Version History - Username":
                    show_syn_table_username(conn, table_name)
                elif ch1 == "Version History - Date":
                    show_syn_table_date(conn, table_name)
                elif ch1 == "Show Full Table":
                    show_synonym_table(conn, table_name)

        elif sub_option == "SKU":
            cols1, cols2 = st.columns([2, 2])
            ch = cols1.radio("Choose an operation", ["Show table"])
            if ch == "Show table":
                ch1 = cols2.selectbox(
                    "Select an option",
                    ["", "ICICI Trading-Navigation", "ICICI Trading-Portfolio"],
                )
                if ch1 == "ICICI Trading-Navigation":
                    show_iciciNavigation_table(conn, "icicitrading_navigation")
                elif ch1 == "ICICI Trading-Portfolio":
                    show_iciciPortfolio_table(conn, "icicitrading_portfolio")

        elif sub_option == "Language":
            table_name = "icicitrading_language"
            cols1, cols2 = st.columns([2, 2])
            ch = cols1.radio("Choose an operation", ["Edit table", "Show table"])
            if ch == "Edit table":
                st.subheader("ICICIstock Language Data")
                langfix1(username, "icicitrading_language")
            elif ch == "Show table":
                ch1 = cols2.selectbox(
                    "Select an option",
                    [
                        "",
                        "Version History - Username",
                        "Version History - Date",
                        "Show Full Table",
                    ],
                )
                if ch1 == "Version History - Username":
                    show_lang_table_username(conn, table_name)
                elif ch1 == "Version History - Date":
                    show_lang_table_date(conn, table_name)
                elif ch1 == "Show Full Table":
                    show_lang_table(conn, table_name)

    if st.sidebar.button("Back"):
        st.session_state["page"] = "page1"
        st.experimental_rerun()


def choose_page(username):
    conn = establish_connection()
    if conn is None:
        return
    st.subheader(f"Welcome, {username}!")
    choice = st.sidebar.radio("Dashboard", ("Global Dataset", "Customer Dataset"))
    if choice == "Global Dataset":
        sub_option = st.sidebar.selectbox(
            "Global Dataset", ["B & C", "Grocery", "Pharmacy", "Fashion", "Bus"]
        )
        if sub_option == "B & C":
            sub_table = st.sidebar.selectbox(
                "Choose a table", ["SKU", "Synonym", "Language"]
            )
            if sub_table == "SKU":
                table_name = "b&c_global"
                cols1, cols2 = st.columns([2, 2])
                ch = cols1.radio("Choose an operation", ["Show table", "Edit table"])
                if ch == "Show table":
                    ch1 = cols2.selectbox(
                        "Select an option",
                        [
                            "",
                            "Version History - Username",
                            "Version History - Date",
                            "Show Full Table",
                        ],
                    )
                    if ch1 == "Version History - Username":
                        show_sku_table_username(conn, table_name)
                    elif ch1 == "Version History - Date":
                        show_sku_table_date(conn, table_name)
                    elif ch1 == "Show Full Table":
                        show_sku_table(conn, table_name)
                elif ch == "Edit table":
                    global_sku_fix(conn, username, "b&c_global")

            elif sub_table == "Synonym":
                table_name = "b&c_global_syn"
                cols1, cols2 = st.columns([2, 2])
                ch = cols1.radio("Choose an operation", ["Show table", "Edit table"])
                if ch == "Show table":
                    ch1 = cols2.selectbox(
                        "Select an option",
                        [
                            "",
                            "Version History - Username",
                            "Version History - Date",
                            "Show Full Table",
                        ],
                    )
                    if ch1 == "Version History - Username":
                        show_syn_table_username(conn, table_name)
                    elif ch1 == "Version History - Date":
                        show_syn_table_date(conn, table_name)
                    elif ch1 == "Show Full Table":
                        show_synonym_table(conn, table_name)
                elif ch == "Edit table":
                    global_syn_fix(conn, username, "b&c_global_syn", "b&c_global")

            elif sub_table == "Language":
                table_name = "b&c_global_lang"
                cols1, cols2 = st.columns([2, 2])
                ch = cols1.radio("Choose an operation", ["Show table", "Edit table"])
                if ch == "Show table":
                    ch1 = cols2.selectbox(
                        "Select an option",
                        [
                            "",
                            "Version History - Username",
                            "Version History - Date",
                            "Show Full Table",
                        ],
                    )
                    if ch1 == "Version History - Username":
                        show_lang_table_username(conn, table_name)
                    elif ch1 == "Version History - Date":
                        show_lang_table_date(conn, table_name)
                    elif ch1 == "Show Full Table":
                        show_lang_table(conn, table_name)
                elif ch == "Edit table":
                    global_lang_fix(conn, username, "b&c_global_lang", "b&c_global")

        if sub_option == "Grocery":
            sub_table = st.sidebar.selectbox(
                "Choose a table", ["SKU", "Synonym", "Language"]
            )
            if sub_table == "SKU":
                table_name = "grocery_global"
                cols1, cols2 = st.columns([2, 2])
                ch = cols1.radio("Choose an operation", ["Show table", "Edit table"])
                if ch == "Show table":
                    ch1 = cols2.selectbox(
                        "Select an option",
                        [
                            "",
                            "Version History - Username",
                            "Version History - Date",
                            "Show Full Table",
                        ],
                    )
                    if ch1 == "Version History - Username":
                        show_sku_table_username(conn, table_name)
                    elif ch1 == "Version History - Date":
                        show_sku_table_date(conn, table_name)
                    elif ch1 == "Show Full Table":
                        show_sku_table(conn, table_name)
                elif ch == "Edit table":
                    global_sku_fix(conn, username, "grocery_global")

            elif sub_table == "Synonym":
                table_name = "grocery_global_syn"
                cols1, cols2 = st.columns([2, 2])
                ch = cols1.radio("Choose an operation", ["Show table", "Edit table"])
                if ch == "Show table":
                    ch1 = cols2.selectbox(
                        "Select an option",
                        [
                            "",
                            "Version History - Username",
                            "Version History - Date",
                            "Show Full Table",
                        ],
                    )
                    if ch1 == "Version History - Username":
                        show_syn_table_username(conn, table_name)
                    elif ch1 == "Version History - Date":
                        show_syn_table_date(conn, table_name)
                    elif ch1 == "Show Full Table":
                        show_synonym_table(conn, table_name)
                elif ch == "Edit table":
                    global_syn_fix(
                        conn, username, "grocery_global_syn", "grocery_global"
                    )

            elif sub_table == "Language":
                table_name = "grocery_global_lang"
                cols1, cols2 = st.columns([2, 2])
                ch = cols1.radio("Choose an operation", ["Show table", "Edit table"])
                if ch == "Show table":
                    ch1 = cols2.selectbox(
                        "Select an option",
                        [
                            "",
                            "Version History - Username",
                            "Version History - Date",
                            "Show Full Table",
                        ],
                    )
                    if ch1 == "Version History - Username":
                        show_lang_table_username(conn, table_name)
                    elif ch1 == "Version History - Date":
                        show_lang_table_date(conn, table_name)
                    elif ch1 == "Show Full Table":
                        show_lang_table(conn, table_name)
                elif ch == "Edit table":
                    global_lang_fix(
                        conn, username, "grocery_global_lang", "grocery_global"
                    )

        if sub_option == "Pharmacy":
            sub_table = st.sidebar.selectbox(
                "Choose a table", ["SKU", "Synonym", "Language"]
            )
            if sub_table == "SKU":
                table_name = "pharmacy_global"
                cols1, cols2 = st.columns([2, 2])
                ch = cols1.radio("Choose an operation", ["Show table", "Edit table"])
                if ch == "Show table":
                    ch1 = cols2.selectbox(
                        "Select an option",
                        [
                            "",
                            "Version History - Username",
                            "Version History - Date",
                            "Show Full Table",
                        ],
                    )
                    if ch1 == "Version History - Username":
                        show_sku_table_username(conn, table_name)
                    elif ch1 == "Version History - Date":
                        show_sku_table_date(conn, table_name)
                    elif ch1 == "Show Full Table":
                        show_sku_table(conn, table_name)
                elif ch == "Edit table":
                    global_sku_fix(conn, username, "pharmacy_global")

            elif sub_table == "Synonym":
                table_name = "pharmacy_global_syn"
                cols1, cols2 = st.columns([2, 2])
                ch = cols1.radio("Choose an operation", ["Show table", "Edit table"])
                if ch == "Show table":
                    ch1 = cols2.selectbox(
                        "Select an option",
                        [
                            "",
                            "Version History - Username",
                            "Version History - Date",
                            "Show Full Table",
                        ],
                    )
                    if ch1 == "Version History - Username":
                        show_syn_table_username(conn, table_name)
                    elif ch1 == "Version History - Date":
                        show_syn_table_date(conn, table_name)
                    elif ch1 == "Show Full Table":
                        show_synonym_table(conn, table_name)
                elif ch == "Edit table":
                    global_syn_fix(
                        conn, username, "pharmacy_global_syn", "pharmacy_global"
                    )

            elif sub_table == "Language":
                table_name = "pharmacy_global_lang"
                cols1, cols2 = st.columns([2, 2])
                ch = cols1.radio("Choose an operation", ["Show table", "Edit table"])
                if ch == "Show table":
                    ch1 = cols2.selectbox(
                        "Select an option",
                        [
                            "",
                            "Version History - Username",
                            "Version History - Date",
                            "Show Full Table",
                        ],
                    )
                    if ch1 == "Version History - Username":
                        show_lang_table_username(conn, table_name)
                    elif ch1 == "Version History - Date":
                        show_lang_table_date(conn, table_name)
                    elif ch1 == "Show Full Table":
                        show_lang_table(conn, table_name)
                elif ch == "Edit table":
                    global_lang_fix(
                        conn, username, "pharmacy_global_lang", "pharmacy_global"
                    )

        if sub_option == "Fashion":
            sub_table = st.sidebar.selectbox(
                "Choose a table", ["SKU", "Synonym", "Language"]
            )
            if sub_table == "SKU":
                table_name = "fashion_global"
                cols1, cols2 = st.columns([2, 2])
                ch = cols1.radio("Choose an operation", ["Show table", "Edit table"])
                if ch == "Show table":
                    ch1 = cols2.selectbox(
                        "Select an option",
                        [
                            "",
                            "Version History - Username",
                            "Version History - Date",
                            "Show Full Table",
                        ],
                    )
                    if ch1 == "Version History - Username":
                        show_sku_table_username(conn, table_name)
                    elif ch1 == "Version History - Date":
                        show_sku_table_date(conn, table_name)
                    elif ch1 == "Show Full Table":
                        show_sku_table(conn, table_name)
                elif ch == "Edit table":
                    global_sku_fix(conn, username, "fashion_global")

            elif sub_table == "Synonym":
                table_name = "fashion_global_syn"
                cols1, cols2 = st.columns([2, 2])
                ch = cols1.radio("Choose an operation", ["Show table", "Edit table"])
                if ch == "Show table":
                    ch1 = cols2.selectbox(
                        "Select an option",
                        [
                            "",
                            "Version History - Username",
                            "Version History - Date",
                            "Show Full Table",
                        ],
                    )
                    if ch1 == "Version History - Username":
                        show_syn_table_username(conn, table_name)
                    elif ch1 == "Version History - Date":
                        show_syn_table_date(conn, table_name)
                    elif ch1 == "Show Full Table":
                        show_synonym_table(conn, table_name)
                elif ch == "Edit table":
                    global_syn_fix(
                        conn, username, "fashion_global_syn", "fashion_global"
                    )

            elif sub_table == "Language":
                table_name = "fashion_global_lang"
                cols1, cols2 = st.columns([2, 2])
                ch = cols1.radio("Choose an operation", ["Show table", "Edit table"])
                if ch == "Show table":
                    ch1 = cols2.selectbox(
                        "Select an option",
                        [
                            "",
                            "Version History - Username",
                            "Version History - Date",
                            "Show Full Table",
                        ],
                    )
                    if ch1 == "Version History - Username":
                        show_lang_table_username(conn, table_name)
                    elif ch1 == "Version History - Date":
                        show_lang_table_date(conn, table_name)
                    elif ch1 == "Show Full Table":
                        show_lang_table(conn, table_name)
                elif ch == "Edit table":
                    global_lang_fix(
                        conn, username, "fashion_global_lang", "fashion_global"
                    )

        if sub_option == "Bus":
            sub_table = st.sidebar.selectbox(
                "Choose a table", ["Location", "Synonym", "Language"]
            )
            if sub_table == "Location":
                table_name = "bus_global"
                cols1, cols2 = st.columns([2, 2])
                ch = cols1.radio("Choose an operation", ["Show table", "Edit table"])
                if ch == "Show table":
                    ch1 = cols2.selectbox(
                        "Select an option",
                        [
                            "",
                            "Version History - Username",
                            "Version History - Date",
                            "Show Full Table",
                        ],
                    )
                    if ch1 == "Version History - Username":
                        show_bussku_table_username(conn, table_name)
                    elif ch1 == "Version History - Date":
                        show_bussku_table_date(conn, table_name)
                    elif ch1 == "Show Full Table":
                        show_bussku_table(conn, table_name)
                elif ch == "Edit table":
                    global_bussku_fix(conn, username, "bus_global")

            elif sub_table == "Synonym":
                table_name = "bus_global_syn"
                cols1, cols2 = st.columns([2, 2])
                ch = cols1.radio("Choose an operation", ["Show table", "Edit table"])
                if ch == "Show table":
                    ch1 = cols2.selectbox(
                        "Select an option",
                        [
                            "",
                            "Version History - Username",
                            "Version History - Date",
                            "Show Full Table",
                        ],
                    )
                    if ch1 == "Version History - Username":
                        show_syn_table_username(conn, table_name)
                    elif ch1 == "Version History - Date":
                        show_syn_table_date(conn, table_name)
                    elif ch1 == "Show Full Table":
                        show_synonym_table(conn, table_name)
                elif ch == "Edit table":
                    global_syn_fix(conn, username, "bus_global_syn", "bus_global")

            elif sub_table == "Language":
                table_name = "bus_global_lang"
                cols1, cols2 = st.columns([2, 2])
                ch = cols1.radio("Choose an operation", ["Show table", "Edit table"])
                if ch == "Show table":
                    ch1 = cols2.selectbox(
                        "Select an option",
                        [
                            "",
                            "Version History - Username",
                            "Version History - Date",
                            "Show Full Table",
                        ],
                    )
                    if ch1 == "Version History - Username":
                        show_lang_table_username(conn, table_name)
                    elif ch1 == "Version History - Date":
                        show_lang_table_date(conn, table_name)
                    elif ch1 == "Show Full Table":
                        show_lang_table(conn, table_name)
                elif ch == "Edit table":
                    global_lang_fix(conn, username, "bus_global_lang", "bus_global")

    elif choice == "Customer Dataset":
        dashboard_page(username)


def page1():
    st.title("Login")
    choice = st.sidebar.radio("Select an option", ("Login", "Register", "Exit"))
    conn = establish_connection()
    if choice == "Login":
        login_page(conn)
    elif choice == "Register":
        register_page(conn)
    elif choice == "Exit":
        conn.close()
        st.title("Thank you!")


def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "page1"

    if st.session_state["page"] == "page1":
        page1()
    elif st.session_state["page"] == "dashboard":
        username = st.session_state["value_from_main"]
        choose_page(username)


def _parse_args():
    parser = argparse.ArgumentParser(description="Parser for app arguments")

    parser.add_argument(
        "--env",
        default="local",
        help="Environment name. Can be one of ['local', 'stage', 'prod']",
    )

    try:
        args = parser.parse_args()
        return args
    except SystemExit as e:
        # This exception will be raised if --help or invalid command line arguments
        # are used. Currently streamlit prevents the program from exiting normally
        # so we have to do a hard exit.
        os._exit(e.code)


if __name__ == "__main__":
    main()
