from bitcoin import *
import requests
from bitcoin.core import b2x, lx, CMutableTxIn, CMutableTxOut, COutPoint, CMutableTransaction, Hash160, COIN, CTxIn, CTxOut, CTransaction
from bitcoin.wallet import CBitcoinSecret, CBitcoinAddress, P2PKHBitcoinAddress
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH, SIGHASH_ALL
from bitcoin.core.script import CScript, OP_CHECKSIG, OP_DUP, OP_HASH160, OP_EQUALVERIFY, SignatureHash
from os import urandom
import hashlib

def broadcast_transaction(tx: CMutableTransaction):
    raw_transaction = b2x(tx.serialize())
    headers = {
        'content-type': 'application/x-www-form-urlencoded'
    }
    return requests.post(
        'https://api.blockcypher.com/v1/btc/test3/txs/push',
        headers=headers,
        data='{"tx": "%s"}' % raw_transaction
    )
    

def main(amount):
    SelectParams('testnet')
    private_key = CBitcoinSecret('cN99D4zT194CypQTuMhrrsbjRNjRFJ25qwTSHammF7uUgF2k4wYz')

    public_key = private_key.pub

    address = P2PKHBitcoinAddress.from_pubkey(public_key)
    print(address)

    # Create a transaction input (UTXO)
    txid = lx('cd81a0931237a99a6bcf954f6dbb474f44c2eca990b688d28420c581b5837959')
    script_pubkey = CScript([OP_DUP, OP_HASH160, Hash160(private_key.pub), OP_EQUALVERIFY, OP_CHECKSIG])
    vout = CTxOut(nValue=amount* COIN, scriptPubKey=script_pubkey)
   
    # Create a transaction output to the desired destination
    message_hash = hashlib.sha256(public_key).digest()
    sig = private_key.sign(message_hash)
    scriptSig =  CScript([sig, public_key])
    vin = CTxIn(prevout=COutPoint(hash=txid, n=0), scriptSig=scriptSig)
    txn = CTransaction(vin=[vin], vout=[vout], nLockTime=2570597)

    print(b2x(txn.serialize()))

if __name__ == "__main__":
    main(0.00007000)
