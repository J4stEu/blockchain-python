from app import app, bc
import models
import json


@app.route('/')
def index():
    if bc.is_system_initialized():
        return "<p>Blockchain instance is already initialized.</p>"
    else:
        return "<p>Blockchain is not initialized yet.</p>"


@app.route('/get_wallets')
def get_wallets():
    wallets_info = {}
    wallets, error = bc.get_wallets()
    if wallets in None and error != "":
        return {
            "error": error
        }
    wallets = bc.get_wallets()
    for address, wallet in wallets.items():
        acc = bc.get_balance(address, True)
        wallets_info[address] = {
            "wallet": bc.serialize_wallet(wallet),
            "balance": acc
        }
    return wallets_info


@app.route('/get_blocks')
def get_blocks():
    blocks = {}
    for block in bc.get_blocks():
        blocks[block.hash] = {
            "serializedBlock": block.serializedBlock,
            "txsRootNode": block.txsRootNode
        }
    return blocks


@app.route('/get_chainstate')
def get_chainstate():
    utxo = {}
    for serialized_utxo_item in bc.chain_state.get_utxo(False):
        utxo[serialized_utxo_item.txID] = {
            "serializedUnspentOutputs": serialized_utxo_item.serializedUnspentOutputs
        }
        pass
    return utxo


@app.route('/get_pool')
def get_pool():
    txs_pool = bc.get_all_pool()
    pool = {}
    for tx in txs_pool:
        pool[tx.txID] = {
            "fromAddr": tx.fromAddr,
            "toAddr": tx.toAddr,
            "amount": tx.amount,
            "serializedTransaction": tx.serializedTransaction,
            "error": tx.error,
            "errorText": tx.errorText
        }
    return pool
