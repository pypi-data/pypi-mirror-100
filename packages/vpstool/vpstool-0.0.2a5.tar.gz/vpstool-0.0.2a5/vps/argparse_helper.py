from dofast.simple_parser import SimpleParser
from dofast.oss import Bucket, Message

from .toolkits.telegram import read_hema_bot, download_file_by_id, bot_messalert
from .network import Network, PapaPhone
from .linuxtools import LinuxTools

msg = """VPS toolkits 😏
-m(--monitor) ip:port ::: Monitor ip:port proxy
-ma(--messalert) message ::: Bot MessAlert. 
-k(--kill) process ::: Kill linux process.
-p(--phone) ::: Papa phone monitor.
-socks [port] ::: Set up a socks5 proxy.
"""


def parse_arguments():
    sp = SimpleParser()
    sp.add_argument('-cos',
                    '--cos',
                    sub_args=[["u", "up", "upload"], ["download", "d", "dw"],
                              ["l", "list"], ["del", "delete"]])
    sp.add_argument('-oss',
                    '--oss',
                    sub_args=[["u", "up", "upload"], ["download", "d", "dw"],
                              ["l", "list"], ["del", "delete"]])
    sp.add_argument('-m', '--monitor')
    sp.add_argument('-k', '--kill')
    sp.add_argument('-p', '--phone')
    sp.add_argument('-socks', '--socks')
    sp.parse_args()

    if sp.oss:
        access_id = decode
        cli = Bucket()
        if sp.oss.upload:
            cli.upload(sp.oss.upload)
        elif sp.oss.download:
            # Note the download func here is: dofast.utils.download
            du.download(cli.url_prefix + sp.oss.download)
        elif sp.oss.delete:
            cli.delete(sp.oss.delete)
        elif sp.oss.list:
            print(cli.url_prefix)
            cli.list_files()

    if sp.monitor:
        Network().monitor_proxy(sp.monitor.value)

    elif sp.kill:
        LinuxTools().pskill(sp.kill.value)

    elif sp.phone:
        PapaPhone().entry()

    elif sp.socks:
        port = sp.socks.value
        if port == 'PLACEHOLDER': port = 8888
        Network.setup_socks5_proxy(port)
    else:
        for l in msg.split("\n"):
            c, e = (l + " ::: ").split(':::')[:2]
            print("{:<70} {:<20}".format(c, e))
