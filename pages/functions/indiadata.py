import pandas as pd

# from bs4 import BeautifulSoup


def return_india_table_df(url, pos, strip):
    # Create a handle, page, to handle the contents of the website
    df_list = pd.read_html(url)[pos]
    df_india = pd.DataFrame(df_list)
    df_india = df_india.drop(columns=["S. No."])
    df_india = df_india[:-strip]
    df_india.columns = ["State/UT", "Confirmed", "Recovered", "Deaths"]

    # print(df_india.info())
    df_india["Confirmed"] = df_india["Confirmed"].str.rstrip('*')

    df_india["Confirmed"] = df_india["Confirmed"].astype(int)
    df_india["Deaths"] = df_india["Deaths"].astype(int)
    df_india["Recovered"] = df_india["Recovered"].astype(int)

    return df_india


def return_india_map_df(url, pos, strip):
    # Create a handle, page, to handle the contents of the website
    df_list = pd.read_html(url)[pos]
    df_india = pd.DataFrame(df_list, dtype=str)
    df_india.columns = ["S. No.", "State", "Confirmed", "Recovered", "Deaths"]
    df_india = df_india[:-strip]

    df_india["Confirmed"] = df_india["Confirmed"].astype(float)
    df_india["Recovered"] = df_india["Recovered"].astype(float)
    df_india["Deaths"] = df_india["Deaths"].astype(float)

    df_india = df_india.set_index("S. No.", inplace=False)

    return df_india


def return_india_total_df(url, pos, endrow):
    # Create a handle, page, to handle the contents of the website
    df_list = pd.read_html(url)[pos]
    df_india = pd.DataFrame(df_list, dtype=str)
    df_india.columns = ["S. No.", "State", "Confirmed", "Recovered", "Deaths"]
    df_india_total = df_india.iloc[[-endrow]]
    df_india_total["Confirmed"] = df_india_total["Confirmed"].str.rstrip('*')

    return df_india_total
