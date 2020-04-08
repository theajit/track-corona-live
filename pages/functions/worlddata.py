import pandas as pd
import numpy as np
import country_converter as coco


def return_world_table_df(url, start, strip):

    df_list = pd.read_html(url)[0]
    df = pd.DataFrame(df_list)

    df_final = df.drop(columns=["Unnamed: 0",
                                "Unnamed: 6",
                                "Unnamed: 9",
                                "Unnamed: 10",
                                "Unnamed: 11",
                                "Unnamed: 12",
                                "Unnamed: 13",
                                "Unnamed: 14",
                                "Unnamed: 15",
                                "Unnamed: 16"
                                ])
    df_final.columns = ["Country",
                        "Confirmed",
                        "New Confirmed",
                        "Deaths",
                        "New Deaths",
                        "Serious & Critical",
                        "Recovered"]

    df_country = df_final.loc[start:, :]
    df_country = df_country[:-strip]

    df_country = df_country.replace(np.nan, value=0)

    df_country["Confirmed"] = df_country["Confirmed"].astype(float)
    df_country["New Confirmed"] = df_country["New Confirmed"].astype(float)
    df_country["Deaths"] = df_country["Deaths"].astype(float)
    df_country["Deaths"] = df_country["Deaths"].astype(float)
    df_country["Serious & Critical"] = df_country["Serious & Critical"].astype(
        float)
    df_country["Recovered"] = df_country["Recovered"].astype(int)

    return df_country


def return_world_map_df(url, start, strip):

    df_list = pd.read_html(url)[0]

    df = pd.DataFrame(df_list)

    df_final = df.drop(
        columns=[
            "Unnamed: 0",
            "Unnamed: 3",
            "Unnamed: 5",
            "Unnamed: 6",
            "Unnamed: 9",
            "Unnamed: 10",
            "Unnamed: 11",
            "Unnamed: 12",
            "Unnamed: 13",
            "Unnamed: 14",
            "Unnamed: 15",
            "Unnamed: 16",
            # "Unnamed: 17",
            # "Unnamed: 18",
            # "Unnamed: 19",
            # "Unnamed: 20"
        ]
    )
    df_final.columns = ["Country", "Confirmed", "Deaths", "Serious & Critical", "Recovered"]
    df_country = df_final.set_index("Country", inplace=False)
    df_country = df_final.loc[start:, :]
    df_country["iso_alpha"] = df_country["Country"].apply(
        lambda x: coco.convert(names=x, src="regex", to="ISO3", not_found=None)
    )
    df_country = df_country[:-strip]
    df_country = df_country.replace(to_replace=np.nan, value=0)

    return df_country


def return_world_total_df(url, endrow):

    df_list = pd.read_html(url)[0]

    df = pd.DataFrame(df_list)
    df_final = df.drop(
        columns=[
            "Unnamed: 0",
            "Unnamed: 3",
            "Unnamed: 5",
            "Unnamed: 6",
            "Unnamed: 9",
            "Unnamed: 10",
            "Unnamed: 11",
            "Unnamed: 12",
            "Unnamed: 13",
            "Unnamed: 14",
            "Unnamed: 15",
            "Unnamed: 16",
            # "Unnamed: 17",
            # "Unnamed: 18",
            # "Unnamed: 19",
            # "Unnamed: 20"
        ]
    )
    df_final.columns = ["Country", "Confirmed", "Deaths", "Serious & Critical", "Recovered"]
    df_country = df_final.set_index("Country", inplace=False)
    df_total = df_country.iloc[[-endrow]]
    # df_total = df_total.replace(np.nan, value =0)
    df_total = df_total.replace("-", 0, regex=True)
    df_total = df_total.fillna(0)

    return df_total
