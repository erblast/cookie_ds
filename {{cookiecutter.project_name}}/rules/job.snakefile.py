# job rules must not only use unit-tested code from packages --no scripts
# jobs are not executed during CI/CD runs
# use environment variables to configure jobs

envvars: "JOB_VAR1"

rule job:
    params:
      job_var1=os.environ["JOB_VAR1"]
    shell: """
            R -e 'devtools::load_all("src/{{cookiecutter.r_pkg_name}}")' \
              -e 'embedded_packages_are_great()' \
              -e 'print("{params.job_var1}")'
           """