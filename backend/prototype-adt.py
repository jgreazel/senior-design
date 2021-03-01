import json
import sys
import nashpy as nash


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

    def __init__(self, probability, impact, nodeKeys):
        """
        Initializes a scenario with the given probability and nodeKeys.

        Parameters
        ----------
        probability : float?
            The scenario's probability of occurring
        impact : float?
            The scenario's impact
        nodeKeys : [str]
            The list of nodes in the scenario
        """
        self.probability = float(probability)
        self.impact = float(impact)
        self.nodeKeys = nodeKeys

    def __str__(self):
        """Returns nodes in scenario"""
        # TODO: Check output with deeper tree
        risk = str(round(self.impact * self.probability, 3))
        prob = str(round(self.probability, 4))
        impact = str(round(self.impact, 2))
        output = (
            "risk: " + risk + "  \tprob: " + prob + "  \timpact: " + impact + "\t: "
        )
        for key in self.nodeKeys:
            output += key + " "
        return output

    def get_cost(self):
        cost = self.probability * self.impact
        return cost

    def combine(self, scenario2):
        """
        Combine scenarios. Used in AND nodes.

        Parameters
        ----------
        scenario2 : Scenario
            The scenario to combine
        """
        prob = self.probability * scenario2.probability
        impact = self.impact + scenario2.impact
        keys = list(())
        for key in self.nodeKeys:
            keys.append(key)
        for key in scenario2.nodeKeys:
            keys.append(key)
        return Scenario(prob, impact, keys)


def normalize():
    """
    Normalizes probabilty of attacks in nodeList to sum to 1
    """
    sum = 0.0
    for node in nodesList:
        if node["key"][0] == "L":
            sum += float(node["riskIndex"])
    for node in nodesList:
        if node["key"][0] == "L":
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


def findAttackRoot():
    """Find root node of attack tree (that does not include safe path node)."""
    root = findRoot()
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
    Recursive function for finding all scenarios from a given node.

    Parameters
    ----------
    node : Node
        Node to find scenarios of
    """
    if node["key"][0] == "L":  # If leaf node
        scenarioList = list(())
        defenseList = list(())
        scenarioList.append(Scenario(node["riskIndex"], node["impact"], [node["key"]]))
        defense = findChildren(node)
        if len(defense) > 0:
            defenseList.append(
                Scenario(
                    defense[0]["riskIndex"], defense[0]["impact"], [defense[0]["key"]]
                )
            )
        return scenarioList, defenseList
    elif node["key"][0] == "O":  # If OR node
        scenarioList = list(())
        defenseList = list(())

        tempList = list(())
        childDefenseLists = list(())

        children = findChildren(node)
        for child in children:
            childScenarios, childDefenses = findScenarios(child)
            childDefenseLists.append(childDefenses)
            for scenario in childScenarios:
                scenarioList.append(scenario)
        defenseScenarioList = childDefenseLists[0]
        for i in range(
            1, len(childDefenseLists)
        ):  # Compare all combinations of scenarios
            for scenario1 in defenseScenarioList:
                for scenario2 in childDefenseLists[i]:
                    tempList.append(scenario1.combine(scenario2))
            defenseList = tempList
            tempList = list(())
        return scenarioList, defenseList
    elif node["key"][0] == "A":  # If AND node
        scenarioList = list(())
        defenseList = list(())

        tempList = list(())
        childLists = list(())  # List of lists

        children = findChildren(node)
        for child in children:  # Create list of child scenario lists
            childScenarios, childDefenses = findScenarios(child)
            childLists.append(childScenarios)
            for defense in childDefenses:
                defenseList.append(defense)
        scenarioList = childLists[0]
        for i in range(1, len(childLists)):  # Compare all combinations of scenarios
            for scenario1 in scenarioList:
                for scenario2 in childLists[i]:
                    tempList.append(scenario1.combine(scenario2))
            scenarioList = tempList
            tempList = list(())
        return scenarioList, defenseList
    else:
        print("Error:: Could not determine node type")


def nasheq(impact, attack_costs, defense_costs):
    """
    Computes the nash equilibrium for the given impacts, attack costs,
    and defense costs. Currently expects 1D parameters of equal length.

    Returns an equilibria generator.
    """
    payoff_attacker = []
    for i in range(len(attack_costs)):
        payoff_row = []
        for j in range(len(defense_costs)):
            payoff_row.append(defense_costs[j] + impact - attack_costs[i])
        payoff_attacker.append(payoff_row)

    game = nash.Game(payoff_attacker)
    eqs = game.support_enumeration(non_degenerate=False, tol=0)
    return eqs


# Get object from JSON to List
jsonObj = """
{
    "nodeData": [
        {
            "key": "OR3",
            "text": "placeholderText",
            "riskIndex": "0",
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
            "impact": "89"
        },
        {
            "key": "LEAF2",
            "text": "physicalAttack",
            "riskIndex": "8.3",
            "impact": "11"
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
            "impact": "231"
        },
        {
            "key": "LEAF4",
            "text": "spyware",
            "riskIndex": "3.4",
            "impact": "20"
        },
        {
            "key": "DEFENSE3",
            "text": "Defense 3",
            "riskIndex": "1",
            "impact": "4"
        },
        {
            "key": "DEFENSE4",
            "text": "Defense 4",
            "riskIndex": "1",
            "impact": "5"
        },
        {
            "key": "DEFENSE2",
            "text": "Defense 2",
            "riskIndex": "1",
            "impact": "3"
        },
        {
            "key": "DEFENSE1",
            "text": "Defense 1",
            "riskIndex": "1",
            "impact": "6.1"
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
        },
        {
            "from": "LEAF4",
            "to": "DEFENSE4",
            "fromPort": "b",
            "toPort": "t",
            "key": -7
        },
        {
            "from": "LEAF3",
            "to": "DEFENSE3",
            "fromPort": "b",
            "toPort": "t",
            "key": -7
        },
        {
            "from": "LEAF2",
            "to": "DEFENSE2",
            "fromPort": "b",
            "toPort": "t",
            "key": -8
        },
        {
            "from": "LEAF",
            "to": "DEFENSE1",
            "fromPort": "b",
            "toPort": "t",
            "key": -9
        }
    ]
}
"""
jsonData = json.loads(jsonObj)

nodesList = jsonData["nodeData"]
edgesList = jsonData["edgeData"]

normalize()

scenarios, defenses = findScenarios(findAttackRoot())
print(*scenarios, sep="\n")
print(*defenses, sep="\n")

attackCosts = [scenario.get_cost() for scenario in scenarios]
defenseCosts = [scenario.get_cost() for scenario in defenses]

eqs = nasheq(10, attackCosts, defenseCosts)
print(list(eqs))
