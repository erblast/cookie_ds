configfile: 'config/config.yml'

# {{cookiecutter.r_pkg_name}} testing

test_files, = glob_wildcards('src/{{cookiecutter.r_pkg_name}}/tests/testthat/{test_file}.R')
function_files, = glob_wildcards('src/{{cookiecutter.r_pkg_name}}/R/{function_file}.R')

rule test:
    input:
        'docs/testlog/test_{{cookiecutter.r_pkg_name}}.txt',
        'docs/testlog/check_{{cookiecutter.r_pkg_name}}.txt',
        "docs/testlog/lint_{{cookiecutter.r_pkg_name}}.txt", 
        "docs/{{cookiecutter.r_pkg_name}}/index.html"

rule test_{{cookiecutter.r_pkg_name}}:
    input:
        expand('src/{{cookiecutter.r_pkg_name}}/R/{function_file}.R', function_file = function_files),
        expand('src/{{cookiecutter.r_pkg_name}}/tests/testthat/{test_file}.R', test_file = test_files)
    output:
        report('docs/testlog/test_{{cookiecutter.r_pkg_name}}.txt', category="test")
    shell:
        "Rscript -e 'sink(\"{output}\")' -e 'devtools::test(\"./src/{{cookiecutter.r_pkg_name}}\")' -e 'sink()'"
        
rule check_{{cookiecutter.r_pkg_name}}:
    input:
        expand('src/{{cookiecutter.r_pkg_name}}/R/{function_file}.R', function_file = function_files),
        expand('src/{{cookiecutter.r_pkg_name}}/tests/testthat/{test_file}.R', test_file = test_files),
        'docs/testlog/test_{{cookiecutter.r_pkg_name}}.txt'
    output:
        report('docs/testlog/check_{{cookiecutter.r_pkg_name}}.txt', category="check")
    shell:
        "Rscript -e 'sink(\"{output}\")' \
                 -e 'devtools::check(\"./src/{{cookiecutter.r_pkg_name}}\", error_on = \"{config[fail_check_on]}\")' \
                 -e 'sink()'"

rule render_docs:
    input:
        expand('src/{{cookiecutter.r_pkg_name}}/R/{function_file}.R', function_file = function_files),
        expand('src/{{cookiecutter.r_pkg_name}}/tests/testthat/{test_file}.R', test_file = test_files),
        'docs/testlog/check_{{cookiecutter.r_pkg_name}}.txt',
    output:
        "docs/{{cookiecutter.r_pkg_name}}/index.html"
    shell:
        """R -e 'pkgdown::build_site("src/{{cookiecutter.r_pkg_name}}/")' """

if config["lint"]:
  rule lint:
    input:
        "docs/{{cookiecutter.r_pkg_name}}/index.html"
    output:
      report("docs/testlog/lint_{{cookiecutter.r_pkg_name}}.txt", category="lint")
    shell: """
              Rscript -e 'sink(\"{output}\")' \
                      -e 'devtools::load_all("src/{{cookiecutter.r_pkg_name}}")' \
                      -e 'my_linters <- with_defaults(line_length_linter = line_length_linter(120))' \
                      -e 'lint_package("src/{{cookiecutter.r_pkg_name}}", linters = my_linters)' \
                      -e 'sink()' \
             """
else:
  rule lint:
    shell: "touch {output} && \
            echo 'lint switched off in confg/config.yml' >> {output}"


