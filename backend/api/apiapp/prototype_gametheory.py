import codecs, json
import sys
import nashpy as nash


class Scenario:
    """
    A class used to represent an attack scenario

    Attributes
    ----------
    probability : float
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
        probability : float
            The scenario's probability of occurring
        cost : float
            The scenario's cost
        nodeKeys : [str]
            The list of nodes in the scenario
        """
        self.probability = float(probability)
        self.cost = float(cost)
        self.nodeKeys = nodeKeys

    def __str__(self):
        """Returns nodes in scenario"""
        prob = str(round(self.probability, 4))
        cost = str(round(self.cost, 2))
        output = (
            "prob: "
            + prob
            + "  \tcost: "
            + cost
            + "\t: "
        )
        for key in self.nodeKeys:
            output += key + " "
        return output

    def get_cost(self):
        return self.cost

    def combine(self, scenario2):
        """
        Combine scenarios. Used in AND nodes.

        Parameters
        ----------
        scenario2 : Scenario
            The scenario to combine
        """
        prob = self.probability * scenario2.probability
        cost = self.probability * self.cost + scenario2.probability * scenario2.cost
        keys = list(())
        for key in self.nodeKeys:
            keys.append(key)
        for key in scenario2.nodeKeys:
            keys.append(key)
        return Scenario(prob, cost, keys)


def normalize(nodesList):
    """
    Normalizes probability of attacks in nodeList to sum to 1
    """
    sum = 0.0
    for node in nodesList:
        if node["key"][0] == "L":
            sum += float(node["probability"])
    for node in nodesList:
        if node["key"][0] == "L":
            node["probability"] = float(node["probability"]) / sum


def findRoot(nodesList):
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


def findAttackRoot(nodesList):
    """Find root node of attack tree (that does not include safe path node)."""
    root = findRoot(nodesList)
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
        scenarioList.append(Scenario(node["probability"], node["cost"], [node["key"]]))
        defense = findChildren(node)
        if len(defense) > 0:
            defenseList.append(
                Scenario(
                    1, defense[0]["cost"], [defense[0]["key"]]
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
    Computes the nash equilibrium for the given impact, attack costs,
    and defense costs.

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
        },
        {
            "key": "DEFENSE3",
            "text": "Defense 3",
            "riskIndex": "1",
            "cost": "42"
        },
        {
            "key": "DEFENSE4",
            "text": "Defense 4",
            "riskIndex": "1",
            "cost": "35"
        },
        {
            "key": "DEFENSE2",
            "text": "Defense 2",
            "riskIndex": "1",
            "cost": "32"
        },
        {
            "key": "DEFENSE1",
            "text": "Defense 1",
            "riskIndex": "1",
            "cost": "61"
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

jsonTest = """
{
"nodes": [{"key":"AND","color":"red","shape":"andgate"},{"key":"AND2","color":"red","shape":"andgate"},{"key":"LEAF","text":"LEAF1","probability":0.4,"cost":3},{"key":"LEAF2","text":"LEAF2","probability":0.2,"cost":10},{"key":"LEAF3","text":"LEAF3","probability":0.3,"cost":2},{"key":"LEAF4","text":"LEAF4","probability":0.1,"cost":5},{"key":"OR","color":"green","shape":"orgate"},{"key":"ROOT_NODE","text":"Root Node","color":"purple","shape":"orgate","impact":"0"},{"key":"SAFE_PATH","text":"Safe Path","cost":"0","probability":"0","color":"lightblue","shape":"square"},{"key":"DEFENSE_NODE","text":"Defense1","cost":1},{"key":"DEFENSE_NODE2","text":"Defense2","cost":2},{"key":"DEFENSE_NODE3","text":"Defense3","cost":2},{"key":"DEFENSE_NODE4","text":"Defense4","cost":6}],
"links": [{"from":"AND","to":"LEAF","fromPort":"b","toPort":"t","key":-3},{"from":"AND","to":"LEAF2","fromPort":"b","toPort":"t","key":-4},{"from":"AND2","to":"LEAF3","fromPort":"b","toPort":"t","key":-5},{"from":"AND2","to":"LEAF4","fromPort":"b","toPort":"t","key":-6},{"from":"OR","to":"AND","fromPort":"b","toPort":"t","key":-7},{"from":"OR","to":"AND2","fromPort":"b","toPort":"t","key":-8},{"from":"ROOT_NODE","to":"OR","fromPort":"b","toPort":"t","key":-9},{"from":"ROOT_NODE","to":"SAFE_PATH","fromPort":"b","toPort":"t","key":-10},{"from":"LEAF3","to":"DEFENSE_NODE3","fromPort":"b","toPort":"t","key":-12},{"from":"LEAF4","to":"DEFENSE_NODE4","fromPort":"b","toPort":"t","key":-11},{"from":"LEAF2","to":"DEFENSE_NODE2","fromPort":"b","toPort":"t","key":-13},{"from":"LEAF","to":"DEFENSE_NODE","fromPort":"b","toPort":"t","key":-14}]
}
"""
# jsonData = json.loads(jsonTest)

# nodesList = jsonData["nodes"]
# edgesList = jsonData["links"]

# normalize()

# scenarios, defenses = findScenarios(findAttackRoot())
# print(*scenarios, sep="\n")
# print(*defenses, sep="\n")

# attackCosts = [scenario.get_cost() for scenario in scenarios]
# costs = [scenario.get_cost() for scenario in defenses]

# eqs = nasheq(5, attackCosts, costs)
# print(list(eqs))

def backendRequest(frontendJson):
    jsonData = json.loads(frontendJson)

    nodesList = jsonData["nodeData"]
    edgesList = jsonData["edgeData"]

    normalize(nodesList)

    scenarios, defenses = findScenarios(findAttackRoot(nodesList))
    # print(*scenarios, sep="\n")
    # print(*defenses, sep="\n")

    attackCosts = [scenario.get_cost() for scenario in scenarios]
    costs = [scenario.get_cost() for scenario in defenses]

    eqs = nasheq(5, attackCosts, costs)

    listEqs = list(eqs)
    print(listEqs)
    returnJson = json.dumps(listEqs)

    return returnJson