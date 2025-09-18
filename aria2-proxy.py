from os import getenv
from typing import Any

from dotenv import load_dotenv
from flask import Flask
from flask_jsonrpc import JSONRPC
from flask_jsonrpc.exceptions import InvalidRequestError, JSONRPCError
from requests import Session as RequestsSession


client = RequestsSession()
app = Flask("application")
jsonrpc = JSONRPC(app, "/jsonrpc", enable_web_browsable_api=False)

load_dotenv()
TARGET_ADDR = getenv('TARGET_ADDR', '0.0.0.0:6801/jsonrpc')
HOST = getenv('HOST', '0.0.0.0')
PORT = getenv('PORT', '6800')
METHODS_TO_PROXY = [
    'aria2.remove',
    'aria2.forceRemove',
    'aria2.pause',
    'aria2.pauseAll',
    'aria2.forcePause',
    'aria2.forcePauseAll',
    'aria2.unpause',
    'aria2.unpauseAll',
    'aria2.tellStatus',
    'aria2.getUris',
    'aria2.getFiles',
    'aria2.getPeers',
    'aria2.getServers',
    'aria2.tellActive',
    'aria2.tellWaiting',
    'aria2.tellStopped',
    'aria2.changePosition',
    'aria2.changeUri',
    'aria2.getOption',
    'aria2.getGlobalOption',
    'aria2.getGlobalStat',
    'aria2.purgeDownloadResult',
    'aria2.removeDownloadResult',
    'aria2.getVersion',
    'aria2.getSessionInfo',
    'aria2.shutdown',
    'aria2.forceShutdown',
    'aria2.saveSession',
    'system.multicall',
    'system.listMethods',
    'system.listNotifications',
]


class DirOptionFobridden(InvalidRequestError):
    message = "Option 'dir' is forbidden"


def raise_error(error_data: dict):
    if error_data is None:
        raise JSONRPCError(message='unexpected error')
    raise JSONRPCError(
        message=error_data.get('message'),
        code=error_data.get('code'),
        data=error_data.get('data'),
        status_code=error_data.get('status_code')
    )


def call(method: str, params: Any) -> Any:
    print(params)
    response = client.post(
        TARGET_ADDR,
        json=dict(
            jsonrpc='2.0',
            id='1',
            method=method,
            params=params,
        )
    )
    response_data = response.json()
    print(response_data)
    result = response_data.get('result', None)
    if result is None:
        raise_error(response_data.get('error'))
    return result


def validate_no_dir_option(options: dict):
    if options.get('dir', '') != '':
        raise DirOptionFobridden()


@jsonrpc.method('aria2.addUri')
def add_uri(uris: list[str], *data: Any) -> str:
    if len(data) >= 1:
        validate_no_dir_option(data[0])
    return call('aria2.addUri', [uris, *data])


@jsonrpc.method('aria2.addTorrent')
def add_torrent(torrent: str, *data: Any) -> str:
    if len(data) >= 2:
        validate_no_dir_option(data[1])
    return call('aria2.addTorrent', [torrent, *data])


@jsonrpc.method('aria2.addMetalink')
def add_torrent(metalink: str, *data: Any) -> str:
    if len(data) >= 1:
        validate_no_dir_option(data[0])
    return call('aria2.addMetalink', [metalink, *data])


@jsonrpc.method('aria2.changeOption')
def add_torrent(gid: str, options: dict) -> str:
    validate_no_dir_option(options)
    return call('aria2.changeOption', [gid, options])


@jsonrpc.method('aria2.changeGlobalOption')
def add_torrent(options: dict) -> str:
    validate_no_dir_option(options)
    return call('aria2.changeGlobalOption', [options])


def generate_proxy_of(method: str):
    def proxy(*data: Any) -> Any:
        return call(method, [*data])
    return proxy


def setup():
    for method in METHODS_TO_PROXY:
        jsonrpc.register_view_function(generate_proxy_of(method), method)


def main():
    setup()
    app.run(host=HOST, port=PORT, debug=False)


if __name__ == '__main__':
    main()
