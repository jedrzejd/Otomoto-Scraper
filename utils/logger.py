from __future__ import annotations

import logging

file_logger = logging.getLogger('file_logger')
file_logger.setLevel(logging.INFO)

console_logger = logging.getLogger('console_logger')
console_logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler('output/logs/app.log')
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s - [%(name)s] - [%(levelname)s] - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

console_logger.addHandler(console_handler)
file_logger.addHandler(file_handler)
