

test_files, = glob_wildcards('{{cookiecutter.project_name}}/tests/testthat/{test_file}.R')
function_files, = glob_wildcards('{{cookiecutter.project_name}}/R/{function_file}.R')

rule test:
    input:
        'testlog/test_{{cookiecutter.project_name}}.txt',
        'testlog/check_{{cookiecutter.project_name}}.txt'

rule test_{{cookiecutter.project_name}}:
    input:
        expand('{{cookiecutter.project_name}}/R/{function_file}.R', function_file = function_files),
        expand('{{cookiecutter.project_name}}/tests/testthat/{test_file}.R', test_file = test_files)
    output:
        'testlog/test_{{cookiecutter.project_name}}.txt'
    shell:
        "Rscript -e 'sink(\"{output}\")' -e 'devtools::test(\"./{{cookiecutter.project_name}}\")' -e 'sink()'"
        
rule check_{{cookiecutter.project_name}}:
    input:
        expand('{{cookiecutter.project_name}}/R/{function_file}.R', function_file = function_files),
        expand('{{cookiecutter.project_name}}/tests/testthat/{test_file}.R', test_file = test_files),
        'testlog/test_{{cookiecutter.project_name}}.txt'
    output:
        'testlog/check_{{cookiecutter.project_name}}.txt'
    shell:
        "Rscript -e 'sink(\"{output}\")' -e 'devtools::check(\"./{{cookiecutter.project_name}}\")' -e 'sink()'"
