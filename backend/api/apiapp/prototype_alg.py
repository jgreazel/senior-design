import json
import sys


class Scenario:
    """
    A class used to represent an attack scenario

    Attributes
    ----------
    probabilty : float
        probability of scenario occurring, 0-1
    nodeKeys : [str]
        list of node keys, each key represented by a string

    Methods
    -------
    combine(scenario2)
        Combines scenario2 with self
    """

    def __init__(self, probability, nodeKeys):
        """
        Initializes a scenario with the given probability and nodeKeys.

        Parameters
        ----------
        probability : float?
            The scenario's probability of occurring
        nodeKeys : [str]
            The list of nodes in the scenario
        """
        self.probability = float(probability)
        self.nodeKeys = nodeKeys
    '''
    def __str__(self):
        """Returns nodes in scenario"""
        # TODO: Check output with deeper tree
        risk = str(round(float(treeRoot["impact"]) * self.probability, 4))
        prob = str(round(self.probability, 4))
        output = "risk: " + risk + "  \tprob: " + prob + "\t: "
        for key in self.nodeKeys:
            output += key + " "
        return output
    '''
    def toDict(self,treeRoot,nodesList):
        """Returns dictionary representation of scenario"""
        risk = round(float(treeRoot["impact"]) * self.probability, 4)
        prob = round(self.probability, 4)
        leafKeys = self.nodeKeys
        keyTextPairs = []
        for key in leafKeys:
          node = findNode(key,nodesList)
          keyTextPairs.append([key, node["text"]])
        dit = {
          "risk" : risk,
          "probability" : prob,
          "leafKeys" : keyTextPairs
        }
        return dit

    def combine(self, scenario2):
        """
        Combine scenarios. Used in AND nodes.

        Parameters
        ----------
        scenario2 : Scenario
            The scenario to combine
        """
        prob = self.probability * scenario2.probability
        keys = list(())
        for key in self.nodeKeys:
            keys.append(key)
        for key in scenario2.nodeKeys:
            keys.append(key)
        return Scenario(prob, keys)

def normalize(nodesList):
    """
    Normalizes probabilty of attacks in nodeList to sum to 1
    """
    sum = 0.0
    for node in nodesList:
        if node["key"][0] == "L" or node["key"][0] == "S":
            sum += float(node["probability"])
    for node in nodesList:
      if node["key"][0] == "L":
        node["probability"] = float(node["probability"]) / sum


def findRoot(nodesList,edgesList):
    """Find root node."""
    root = None
    for n in nodesList:
        hasParent = False
        # Check if node exists as a destination in edge list
        for e in edgesList:
            if e["to"] == n["key"]:
                hasParent = True
                break
        if not hasParent:
            root = n
            break
    if root is None:
        print("Error:: Cannot find root node")
    return root

def findAttackRoot(root,edgesList,nodesList):
    """
    Find root node of attack tree (that does not include safe path node).
    
    Parameters
        ----------
        root : Node (list)
            Root of tree
    """
    children = findChildren(root,edgesList,nodesList)
    for node in children:
      if node["key"][0] != "S":
        return node
    print("Error:: Cannot find attack root node")
    return root


def findNode(key,nodesList):
    """
    Finds the node with the given key.
    
    Parameters
    ----------
    key : str
        Key of node to find
    """
    for node in nodesList:
        if node["key"] == key:
            return node
    print("Error:: Could not find node with given key")


def findChildren(node,edgesList,nodesList):
    """
    Searches edge list to find all children of given node.
    
    Parameters
    ----------
    node : Node
        Node to find children of
    """
    children = list(())
    for e in edgesList:
        if e["from"] == node["key"]:
            children.append(findNode(e["to"],nodesList))
    return children


