from dataclasses import dataclass

@dataclass
class Props:
    name: str
    bot: bool = False
    diff: tuple = None
    score: int = 0
    center: int = 100
    lose: int = -3
    darts: int = 3
    target_type: str = 'score'
    target: int = 500
    coeff: float = 1
    exponent: float = 1
    autoskip: bool = False
    antidartz: bool = False
