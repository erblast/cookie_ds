

import papermill as pm

# Run Parametrized Notebook

pm.execute_notebook(  snakemake.input[0]
                    , snakemake.output[0]
                    , parameters = dict( input = snakemake.input[1:]
                                        , config = snakemake.config) )
