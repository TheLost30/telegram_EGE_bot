import logging

token = '5861871187:AAFUviveTBcgLgylI1R7XebO-NiZ_SjScCM'

logs_level = logging.WARNING

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logs_level)  # filename='latest.log'

logger = logging.getLogger(__name__)
