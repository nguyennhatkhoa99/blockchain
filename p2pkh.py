from bitcoin import *
from bitcoin.core import b2x, lx, CMutableTxIn, CMutableTxOut, COutPoint, CMutableTransaction, Hash160, COIN
from bitcoin.wallet import CBitcoinSecret, CBitcoinAddress
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH
from bitcoin.core.script import CScript, OP_CHECKSIG, OP_DUP, OP_HASH160, OP_EQUALVERIFY, SignatureHash
from os import urandom


def main(n, amount):
    SelectParams('testnet')
    private_key1 = CBitcoinSecret.from_secret_bytes(urandom(n))

    public_key1 = private_key1.pub

    # address = P2PKHBitcoinAddress.from_pubkey(public_key1)
    # print(b2x(address))

    # Create a transaction input (UTXO)
    txid = lx('bff785da9f8169f49be92fa95e31f0890c385bfb1bd24d6b94d7900057c617ae')
    output_index = 0
    txin = CMutableTxIn(COutPoint(txid, output_index))

    # Create a transaction output to the desired destination

    destination_address = CBitcoinAddress('1C7zdTfnkzmr13HfA2vNm5SJYRK6nEKyq8').to_scriptPubKey()
    amount = amount*COIN
    txout = CMutableTxOut(amount, destination_address)

    tx = CMutableTransaction([txin], [txout])

    sig_script = CScript([
        OP_DUP, 
        OP_HASH160, 
        Hash160(public_key1), 
        OP_EQUALVERIFY, 
        OP_CHECKSIG
    ])
    sighash = VerifyScript(txin.scriptSig, sig_script, tx, 0, (SCRIPT_VERIFY_P2SH,))

    print(b2x(tx.serialize()))

if __name__ == "__main__":
    main()