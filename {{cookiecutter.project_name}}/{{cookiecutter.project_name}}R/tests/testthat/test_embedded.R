

context('embedded')

test_that('embedded'
          ,{

    val = embedded_packages_are_great()
    expect_true( val == "embedded packages are great for testing" )

})
