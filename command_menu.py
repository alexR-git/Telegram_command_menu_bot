from telegram import Update, InputMediaDocument, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext, PrefixHandler, ConversationHandler

import Token as btoken

token = btoken.token

print('Bot iniciado...')

def start_command(update: Update, context: CallbackContext) -> None:    # devuelve None

    """ Método para contestar cuando el usuario escriba el comando /start """

    user_id = update.message.from_user.id
    print('user ID:', user_id)
    user_name = update.message.from_user.username
    print('user name:', user_name)
    first_name = update.message.from_user.first_name
    print('first_name:', first_name)
    chat_id = update.message.chat_id
    print('chat ID:', chat_id)

    update.message.reply_text(
        text=f'¡Hola, <b>{user_name}!</b>\n\n'
             f'Puedes escribir los siguientes comandos:\n\n'
             f'<i>/contact</i> para contacto\n'
             f'<i>/repeatingreminder+[segundos]</i> para que te envíe un recordatorio cada [segundos]\n'
             f'<i>/rateme</i> para ponerme nota\n\n'
             f'¡Un saludo!',
        parse_mode='HTML'
    )

def contact(update: Update, context: CallbackContext) -> None:  # devuelve None

    """ Método para mostrar las fuentes de contacto del bot """

    user_id = update.message.from_user.id
    print('user ID:', user_id)
    user_name = update.message.from_user.username
    print('user name:', user_name)
    first_name = update.message.from_user.first_name
    print('first_name:', first_name)
    chat_id = update.message.chat_id
    print('chat ID:', chat_id)

    update.message.reply_text(
        text='Puedes encontrarme en cualquiera de las siguientes direcciones:'
    )

    update.message.reply_photo(
        open('[ruta local de la imagen]', 'rb'),
        caption='En [nombre de la ubicación]'
    )

    # coordenadas de la ubicación
    lat = 39.4763
    long = -0.3752

    update.message.reply_text('Ubicada aquí:')

    update.message.reply_location(
        longitude=long,
        latitude=lat
    )

def repeating_reminder(callback_context) -> None:

    """ Método callback del job queue run_repeating del método schedule_repeating """

    callback_context.bot.send_message(
        chat_id=callback_context.job.context,
        text='repeating reminder message'
    )

def schedule_repeating(update: Update, context: CallbackContext) -> None:

    """ Método para que le repita un mensaje a un usuario cada X segundos pasados por el usuario mismo en el comando """

    context.job_queue.run_repeating(
        callback=repeating_reminder,
        interval=int(context.args[0]),
        context=update.message.chat_id
    )

    update.message.reply_text(text=f'Hola, te voy a enviar un reminder cada {context.args[0]} segundos')

def rate_me(update: Update, context: CallbackContext) -> None:  # devuelve None

    """ Método para lanzar una encuesta para evaluar al bot """

    user_id = update.message.from_user.id
    print('user ID:', user_id)
    user_name = update.message.from_user.username
    print('user name:', user_name)
    first_name = update.message.from_user.first_name
    print('first_name:', first_name)
    chat_id = update.message.chat_id
    print('chat ID:', chat_id)
    message_id = update.message.message_id
    print('message ID:', message_id)

    update.message.reply_poll(
        question='¿Qué puntuación me das? No te preocupes, la encuesta es anónima.',            # pregunta de la encuesta
        options=['1: muy mejorable', '2: mejorable', '3: bien', '4: muy bien', '5: perfecto'],  # lista de strings con las opciones
        is_anonymous=True,                  # encuesta anónima
        type='regular',                     # encuesta normal, no cuestionario.
        allows_multiple_answers=False,      # no permitir respuestas múltiples
        open_period=60,                     # tiempo que la encuesta está abierta
    )

def error(update: Update, context: CallbackContext) -> None:    #devuelve None

    """ Método de error """

    print(f'Update {update} caused error {context.error}')

def main():

    updater = Updater(token)                        # objeto Updater: interfaz con el bot: nos permite interactuar con él
    print('updater creado')
    #updater = Updater(token, use_context=True)
    dp = updater.dispatcher                         # objeto dispatcher: hacia donde se va a despachar todas las actualizaciones de mensajes que haga un usuario hacia nosotros
    print('dispatcher creado')

    # COMMANDHANDLERS
    dp.add_handler(CommandHandler('contact', contact))  # handler de comando para el contacto
    dp.add_handler(CommandHandler("rateme", rate_me))   # handler de comando para la evaluación del bot
    dp.add_handler(CommandHandler(
        command='repeatingreminder',
        callback=schedule_repeating
    ))

    # ERRORHANDLER
    dp.add_error_handler(error)     # le especificamos que invoque el método error

    updater.start_polling(5)    # listo para escuchar en 5 minutos
    updater.idle()              # método para que el bot se quede escuchando

main()