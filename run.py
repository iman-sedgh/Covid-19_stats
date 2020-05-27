from scraper import Data
import logging
from uuid import uuid4
from telegram.ext import Updater, CommandHandler, InlineQueryHandler, CallbackQueryHandler
from telegram import ( InputTextMessageContent, InlineQueryResultArticle ,
    InlineKeyboardButton, InlineKeyboardMarkup )
import schedule
import time
import pycountry
from emoji import emojize
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

PROJECT_TOKEN = "tPwDTyxPRMD6"
API_KEY = "tT3y7qX1U9zq"
token = '1154001455:AAGORgp9gVuifyMTlQjuipblb0YjWuG0sts' #CoronaVirusStats_Bot
#token = '422767920:AAEZVBVBYoCrWu4Pula_eccUiYDcn5FPCq0' #iman iot prj bot

updater = Updater(token, use_context=True)
data = Data( API_KEY, PROJECT_TOKEN )
Keyboards = None

def start_method(update, context):
    update.message.reply_text("Welcome to Our Bot.\n Developer :  @Iman_Sedgh  \n This is a Free Python Script Using BS4 and Python-telegram-bot modules \n Github : https://github.com/iman-sedgh/Air-pollution-Scraping ")
    update.message.reply_text("""
To Get Corona Virus Cases Details All Around The World Use /Get_total
To Get Corona Virus Cases Details For a specific country Use /Get_country
        """)

def get_total(update,context):
    """Returns total Values"""
    print('get method')
    total_data = data.get_total_data()
    update.message.reply_text(f"""
    Total Corona Virus Details All Around The World 🌎 :
Number Of Corona Virus Cases: {total_data["coronavirus cases:"]}
Number Of Corona Virus Deaths: {total_data["deaths:"]}
Number Of Corona Virus Recovers: {total_data["recovered:"]}""" )

def get_by_country(update,context):
    global Keyboards
    Keyboards = make_keyboards()
    keyboard = Keyboards[0]
    update.message.reply_text("Select a country to see details for that specific country "
        ,reply_markup = InlineKeyboardMarkup(keyboard))

def make_keyboards():
    btn = InlineKeyboardButton
    keyboards = [ [[]] ]
    country_data = data.country_data
    country_list = list( country_data.keys() )
    for keyboard in keyboards:
        if(len(country_list) == 0 ):
            break
        for i in range(0,10) :
            for x in range(0,2):
                if(len(country_list) == 0):
                    break
                country_name = country_list.pop(0)
                tmp = country_name
                if(len(tmp)>= 4):
                    tmp = tmp.title()
                else:
                    tmp = tmp.upper()
                flag = get_flag(tmp)
                nice_name = tmp + str (f" {flag}")
                keyboard[i].append( btn( nice_name  ,callback_data=country_name +'\n'+ nice_name ) )
            keyboard.append([])#new row
        index = len(keyboards) -1
        if( len(keyboards) > 1):
            keyboard[10].append( btn('Back', callback_data= str( index-1 )  ))
        if( len(keyboards) < 10):
            keyboard[10].append( btn('Next', callback_data= str( index+1  ) ) )
        keyboards.append([[]])
    return keyboards

def get_by_country_query(update,context):
    query = update.callback_query
    query_data = query.data.split('\n')
    Qdata =query_data[0]  #query_data[0]-> country_name(lowercase) query_data[1]->tmp(Display Name)
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    if( Qdata.isnumeric() and Keyboards ):
        reply_markup = InlineKeyboardMarkup(Keyboards[int ( Qdata ) ])
        context.bot.editMessageReplyMarkup(chat_id=chat_id, message_id= message_id ,
                reply_markup = reply_markup)    
    else:
        display_name = query_data[1]
        country_data = data.get_country_data(Qdata)
        text= f"""
        Details For {display_name+" : "}
Number Of Corona Virus Cases: {country_data["total"]}
Number Of Corona Virus Deaths: {country_data["death"]}
Number Of Corona Virus Recovers: {country_data["recovered"]}"""
        context.bot.editMessageText(text = text,chat_id = chat_id,message_id= message_id )
        return None

def get_flag(country_name):
    OFFSET = 127462 - ord('A')
    country = pycountry.countries.get(name = country_name)
    if (country == None):
        if(len(country_name)>15):
            country_name = country_name[:15]
        flag = emojize(f":{country_name}:",use_aliases=True)
        if(flag == f":{country_name}:"):
            missing_flags = {"USA":'🇺🇸',"UK":'🇬🇧',"UAE":'🇦🇪',"S. Korea":'🇰🇷',"Bosnia And Herz":'🇧🇦',
                "Ivory Coast":'🇨🇮',"DRC":'🇨🇩',"CAR":'🇨🇫',"Channel Islands":'🇯🇪',
                "Palestine":'🇵🇸',"Isle Of Man":'🇮🇲',"Sao Tome And Pr":'🇸🇹',"Trinidad And To":'🇹🇹',"Sint Maarten":'🇸🇽',
                "Saint Martin":'🇲🇫',"Antigua And Bar":'🇦🇬',"Turks And Caico":'🇹🇨',"British Virgin ":'🇻🇬'}
            flag = missing_flags.get(country_name)
            
        return flag
     
    else: 
        code =country.alpha_2
        code = code.upper()
        return chr(ord(code[0]) + OFFSET) + chr(ord(code[1]) + OFFSET)



"""
def inline_feature(update,context):
    query = update.inline_query.query
    results = []
    results.append(InlineQueryResultArticle(id = uuid4(),title="English",input_message_content = InputTextMessageContent("Air Quality Index Of Tehran Is {}".format(str(quality.getairquality())))))
    results.append(InlineQueryResultArticle(id = uuid4(),title="Persian",input_message_content = InputTextMessageContent("شاخص آلودگی هوای تهران در حال حاضر {}".format(str(quality.getairquality())))))
    if query.find('{}') != -1:
        results.append(InlineQueryResultArticle(id = uuid4(),title="Custom Text",input_message_content = InputTextMessageContent(query.format(("<b>" +quality.getairquality() + "</b>")),parse_mode='HTML')))
    else :
        results.append(InlineQueryResultArticle(id = uuid4(),title="Custom Text",description='*Error !!!*' ,input_message_content = InputTextMessageContent ("* Error \n {} Not Found !!*",parse_mode='Markdown')))
    update.inline_query.answer(results)
"""

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def Job_Refresh(bot=None):
    data.refresh_data()



if(__name__ == "__main__"):
    updater.dispatcher.add_handler( CommandHandler( 'start', start_method ) )
    updater.dispatcher.add_handler( CommandHandler( 'get_total',get_total ) )
    updater.dispatcher.add_handler( CommandHandler( 'get_country',get_by_country ) )
    updater.dispatcher.add_handler( CallbackQueryHandler(get_by_country_query) )
#    updater.dispatcher.add_handler( InlineQueryHandler( inline_feature ) )
    updater.dispatcher.add_error_handler( error )
    updater.job_queue.run_repeating(Job_Refresh,60,first=0)

    updater.start_polling()
    updater.idle()