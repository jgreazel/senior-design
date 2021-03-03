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

    def __init__(self, probability, cost, nodeKeys):
        """
        Initializes a scenario with the given probability and nodeKeys.

        Parameters
        ----------
        probability : float?
            The scenario's probability of occurring
        cost : float?
            The scenario's cost to defend
        nodeKeys : [str]
            The list of nodes in the scenario
        """
        self.probability = float(probability)
        self.cost = float(cost)
        self.nodeKeys = nodeKeys

    def __str__(self):
        """Returns nodes in scenario"""
        # TODO: Check output with deeper tree
        risk = str(round(float(treeRoot["impact"]) * self.probability, 3))
        prob = str(round(self.probability, 4))
        cost = str(round(self.cost, 2))
        output = "risk: " + risk + "  \tprob: " + prob + "  \tdcost: " + cost + "\t: "
        for key in self.nodeKeys:
            output += key + " "
        return output

    def combine(self, scenario2):
        """
        Combine scenarios. Used in AND nodes.

        Parameters
        ----------
        scenario2 : Scenario
            The scenario to combine
        """
        prob = self.probability * scenario2.probability
        cost = self.cost if self.cost < scenario2.cost else scenario2.cost
        keys = list(())
        for key in self.nodeKeys:
            keys.append(key)
        for key in scenario2.nodeKeys:
            keys.append(key)
        return Scenario(prob, cost, keys)

def normalize():
    """
    Normalizes probabilty of attacks in nodeList to sum to 1
    """
    sum = 0.0
    for node in nodesList:
        if node["key"][0] == "L":
            sum += float(node["riskIndex"])
    for node in nodesList:
        node["riskIndex"] = float(node["riskIndex"]) / sum


def findRoot():
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

def findAttackRoot(root):
    """
    Find root node of attack tree (that does not include safe path node).
    
    Parameters
        ----------
        root : Node (list)
            Root of tree
    """
    children = findChildren(root)
    for node in children:
      if node["key"][0] != "L":
        return node
    print("Error:: Cannot find attack root node")
    return root


def findNode(key):
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


def findChildren(node):
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
            children.append(findNode(e["to"]))
    return children


def findScenarios(node):
    """
    Recusive function for finding all scenarios from a given node.
    
    Parameters
    ----------
    node : Node
        Node to find scenarios of
    """
    if node["key"][0] == "L":  # If leaf node
        scenarioList = list(())
        scenarioList.append(Scenario(node["riskIndex"], node["cost"], [node["key"]]))
        return scenarioList
    elif node["key"][0] == "O":  # If OR node
        scenarioList = list(())
        children = findChildren(node)
        for child in children:
            childScenarios = findScenarios(child)
            for scenario in childScenarios:
                scenarioList.append(scenario)
        return scenarioList
    elif node["key"][0] == "A":  # If AND node
        scenarioList = list(())
        tempList = list(())
        childLists = list(())  # List of lists
        children = findChildren(node)
        for child in children:  # Create list of child scenario lists
            childLists.append(findScenarios(child))
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
      "riskIndex": "1.1",
      "cost": "89"
    },
    {
      "key": "LEAF2",
      "text": "physicalAttack",
      "riskIndex": "8.3",
      "cost": "11"
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
      "riskIndex": "7.2",
      "cost": "231"
    },
    {
      "key": "LEAF4",
      "text": "spyware",
      "riskIndex": "3.4",
      "cost": "20"
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
jsonData = json.loads(jsonObj)

nodesList = jsonData["nodeData"]
edgesList = jsonData["edgeData"]

normalize()

treeRoot = findRoot()
attackRoot = findAttackRoot(treeRoot)

scenarios = findScenarios(attackRoot)
print(*scenarios, sep="\n")
