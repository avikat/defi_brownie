from decimal import Decimal
from brownie import Contract, accounts,network,config,MockV3Aggregator,VRFCoordinatorMock,LinkToken,interface,MockOracle,MockERC20,MockDAI,MockWETH
from web3 import Web3
FORKED_LOCAL_ENVIROMENTS=["mainnet-fork","mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIROMENTS = ["development","ganache-local"]

def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)

    if(network.show_active() in LOCAL_BLOCKCHAIN_ENVIROMENTS or network.show_active() in FORKED_LOCAL_ENVIROMENTS):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])



contract_to_mock = {"eth_usd_price_feed": MockV3Aggregator,
                    "fau_token":MockDAI,
                    "weth_token": MockWETH,
                    "dai_usd_price_feed":MockV3Aggregator
}


def get_contract(contract_name):
    # """"This function will grab the address and give us project
    # """
    contract_type = contract_to_mock[contract_name]


    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        if len(contract_type) <=0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]

        contract=Contract.from_abi(contract_type._name,contract_address,contract_type.abi)
    return contract
     

DECIMALS =18
INITIAL_VALUE=2000000000000000000000

def deploy_mocks(decimals=DECIMALS,initial_value=INITIAL_VALUE):
    account=get_account()
    mock_price_feed = MockV3Aggregator.deploy(decimals,initial_value,{"from":account})
    print("Deploying Mock DAI ")
    dai_token=MockDAI.deploy({"from":account})
    print(f"Deployed to {dai_token.address}")
    print ("Deploying Mock Weth")
    weth_token=MockWETH.deploy({"from":account})
    print(f"Deployed to {weth_token.address}")
   
    print("deployed!")


def fund_with_link(contract_address,account=None,link_token=None,amount=100000000000000000):
    account = account if account else get_account()
    link_token=link_token if link_token else get_contract("link_token")
    # link_token_contract= interface.LinkTokenInterface(link_token.address)
    # tx=link_token_contract.transfer(contract_address,amount)
    tx=link_token.transfer(contract_address,amount,{"from" : account})

    tx.wait(1)
    print("Fund Transfer")
    return tx
