import os
import requests
import json
import pandas as pd
from github import Github
from github.InputFileContent import InputFileContent

ENV_LEETCODE_USERNAME = "LEETCODE_USERNAME"
# these variables should be set as secrets in the repository!
ENV_GH_TOKEN = "GH_TOKEN" # token with gist scope enabled
ENV_GIST_ID = "GIST_ID" # id part of gist url

DIFFICULTY = [
   "advanced",
   "intermediate",
   "fundamental"
]
REQUIRED_ENVS = [
    ENV_GH_TOKEN,
    ENV_GIST_ID,
    ENV_LEETCODE_USERNAME
]
LEETCODE_URL = "https://leetcode.com/graphql"


def main() -> None:
  if check_vars():
    update_gist(create_graph(get_stats()))

'''
check that the environment variables are correctly declared.
'''
def check_vars() -> bool:
    env_vars_absent = [
        env
        for env in REQUIRED_ENVS
        if env not in os.environ or len(os.environ[env]) == 0
    ]
    if env_vars_absent:
        print(f"Could not find {env_vars_absent} in your github secrets. Check the\
              secrets in the repo settings.")
        return False

    return True

'''
get stats from leetcode and organise them into a pandas dataframe.
'''
def get_stats() -> pd.DataFrame:
    variables = {"username": os.environ[ENV_LEETCODE_USERNAME]}
    query = '''
    query Skills ($username: String!) {
      matchedUser(username: $username) {
        tagProblemCounts {
          advanced {
            tagName
            problemsSolved
          }
          intermediate {
            tagName
            problemsSolved
          }
          fundamental {
            tagName
            problemsSolved
          }
        }
      }
    }
    '''
    x = requests.post(LEETCODE_URL, json={"query": query, "variables": variables})
    data = json.loads(x.text)["data"]["matchedUser"]["tagProblemCounts"]
    
    skill_frame = pd.DataFrame(columns=["skill", "count", "difficulty"])

    for difficulty in DIFFICULTY:
        for entry in data[difficulty]:
            skill_frame = skill_frame.append({
                "skill": entry["tagName"],
                "count": entry["problemsSolved"],
                "difficulty": difficulty
            }, ignore_index=True)

    return skill_frame.sort_values(by=["count"], ascending=False).reset_index(drop=True)


'''
create and format an ascii graph of the top five skills, making sure the
total character length of each label and bar does not exceed 46 characters.
'''
def create_graph(df: pd.DataFrame) -> str:
    max_str = max(df["skill"][0:5].str.len())
    max_digit = len(str(df["count"].max()))
    bar_len = 46 - (max_str + max_digit + 4)

    df["pct"] = df["count"] / df["count"].max() * bar_len

    f = "{0:<%d} ({1:>%d}) {2}{3} {4}\n" % (max_str, max_digit)

    graph_str = ""
    for i in range(0, min(len(df), 8)):
        graph_str += f.format(df["skill"][i], df["count"][i],
                                   '█' * round(df["pct"][i]),
                                   '░' * (bar_len - round(df["pct"][i])),
                                    df["difficulty"][i])

    return graph_str

'''
overwrite the existing contents of the gist with the ascii graph string.
'''
def update_gist(graph: str) -> None:
    gist = Github(os.environ[ENV_GH_TOKEN]).get_gist(os.environ[ENV_GIST_ID])
    title = list(gist.files.keys())[0]
    gist.edit(
        title,
        {title: InputFileContent(graph)}
    )


if __name__ == "__main__":
    main()
