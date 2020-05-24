from scraper import Data
import logging
from uuid import uuid4
from telegram.ext import Updater, CommandHandler, InlineQueryHandler
from telegram import InputTextMessageContent, InlineQueryResultArticle
import schedule
import time

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

token = '1154001455:AAGORgp9gVuifyMTlQjuipblb0YjWuG0sts' #CoronaVirusStats_Bot
#token = '422767920:AAEZVBVBYoCrWu4Pula_eccUiYDcn5FPCq0' #iman iot prj bot

updater = Updater(token, use_context=True)
data = Data()

def start_method(bot, update):
    bot.message.reply_text("Welcome to Our Bot.\n Developer :  @Iman_Sedgh  \n This is a Free Python Script Using BS4 and Python-telegram-bot modules \n Github : https://github.com/iman-sedgh/Air-pollution-Scraping ")
    bot.message.reply_text("To Get Corona Virus Cases /Get")

def get_method(bot,update):
    print('get method')
    bot.message.reply_text("Getting Index From {}".format(data.url),disable_web_page_preview= True)
    numbers_list = data.get_data()
    print(numbers_list)
    bot.message.reply_text(f"""
Number Of Corona Virus Cases: {numbers_list[0]}
Number Of Corona Virus Deaths: {numbers_list[1]}
Number Of Corona Virus Recovers: {numbers_list[2]} """)
"""

def inline_feature(bot,update):
    query = bot.inline_query.query
    results = []
    results.append(InlineQueryResultArticle(id = uuid4(),title="English",input_message_content = InputTextMessageContent("Air Quality Index Of Tehran Is {}".format(str(quality.getairquality())))))
    results.append(InlineQueryResultArticle(id = uuid4(),title="Persian",input_message_content = InputTextMessageContent("شاخص آلودگی هوای تهران در حال حاضر {}".format(str(quality.getairquality())))))
    if query.find('{}') != -1:
        results.append(InlineQueryResultArticle(id = uuid4(),title="Custom Text",input_message_content = InputTextMessageContent(query.format(("<b>" +quality.getairquality() + "</b>")),parse_mode='HTML')))
    else :
        results.append(InlineQueryResultArticle(id = uuid4(),title="Custom Text",description='*Error !!!*' ,input_message_content = InputTextMessageContent ("* Error \n {} Not Found !!*",parse_mode='Markdown')))
    bot.inline_query.answer(results)
"""


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def Job():
    data.scrape_data()

if(__name__ == "__main__"):
    updater.dispatcher.add_handler( CommandHandler( 'start', start_method ) )
    updater.dispatcher.add_handler( CommandHandler( 'get',get_method ) )
#    updater.dispatcher.add_handler( InlineQueryHandler( inline_feature ) )
    updater.dispatcher.add_error_handler( error )
    schedule.every(60).minutes.do(Job)
    Job()
    updater.start_polling()
    updater.idle()
    while True:  
        # Checks whether a scheduled task  
        # is pending to run or not 
        schedule.run_pending() 
        time.sleep(1) 
