from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, InlineQueryHandler
from my_parser import Parser
from uuid import uuid4
import logging

TOKEN = "637115124:AAHbAtbnTwEO10RutD0PmKSR8_tbz17i2R4"


def handle_start(bot, update):
    update.message.reply_text("Ciao, dimmi il nome di un luogo e troverò gli eventi nelle vicinanze per te")


def error(bot, update, e):
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.warning('Update {} caused error {}'.format(update, e))


def inline_place(bot, update):
    query = update.inline_query.query
    help_line = 'Scrivi il nome di una città per cercare solo gli eventi in quella città.' \
                'Puoi anche cercare in una intera regione!Oppure puoi cercare nei dintorni ' \
                'di una città scrivendo "dintorni" dopo il nome della città'

    if query == 'help':
        results = [
            InlineQueryResultArticle(
                id=uuid4(),
                title=help_line,
                input_message_content=InputTextMessageContent("Un attimo, sto usando @cercaEventi_bot")
            )
        ]
        update.inline_query.answer(results)
        return
    if not query or len(query) == 1:
        results = [
            InlineQueryResultArticle(
                id=uuid4(),
                title='Nessun evento trovato per {}'.format(query),
                input_message_content=InputTextMessageContent('Nessun evento trovato')
            )
        ]
    else:
        p = Parser(query)
        events = p.getEvents()
        if len(events) > 0:
            results = [
                InlineQueryResultArticle(
                    id=uuid4(),
                    title=event['name'],
                    input_message_content=InputTextMessageContent("{}\n{}".format(event['name'],event['link'])),
                )
                for event in events]
        else:
            results = [
                InlineQueryResultArticle(
                    id=uuid4(),
                    title='Nessun evento trovato per {}'.format(query),
                    input_message_content=InputTextMessageContent('Nessun evento trovato per {}'.format(query))
                )
            ]
    update.inline_query.answer(results)


def main():
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', handle_start)
    inline_place_handler = InlineQueryHandler(inline_place)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(inline_place_handler)
    dispatcher.add_error_handler(error)
    updater.start_polling()
    print('Listening...')
    updater.idle()


if __name__ == '__main__':
    main()
