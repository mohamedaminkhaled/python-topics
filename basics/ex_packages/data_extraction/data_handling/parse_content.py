from bs4 import BeautifulSoup

from basics.ex_packages.data_extraction.helpers import helpers


def get_html_content(response, parser):
    # Use the configured logger
    logger = helpers.setup_logger()
    try:
        soup = BeautifulSoup(response.content, parser)
        main_content = soup.find('div', class_='body') or soup.find('div', class_='document') or soup.find('body')
        logger.debug(f"Found HTML Content: {len(main_content.text)} bytes")
        return main_content

    except AttributeError as err:
        # Handle missing attributes differently
        logger.warning(f"Response might be invalid: {err}")
        return None

    except TypeError as err:
        # Handle type issues differently
        logger.error(f"Programming error - wrong types: {err}")
        raise  # Re-raise because this might be a bug

    except ValueError as err:
        # Handle parser issues - maybe try alternative
        logger.info(f"Parser issue, trying default: {err}")
        return get_html_content(response, 'html.parser')  # Retry with default

    except Exception as err:
        # Only catch truly unexpected errors
        logger.critical(f"Unexpected parsing error: {err}")
        return None
