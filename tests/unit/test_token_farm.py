from decimal import Decimal
from brownie import Contract, accounts,network,config,MockV3Aggregator,VRFCoordinatorMock,LinkToken,interface,MockOracle,MockERC20,MockDAI,MockWETH,exceptions
from scripts.helpful_scripts import get_account,get_contract,INITIAL_VALUE,DECIMALS
from web3 import Web3
import pytest
from scripts.deploy import deploy_token_farm_and_dapp_token

# amount_staked = Web3.toWei(1,"ether")

FORKED_LOCAL_ENVIROMENTS=["mainnet-fork","mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIROMENTS = ["development","ganache-local"]



def test_set_price_feed_contract():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    non_owner = get_account(index=1)
    token_farm,dapp_token = deploy_token_farm_and_dapp_token()
    # token_farm.setPriceFeedContract(dapp_token,get_contract("eth_usd_price_feed"),{"from":account})   

    assert token_farm.tokenPriceFeedMapping(dapp_token.address) == get_contract("eth_usd_price_feed")
    # assert token_farm.tokenPriceFeedMapping(get_contract("weth_token").address) == get_contract("eth_usd_price_feed") 
    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.setPriceFeedContract(dapp_token,get_contract("eth_usd_price_feed"),{"from":non_owner})     


def test_issue_tokens(amount_staked):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    token_farm,dapp_token = test_stake_tokens(amount_staked)
    starting_balance = dapp_token.balanceOf(account.address)
    token_farm.issueTokens({"from":account})

    assert dapp_token.balanceOf(account.address) == starting_balance +  INITIAL_VALUE


def test_stake_tokens(amount_staked):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    token_farm,dapp_token = deploy_token_farm_and_dapp_token()

    dapp_token.approve(token_farm.address,amount_staked,{"from":account})
    token_farm.stakeTokens(amount_staked,dapp_token.address,{"from":account})

    assert token_farm.stakingBalance(dapp_token.address,account.address) == amount_staked
    assert token_farm.uniqueTokenStaked(account.address) == 1
    assert token_farm.stakers(0) == account.address
    return token_farm, dapp_token

def test_get_token_value():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    token_farm,dapp_token = deploy_token_farm_and_dapp_token()
    assert token_farm.getTokenValue(dapp_token.address) == (INITIAL_VALUE,DECIMALS)

def test_unstake_tokens(amount_staked):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    token_farm,dapp_token = test_stake_tokens(amount_staked)

    token_farm.unstakeTokens(dapp_token.address,{"from":account})
    assert token_farm.stakingBalance(dapp_token.address,account.address) == 0
    assert token_farm.uniqueTokenStaked(account.address) == 0
    









        