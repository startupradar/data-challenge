import logging
import os

import pandas as pd
import psycopg2
from startupradar.transformers.core import DomainTextTransformer, WhoisTransformer
from startupradar.transformers.util.api import StartupRadarAPI


def cli():
    df = pd.read_parquet(".data/full.parquet")
    print(df)


def load_data():
    """
    This loads the data from the servers.
    You don't need to run this, just use `full.parquet`.
    """
    # load domains and ratings
    df = pd.read_csv(".in/ratings.csv")
    df = df[~df["Rating"].isna()]
    # df = df.sample(10)
    df = df[["Domain", "Rating"]].set_index("Domain")
    df.to_parquet(".data/ratings.parquet")

    # load embeddings
    with psycopg2.connect(os.environ["DB_URL"]) as conn:
        with conn.cursor() as cur:
            sql = (
                "SELECT domain, data"
                " FROM openai_embeddings"
                " WHERE domain IN %s AND model = 'text-embedding-ada-002'"
            )
            cur.execute(
                sql,
                (tuple(df.index.values.tolist()),),
            )
            domain_and_data = cur.fetchall()
            domains, embeddings_data = list(zip(*domain_and_data))
            df_embeddings = pd.DataFrame(
                map(lambda ed: ed["data"][0]["embedding"], embeddings_data)
            )
            df_embeddings.columns = [f"e{c}" for c in df_embeddings.columns]
            df_embeddings.index = domains
            df_embeddings = df_embeddings[~df_embeddings.index.duplicated(keep="first")]
            df_embeddings.to_parquet(".data/embeddings.parquet")

    # load texts
    api = StartupRadarAPI(os.environ["STARTUPRADAR_API_KEY"])
    text_transformer = DomainTextTransformer(api)
    df_texts = text_transformer.transform(df.index.to_series())
    df_texts.to_parquet(".data/texts.parquet")

    # load whois
    whois_transformer = WhoisTransformer(api)
    df_whois = whois_transformer.transform(df.index.to_series())
    df_whois.to_parquet(".data/whois.parquet")


def combine_dfs():
    """
    This combines all the singular dataframe to one combined df.
    """

    df_ratings = pd.read_parquet(".data/ratings.parquet")
    df_whois = pd.read_parquet(".data/whois.parquet")
    df_texts = pd.read_parquet(".data/texts.parquet")
    df_embeddings = pd.read_parquet(".data/embeddings.parquet")

    df_full = df_ratings.join(df_whois).join(df_texts).join(df_embeddings)
    df_full.to_parquet(".data/full.parquet")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # load_data()
    # combine_dfs()
    cli()
