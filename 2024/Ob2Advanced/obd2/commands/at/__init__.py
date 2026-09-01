from ...OBDMain import Command, CommandReturn, ReturnType
from ...ELMCommand import ELMCommand, ELMReturnType, ELMVoltage



E = ELMCommand(
    "E",
    ELMReturnType(),
    description="Echo on/off"
)

RV = ELMCommand(
    "RV", 
    ELMVoltage(),
    description="Read voltage."
)

AL = ELMCommand(
    "AL",
    ELMReturnType(),
    description="Allow long messagges"
)

H = ELMCommand(
    "H",
    ELMReturnType(),
    description="Headers on or off",
    space=False
)

SH = ELMCommand(
    "SH",
    ELMReturnType(),
    description="Set header"
)

SP = ELMCommand(
    "SP",
    ELMReturnType(),
    description="Set protool"
)

ST = ELMCommand(
    "ST",
    ELMReturnType(),
    description="Set timeout"
)

TA = ELMCommand(
    "TA",
    ELMReturnType(),
    description="Set tester address"
)

CEA = ELMCommand(
    "CEA",
    ELMReturnType(),
    description="Turn off can extended addressing"
)

CAF = ELMCommand(
    "CAF",
    ELMReturnType(),
    description="Automatic formating",
    space=False
)

CF = ELMCommand(
    "CF",
    ELMReturnType(),
    description="Set the ID filter",
)

CFC = ELMCommand(
    "CFC",
    ELMReturnType(),
    description="Flow control on or off",
    space=False
)

CP = ELMCommand(
    "CP",
    ELMReturnType(),
    description="Set can priority"
)

CRA = ELMCommand(
    "CRA",
    ELMReturnType(),
    description="Set CAN recieve address",
)

CSM = ELMCommand(
    "CSM",
    ELMReturnType(),
    description="Silent monitoring on/off",
    space=False
)

D = ELMCommand(
    "D",
    ELMReturnType(),
    description="Display of the DLC off or on",
    space=False
)

FCSM = ELMCommand(
    "FC SM",
    ELMReturnType(),
    description="Set flow control mode"
)

FCSH = ELMCommand(
    "FC SH",
    ELMReturnType(),
    description="Set flow control header"
)

FCSD = ELMCommand(
    "FC SD",
    ELMReturnType(),
    description="Set flow control data"
)