#!/usr/bin/python
import warnings; warnings.simplefilter('ignore')
from tests.gethrpc import GethRPC, dumps
from pyepm.api import abi_data
from colorama import init, Style, Fore
import sys
import re

contracts = {
    'cash' : '0xf1d413688a330839177173ce98c86529d0da6e5c',
    'info' : '0x910b359bb5b2c2857c1d3b7f207a08f3f25c4a8b',
    'branches' : '0x13dc5836cd5638d0b81a1ba8377a7852d41b5bbe',
    'events' : '0xb71464588fc19165cbdd1e6e8150c40df544467b',
    'expiringEvents' : '0x61d90fd4c1c3502646153003ec4d5c177de0fb58',
    'fxpFunctions' : '0xdaf26192091449d14c03026f79272e410fce0908',
    'markets' : '0x2303f6b69e1d7662320819af027d88a9e350ebfb',
    'reporting' : '0xead0c9a9bd9546f476337a79e3d9bc8875241e61',
    'createEvent' : '0xcae6d5912033d66650894e2ae8c2f7502eaba15c',
    'createMarket' : '0x0568c631465eca542affb4bd3c72d1d2ee222c06',
    'checkQuorum' : '0x4eaa7a8b00107bbc11909e327e163b067fd3cfb9',
    'buy&sellShares' : '0xb8555091be5c8b8fc77449bb203717959079c29a',
    'createBranch' : '0x00298dd4fcae1b6063e963048716aeeed853edb6',
    'sendReputation' : '0x049487d32b727be98a4c8b58c4eab6521791f288',
    'transferShares' : '0x78da82256f5775df22eee51096d27666772b592d',
    'makeReports' : '0x32bfb5724874b209193aa0fca45b1f337b27e9b5',
    'dispatch' : '0x662f95de5a6c500de0b35b73f4b48d740d267482',
}

def get_sym(arg):
    if type(arg) in (int, long):
        return 'i'
    if type(arg) == list:
        return 'a'
    else:
        return 's'

def safe_eval(thing):
    try:
        return eval(thing)
    except:
        return thing

if __name__ == '__main__':
    c = contracts[sys.argv[1]]
    func = sys.argv[2]
    args = map(safe_eval, sys.argv[3:])
    sig = reduce(lambda a, b: a+get_sym(b), args, '')
    data = abi_data(func, sig, args)

    rpc = GethRPC()
    coinbase = rpc.eth_coinbase()['result']
    result = rpc.eth_sendTransaction(
        sender=coinbase, gas=hex(3000000), to=c, data=data)
    rpc.eth_getTransactionByHash(result['result'])
    rpc.eth_call('pending', sender=coinbase, gas=hex(3000000), to=c, data=data)