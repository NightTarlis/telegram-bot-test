from telegram.ext import filters

import handlers

command_handlers = (
    ('start', handlers.start, 'handler to start communication'),
)

message_handlers = (
    (filters.Regex(r'(?i)buy.*'), handlers.exchange, 'handler for buying'),
    (filters.Regex(r'(?i)sell.*'), handlers.exchange, 'handler for sales'),
    (filters.Regex(r'(?i)report'), handlers.report, 'handler for report'),
    (filters.TEXT & (~filters.COMMAND), handlers.uncategorized_messages, 'handler for other messages'),
)
