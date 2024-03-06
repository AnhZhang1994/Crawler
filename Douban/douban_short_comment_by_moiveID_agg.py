import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import argparse
import wandb

parser = argparse.ArgumentParser(description="combine csv files by movie_id")
parser.add_argument("--csv_dir", type=str, help="the directory contains the csv files")
parser.add_argument(
    "--movie_id",
    type=str,
    help="the movie_id of the movie you wanna combine the csv files",
)
args = parser.parse_args()
wandb.init(project="douban_short_comment_agg", config=args, reinit=True)
wandb.log({"csv_dir": args.csv_dir, "movie_id": args.movie_id})


def combine_csv_by_movieID(csv_dir: str, movie_id: str) -> pd.DataFrame:
    dfs = []

    for filename in os.listdir(csv_dir):
        if (
            filename.endswith(".csv")
            and movie_id in filename
            and "combined" not in filename
            and "wanna" not in filename
        ):
            filepath = os.path.join(csv_dir, filename)
            print(f"Reading {filepath}...")
            df = pd.read_csv(filepath)
            dfs.append(df)

    combined_df_rated = pd.concat(dfs, ignore_index=True)
    combined_df_rated = combined_df_rated.drop_duplicates()
    combined_df_rated = combined_df_rated.drop_duplicates(
        subset=["comment_time", "comment_content"]
    )

    # Handle parsing errors for comment_time column
    try:
        combined_df_rated["comment_time"] = pd.to_datetime(
            combined_df_rated["comment_time"], errors="coerce"
        )
    except Exception as e:
        print("Error:", e)

    # Drop rows with NaT (parsing errors)
    combined_df_rated = combined_df_rated.dropna(subset=["comment_time"])

    combined_df_rated["comment_star"] = combined_df_rated["comment_star"].astype(str)
    combined_df_rated.to_csv(f"{csv_dir}/{movie_id}_rated_combined.csv", index=False)
    print(f"Combined csv file is saved at {csv_dir}/{movie_id}_rated_combined.csv")
    dfs = []

    for filename in os.listdir(csv_dir):
        if (
            filename.endswith(".csv")
            and movie_id in filename
            and "combined" not in filename
            and "wanna" in filename
        ):
            filepath = os.path.join(csv_dir, filename)
            print(f"Reading {filepath}...")
            df = pd.read_csv(filepath)
            dfs.append(df)

    combined_df_wanna = pd.concat(dfs, ignore_index=True)
    combined_df_wanna = combined_df_wanna.drop_duplicates()
    combined_df_wanna = combined_df_wanna.drop_duplicates(
        subset=["comment_time", "comment_content"]
    )

    # Handle parsing errors for comment_time column
    try:
        combined_df_wanna["comment_time"] = pd.to_datetime(
            combined_df_wanna["comment_time"], errors="coerce"
        )
    except Exception as e:
        print("Error:", e)

    # Drop rows with NaT (parsing errors)
    combined_df_wanna = combined_df_wanna.dropna(subset=["comment_time"])

    combined_df_wanna["comment_star"] = combined_df_wanna["comment_star"].astype(str)
    combined_df_wanna.to_csv(f"{csv_dir}/{movie_id}_wanna_combined.csv", index=False)
    print(f"Combined csv file is saved at {csv_dir}/{movie_id}_wanna_combined.csv")
    wandb.log(
        {
            "combined_csv_saved at ": csv_dir,
            "movie_id": movie_id,
            "time": pd.Timestamp.now(),
        }
    )
    return combined_df_rated, combined_df_wanna


if __name__ == "__main__":
    csv_dir = args.csv_dir
    movie_id = args.movie_id
    combine_csv_by_movieID(csv_dir, movie_id)
