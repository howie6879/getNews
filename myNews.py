"""myNews

Usage: myNews [-p] <port>

Options:
    -h,--help       显示帮助菜单
    -p              端口号

Example:
    myNews -p 8888  设置端口号为8888
"""

from docopt import docopt
from server import main


def cli():
    kwargs = docopt(__doc__)
    port = kwargs['<port>']
    main(port)


if __name__ == "__main__":
    cli()
