
#' @title wrapper around lintr::lint_packages which throws error when code issues are detected
#' @description -
#' @inheritParams lintr::lint_package
#' @return -
#' @details -
#' @export
#' @seealso
#'  \code{\link[lintr]{lint_package}}
#' @rdname lint_package
#' @export
#' @importFrom lintr lint_package
lint_package <- function(...) {
    lint_results <- lintr::lint_package(...)

    if (length(lint_results) > 0) {
        print(lint_results)
        stop(paste(lint_results))
    }

}
