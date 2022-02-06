import pandas as pd
from pandas import json_normalize
import json
import numpy as np

W = '\033[0m';Y = '\033[33m';B = '\033[34m'

with open('output.json', 'r') as j:
    content = json.loads(j.read())
    df = pd.json_normalize(content['calendarItems'])
    df = df[['assignment.assignmentName', 'assignment.grade']]
    for i in range(30, 34):
        try:
            print('Grade of ', B+df.iloc[i][0]+Y, int(df.iloc[i][1]))
        except:
            print(B+df.iloc[i][0]+Y, "No Grade Yet")