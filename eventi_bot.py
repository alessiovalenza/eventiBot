from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, InlineQueryHandler
from my_parser import Parser
from uuid import uuid4

TOKEN = "637115124:AAHbAtbnTwEO10RutD0PmKSR8_tbz17i2R4"
# TOKEN = "669249562:AAGtdMSBoQe4PkG7jujjdeC2ktRlBMOkgN0"

def handle_start(bot, update):
    update.message.reply_text("Dimmi il nome di un luogo e troverò gli eventi nelle vicinanze per te")

def inline_place(bot, update):
    query = update.inline_query.query
    help = 'Scrivi il nome di una città per cercare solo gli eventi in quella città.\nPuoi anche cercare in una intera regione!\nOppure puoi cercare nei dintorni di una città scrivendo "dintorni" dopo il nome della città'
    if not query or len(query)==0:
        return
    else:
        if query == 'help':
            results = [
                InlineQueryResultArticle(
                    id=uuid4(),
                    title=help,
                    input_message_content=InputTextMessageContent("Un attimo, sto usando @cercaEventi_bot")
                )
            ]
            update.inline_query.answer(results)
            return
        p = Parser(query)
        events = p.getEvents()
        if len(events)>0:
            results = [
                InlineQueryResultArticle(
                    id=uuid4(),
                    title=event['name'],
                    input_message_content=InputTextMessageContent("{}\n<b>{}</b>\n<b>{}</b>\n{}".format(event['name'],event['date'],event['place'],event['link']),
                            parse_mode='HTML'),
                    thumb_url = event['img'],
                    description = "{}\n{}".format(event['date'],event['place'])
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
    updater.start_polling()
    print('Listening...')
    updater.idle()

if __name__ == '__main__':
    main()
