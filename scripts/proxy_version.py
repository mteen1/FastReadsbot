import os
import logging
import pyvmomi
import telegram.ext

from api_key import TOKEN

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Set up the vmess proxy
    vcenter_host = 'my-vcenter.example.com'
    vcenter_user = 'my-username'
    vcenter_password = 'my-password'
    vm_name = 'my-proxy-vm'
    vm_port = 1080
    service_instance = pyvmomi.connect.SmartConnectNoSSL(host=vcenter_host, user=vcenter_user, pwd=vcenter_password)
    vm = pyvmomi.vim.VirtualMachine(service_instance.content.searchIndex.FindByDnsName(None, vm_name))

    # Set up the Telegram bot with the vmess proxy
    request_kwargs = {
        'proxy_url': f'socks5://{vm.guest.ipAddress}:{vm_port}',
        'urllib3_proxy_kwargs': {}
    }
    updater = telegram.ext.Updater(TOKEN, request_kwargs=request_kwargs)
    dispatcher = updater.dispatcher

    # Add a command handler for the /hello command
    def handle_hello(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Hello!")

    dispatcher.add_handler(telegram.ext.CommandHandler('hello', handle_hello))

    # Start the bot
    updater.start_polling()
    updater.idle()

    # Disconnect from the vCenter server
    pyvmomi.connect.Disconnect(service_instance)
