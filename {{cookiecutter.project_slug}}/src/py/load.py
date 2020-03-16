

import seaborn as sns
import pandas as pd

params = snakemake.config

df = sns.load_dataset(params['dataset'])

df.to_feather(snakemake.output[0])

print('load finished')
