import logging
import math

logging.basicConfig(level='DEBUG')
logger = logging.getLogger('utils')


def calculate(a: float, b: float, operation: str) -> float:
    match operation:
        case "+":
            return _addition(a, b)
        case "-":
            return _subtraction(a, b)
        case "*":
            return _multiplication(a, b)
        case "/":
            return _division(a, b)
        case "^":
            return _pow(a, b)
        case _:
            logger.error('Некорректная операция.')


def _addition(a: float, b: float) -> float:
    try:
        result: float = a + b
        logger.debug(f'{a} + {b} = {result}')
        return result
    except Exception as e:
        logger.error(e)


def _subtraction(a: float, b: float) -> float:
    try:
        result: float = a - b
        logger.debug(f'{a} - {b} = {result}')
        return result
    except Exception as e:
        logger.error(e)


def _multiplication(a: float, b: float) -> float:
    try:
        result: float = a * b
        logger.debug(f'{a} * {b} = {result}')
        return result
    except Exception as e:
        logger.error(e)


def _division(a: float, b: float) -> float:
    try:
        result: float = a / b
        logger.debug(f'{a} / {b} = {result}')
        return result
    except Exception as e:
        logger.error(e)


def _pow(a: float, b: float) -> float:
    try:
        result: float = math.pow(a, b)
        logger.debug(f'{a} ^ {b} = {result}')
        return result
    except Exception as e:
        logger.error(e)
