from basics.ex_packages.data_extraction.helpers import helpers


def get_headers(main_content, header_tags):
    headers = []
    # Use the configured logger
    logger = helpers.setup_logger()
    try:
        headers = main_content.find_all(header_tags)
        logger.debug(f"Found {len(headers)} headers")
    except AttributeError as err:
        logger.error(f"main_content is invalid for find_all: {err}")

    except TypeError as err:
        logger.error(f"Invalid header_tags type: {err}")

    except Exception as err:
        logger.exception(f"Unexpected error in get_headers: {err}")

    return headers
