from typing import Union, Dict

GenericSchema = Dict[str, Union[str, float, int]]

PurchaseSchema: GenericSchema = {
    'ean': int,
    'price': float,
    'store': int,
    'dateTime': str
}