def findScenarios(node,edgesList,nodesList):
    """
    Recusive function for finding all scenarios from a given node.
    
    Parameters
    ----------
    node : Node
        Node to find scenarios of
    """
    if node["key"][0] == "L":  # If leaf node
        scenarioList = list(())
        scenarioList.append(Scenario(node["probability"], [node["key"]]))
        return scenarioList
    elif node["key"][0] == "O":  # If OR node
        scenarioList = list(())
        children = findChildren(node,edgesList,nodesList)
        for child in children:
            childScenarios = findScenarios(child,edgesList,nodesList)
            for scenario in childScenarios:
                scenarioList.append(scenario)
        return scenarioList
    elif node["key"][0] == "A":  # If AND node
        scenarioList = list(())
        tempList = list(())
        childLists = list(())  # List of lists
        children = findChildren(node,edgesList,nodesList)
        for child in children:  # Create list of child scenario lists
            childLists.append(findScenarios(child,edgesList,nodesList))
        scenarioList = childLists[0]
        for i in range(1, len(childLists)):  # Compare all combinations of scenarios
            for scenario1 in scenarioList:
                for scenario2 in childLists[i]:
                    tempList.append(scenario1.combine(scenario2))
            scenarioList = tempList
            tempList = list(())
        return scenarioList
    else:
        print("Error:: Could not determine node type")


# Get object from JSON to List
jsonObj = """
{
  "nodeData": [
    {
      "key": "OR3",
      "text": "placeholderText",
      "riskIndex": "0",
      "impact": "450",
      "color": "red",
      "shape": "andgate"
    },
    {
      "key": "LEAF5",
      "text": "safePath",
      "riskIndex": "8"
    },
    {
      "key": "AND",
      "text": "placeholderText",
      "riskIndex": "0",
      "color": "red",
      "shape": "andgate"
    },
    {
      "key": "OR",
      "text": "placeholderText",
      "riskIndex": "0",
      "color": "lightgreen",
      "shape": "orgate"
    },
    {
      "key": "LEAF",
      "text": "cyberAttack",
      "riskIndex": "1.1"
    },
    {
      "key": "LEAF2",
      "text": "physicalAttack",
      "riskIndex": "8.3"
    },
    {
      "key": "OR2",
      "text": "placeholderText",
      "riskIndex": "0",
      "color": "lightgreen",
      "shape": "orgate"
    },
    {
      "key": "LEAF3",
      "text": "phishingAttack",
      "riskIndex": "7.2"
    },
    {
      "key": "LEAF4",
      "text": "spyware",
      "riskIndex": "3.4"
    }
  ],
  "edgeData": [
    {
      "from": "OR3",
      "to": "AND",
      "fromPort": "b",
      "toPort": "t",
      "key": -7
    },
    {
      "from": "OR3",
      "to": "LEAF5",
      "fromPort": "b",
      "toPort": "t",
      "key": -8
    },
    {
      "from": "AND",
      "to": "OR",
      "fromPort": "b",
      "toPort": "t",
      "key": -1
    },
    {
      "from": "OR",
      "to": "LEAF",
      "fromPort": "b",
      "toPort": "t",
      "key": -2
    },
    {
      "from": "OR",
      "to": "LEAF2",
      "fromPort": "b",
      "toPort": "t",
      "key": -3
    },
    {
      "from": "AND",
      "to": "OR2",
      "fromPort": "b",
      "toPort": "t",
      "key": -4
    },
    {
      "from": "OR2",
      "to": "LEAF3",
      "fromPort": "b",
      "toPort": "t",
      "key": -5
    },
    {
      "from": "OR2",
      "to": "LEAF4",
      "fromPort": "b",
      "toPort": "t",
      "key": -6
    }
  ]
}
"""
# jsonData = json.loads(jsonObj)

# nodesList = jsonData["nodeData"]
# edgesList = jsonData["edgeData"]

# normalize()

# treeRoot = findRoot()
# attackRoot = findAttackRoot(treeRoot)

# scenarios = findScenarios(attackRoot)

# scenList = []
# for scen in scenarios:
#     scenList.append(scen.toDict())

# sendToFrontendJson = json.dumps(scenList)
# print(sendToFrontendJson)

def api_request(frontend_json):
    jsonData = json.loads(frontend_json)

    nodesList = jsonData["nodeData"]
    edgesList = jsonData["edgeData"]

    normalize(nodesList)

    treeRoot = findRoot(nodesList,edgesList)
    attackRoot = findAttackRoot(treeRoot,edgesList,nodesList)

    scenarios = findScenarios(attackRoot,edgesList,nodesList)

    scenList = []
    if(scenarios != None):
      for scen in scenarios:
          scenList.append(scen.toDict(treeRoot,nodesList))

    sendToFrontendJson = json.dumps(scenList)
    return sendToFrontendJson