from web3 import Web3
import json
from django.conf import settings

# Ganache EC2 서버 URL
ganache_url = "http://13.211.77.105:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# 배포된 컨트랙트 주소
# contract_address = "#####################################"
contract_address = getattr(settings, "CONTRACT_ADDRESS")


# ABI 로드
abi = [
  {
    "inputs": [],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "anonymous": False,
    "inputs": [
      {
        "indexed": True,
        "internalType": "string",
        "name": "registrationHash",
        "type": "string"
      },
      {
        "indexed": False,
        "internalType": "string",
        "name": "frameNumber",
        "type": "string"
      }
    ],
    "name": "BicycleRegistered",
    "type": "event"
  },
  {
    "anonymous": False,
    "inputs": [
      {
        "indexed": True,
        "internalType": "string",
        "name": "registrationHash",
        "type": "string"
      },
      {
        "indexed": False,
        "internalType": "string",
        "name": "cid",
        "type": "string"
      }
    ],
    "name": "InsuranceHistoryAdded",
    "type": "event"
  },
  {
    "anonymous": False,
    "inputs": [
      {
        "indexed": True,
        "internalType": "string",
        "name": "registrationHash",
        "type": "string"
      },
      {
        "indexed": False,
        "internalType": "string",
        "name": "oldOwnerId",
        "type": "string"
      },
      {
        "indexed": False,
        "internalType": "string",
        "name": "newOwnerId",
        "type": "string"
      },
      {
        "indexed": False,
        "internalType": "string",
        "name": "newOwnerContact",
        "type": "string"
      }
    ],
    "name": "OwnershipTransferred",
    "type": "event"
  },
  {
    "anonymous": False,
    "inputs": [
      {
        "indexed": True,
        "internalType": "string",
        "name": "registrationHash",
        "type": "string"
      },
      {
        "indexed": False,
        "internalType": "string",
        "name": "cid",
        "type": "string"
      }
    ],
    "name": "RepairHistoryAdded",
    "type": "event"
  },
  {
    "anonymous": False,
    "inputs": [
      {
        "indexed": True,
        "internalType": "string",
        "name": "registrationHash",
        "type": "string"
      },
      {
        "indexed": False,
        "internalType": "string",
        "name": "cid",
        "type": "string"
      }
    ],
    "name": "ReplacementHistoryAdded",
    "type": "event"
  },
  {
    "anonymous": False,
    "inputs": [
      {
        "indexed": True,
        "internalType": "string",
        "name": "registrationHash",
        "type": "string"
      },
      {
        "indexed": False,
        "internalType": "bool",
        "name": "isStolen",
        "type": "bool"
      }
    ],
    "name": "TheftReported",
    "type": "event"
  },
  {
    "anonymous": False,
    "inputs": [
      {
        "indexed": True,
        "internalType": "string",
        "name": "registrationHash",
        "type": "string"
      },
      {
        "indexed": False,
        "internalType": "string",
        "name": "cid",
        "type": "string"
      }
    ],
    "name": "TuningHistoryAdded",
    "type": "event"
  },
  {
    "inputs": [
      {
        "internalType": "string",
        "name": "regHash",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "cid",
        "type": "string"
      },
      {
        "internalType": "uint256",
        "name": "customTimestamp",
        "type": "uint256"
      }
    ],
    "name": "addInsuranceHistory",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "string",
        "name": "regHash",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "cid",
        "type": "string"
      },
      {
        "internalType": "uint256",
        "name": "customTimestamp",
        "type": "uint256"
      }
    ],
    "name": "addRepairHistory",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "string",
        "name": "regHash",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "cid",
        "type": "string"
      },
      {
        "internalType": "uint256",
        "name": "customTimestamp",
        "type": "uint256"
      }
    ],
    "name": "addReplacementHistory",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "string",
        "name": "regHash",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "cid",
        "type": "string"
      },
      {
        "internalType": "uint256",
        "name": "customTimestamp",
        "type": "uint256"
      }
    ],
    "name": "addTuningHistory",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "admin",
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getAllRegisteredFrameNumbers",
    "outputs": [
      {
        "internalType": "string[]",
        "name": "",
        "type": "string[]"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "string",
        "name": "regHash",
        "type": "string"
      }
    ],
    "name": "getBicycleBasicInfo",
    "outputs": [
      {
        "internalType": "string",
        "name": "frameNumber",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "manufacturer",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "model",
        "type": "string"
      },
      {
        "internalType": "uint256",
        "name": "purchaseDate",
        "type": "uint256"
      },
      {
        "internalType": "uint16",
        "name": "manufactureYear",
        "type": "uint16"
      },
      {
        "internalType": "uint256",
        "name": "registrationDate",
        "type": "uint256"
      },
      {
        "internalType": "string",
        "name": "ownerId",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "ownerName",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "ownerRRNFront",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "ownerContact",
        "type": "string"
      },
      {
        "internalType": "bool",
        "name": "stolen",
        "type": "bool"
      },
      {
        "internalType": "uint16",
        "name": "weight",
        "type": "uint16"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "string",
        "name": "regHash",
        "type": "string"
      }
    ],
    "name": "getInsuranceHistory",
    "outputs": [
      {
        "components": [
          {
            "internalType": "string",
            "name": "cid",
            "type": "string"
          },
          {
            "internalType": "uint256",
            "name": "timestamp",
            "type": "uint256"
          }
        ],
        "internalType": "struct BicycleRegistry.HistoryItem[]",
        "name": "",
        "type": "tuple[]"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "string",
        "name": "regHash",
        "type": "string"
      }
    ],
    "name": "getOwnershipHistory",
    "outputs": [
      {
        "components": [
          {
            "internalType": "string",
            "name": "newOwnerId",
            "type": "string"
          },
          {
            "internalType": "string",
            "name": "newOwnerName",
            "type": "string"
          },
          {
            "internalType": "string",
            "name": "newOwnerRRNFront",
            "type": "string"
          },
          {
            "internalType": "string",
            "name": "newOwnerContact",
            "type": "string"
          },
          {
            "internalType": "uint256",
            "name": "timestamp",
            "type": "uint256"
          }
        ],
        "internalType": "struct BicycleRegistry.OwnershipTransfer[]",
        "name": "",
        "type": "tuple[]"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "string",
        "name": "frameNumber",
        "type": "string"
      }
    ],
    "name": "getRegistrationHash",
    "outputs": [
      {
        "internalType": "string",
        "name": "",
        "type": "string"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "string",
        "name": "regHash",
        "type": "string"
      }
    ],
    "name": "getRepairHistory",
    "outputs": [
      {
        "components": [
          {
            "internalType": "string",
            "name": "cid",
            "type": "string"
          },
          {
            "internalType": "uint256",
            "name": "timestamp",
            "type": "uint256"
          }
        ],
        "internalType": "struct BicycleRegistry.HistoryItem[]",
        "name": "",
        "type": "tuple[]"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "string",
        "name": "regHash",
        "type": "string"
      }
    ],
    "name": "getReplacementHistory",
    "outputs": [
      {
        "components": [
          {
            "internalType": "string",
            "name": "cid",
            "type": "string"
          },
          {
            "internalType": "uint256",
            "name": "timestamp",
            "type": "uint256"
          }
        ],
        "internalType": "struct BicycleRegistry.HistoryItem[]",
        "name": "",
        "type": "tuple[]"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "string",
        "name": "regHash",
        "type": "string"
      }
    ],
    "name": "getTuningHistory",
    "outputs": [
      {
        "components": [
          {
            "internalType": "string",
            "name": "cid",
            "type": "string"
          },
          {
            "internalType": "uint256",
            "name": "timestamp",
            "type": "uint256"
          }
        ],
        "internalType": "struct BicycleRegistry.HistoryItem[]",
        "name": "",
        "type": "tuple[]"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "string",
        "name": "frameNumber",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "manufacturer",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "model",
        "type": "string"
      },
      {
        "internalType": "uint256",
        "name": "purchaseDate",
        "type": "uint256"
      },
      {
        "internalType": "uint16",
        "name": "manufactureYear",
        "type": "uint16"
      },
      {
        "internalType": "string",
        "name": "ownerId",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "ownerName",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "ownerRRNFront",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "ownerContact",
        "type": "string"
      },
      {
        "internalType": "uint16",
        "name": "weight",
        "type": "uint16"
      }
    ],
    "name": "registerBicycle",
    "outputs": [
      {
        "internalType": "string",
        "name": "",
        "type": "string"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "string",
        "name": "regHash",
        "type": "string"
      },
      {
        "internalType": "bool",
        "name": "stolen",
        "type": "bool"
      }
    ],
    "name": "reportStolen",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "string",
        "name": "regHash",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "newOwnerId",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "newOwnerName",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "newOwnerRRNFront",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "newOwnerContact",
        "type": "string"
      },
      {
        "internalType": "uint256",
        "name": "customTimestamp",
        "type": "uint256"
      }
    ],
    "name": "transferOwnership",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  }
]




# 컨트랙트 인스턴스 생성
contract_instance = web3.eth.contract(address=contract_address, abi=abi)

# 연결 확인
print("Ganache Connected:", web3.is_connected())