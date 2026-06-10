import logging
import sys
from config import LOG_FILE, LOG_LEVEL

def get_logger(name="ETL_Pipeline"):
    """
    Sets up and returns a configured logger that logs to both console and file.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(LOG_LEVEL)
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # File Handler
        try:
            fh = logging.FileHandler(LOG_FILE, encoding='utf-8')
            fh.setFormatter(formatter)
            logger.addHandler(fh)
        except Exception as e:
            print(f"Warning: Could not create log file handler: {e}")

        # Console Handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger

def capitalize_each_word(text):
    """
    Capitalizes the first letter of each word and lowers all other letters.
    Replicates Talend's CapitalizeEachWord.capitailizeOnlyFirst.
    """
    if text is None or not isinstance(text, str):
        return text
    # Trim and split words by space, capitalize each word, then join back with a single space
    return ' '.join(word.capitalize() for word in text.strip().split())

def extract_sku(sku):
    """
    Returns SKU code up to (but not including) the second hyphen.
    Replicates Talend custom routine ExtractSKU.Extract.
    Example: 'HL-U509-R' -> 'HL-U509'
    """
    if not isinstance(sku, str):
        return sku
    parts = sku.split('-')
    if len(parts) >= 2:
        return '-'.join(parts[:2])
    return sku

def extract_sku_category(sku):
    """
    Returns SKU code up to (but not including) the first hyphen.
    Replicates Talend custom routine ExtractSKU.ExtractSKUCategory.
    Example: 'HL-U509-R' -> 'HL'
    """
    if not isinstance(sku, str):
        return sku
    parts = sku.split('-')
    if len(parts) >= 1:
        return parts[0]
    return sku
