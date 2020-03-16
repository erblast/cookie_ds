wd = getwd()

debug_file = paste0('debug/', snakemake@rule, '.Rdata')
save.image(debug_file)

params= list()
params$input = snakemake@input[2:length(snakemake@input)]
params$output = snakemake@output[2:length(snakemake@output)]
params$config = snakemake@config
params$rule = snakemake@rule

output_file = paste0( getwd(),'/' , snakemake@output[[1]] )
output_file = normalizePath(output_file)

rmarkdown::render( snakemake@input[[1]]
                   , output_file = output_file
                   , params      = params
                   , knit_root_dir = getwd()
                   , envir = new.env()
)
