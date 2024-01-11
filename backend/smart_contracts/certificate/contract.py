from pyteal import *

def nft_contract(receiver, reference_program, approval_program, clear_program):
    is_creator = Txn.sender() == Global.creator_address()
    is_close_to_creator = Txn.close_remainder_to() == Global.creator_address()

    on_creation = And(
        Txn.application_args.length() == Int(0),
        Txn.asset_total() == Int(1),
        Txn.asset_sender() == Global.creator_address(),
        Txn.asset_close_to() == Global.creator_address(),
        Gtxn[0].type_enum() == TxnType.AssetConfig,
        Gtxn[0].xfer_asset() == Int(0),
        Gtxn[0].asset_sender() == Global.creator_address(),
        Gtxn[0].asset_close_to() == Global.creator_address(),
        Gtxn[1].type_enum() == TxnType.AssetTransfer,
        Gtxn[1].xfer_asset() == Int(0),
        Gtxn[1].asset_sender() == Global.creator_address(),
        Gtxn[1].asset_close_to() == Global.creator_address(),
    )

    transfer_check = And(
        Gtxn[0].asset_sender() == Global.creator_address(),
        Gtxn[0].asset_close_to() == Global.creator_address(),
        Gtxn[1].asset_receiver() == Global.creator_address(),
    )

    on_transfer = And(
        Gtxn[0].type_enum() == TxnType.AssetTransfer,
        Gtxn[0].asset_amount() == Int(1),
        Gtxn[0].asset_close_to() == Global.creator_address(),
        Gtxn[1].type_enum() == TxnType.Payment,
        Gtxn[2].type_enum() == TxnType.Payment,
        Gtxn[1].amount() == Int(0),
        Gtxn[2].amount() == Int(0),
        transfer_check
    )

    return Cond(
        [on_creation, Seq([App.localPut(Int(0), Bytes("reference_program"), reference_program),
                          App.localPut(Int(0), Bytes("approval_program"), approval_program),
                          App.localPut(Int(0), Bytes("clear_program"), clear_program),
                          App.localPut(Int(0), Bytes("owner"), receiver),
                          App.localPut(Int(0), Bytes("freeze"), Int(0)),
                          Return(Int(1))])],
        [on_transfer, App.localGet(Int(0), Bytes("freeze")) == Int(0)],
        [is_creator, Int(1)],
        [is_close_to_creator, Int(1)],
        [Txn.close_remainder_to() == Global.creator_address(), Int(1)],
        [And(Txn.close_remainder_to() == Global.creator_address(),
             Gtxn[0].asset_close_to() == Global.creator_address()), Int(1)],
        [Else(), Int(0)]
    )

# Example parameters for creating the contract
creator_address = "YOUR_CREATOR_ADDRESS"
reference_program = "REFERENCE_PROGRAM_HASH"
approval_program = "APPROVAL_PROGRAM_HASH"
clear_program = "CLEAR_PROGRAM_HASH"

# Compile the contract
compiled_contract = compileTeal(nft_contract(creator_address, reference_program, approval_program, clear_program), mode=Mode.Application)

# Print the compiled contract
print(compiled_contract.to_json())
