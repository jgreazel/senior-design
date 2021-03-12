import json
import sys


class Scenario:
  def __init__(self, attackKey, probability, cost):
    self.probability = float(probability)
    self.minDcost = cost
    self.minDcostNode = attackKey
    self.attackDict[attackKey] = [probability, cost]

  def __str__(self): #OUTDATED
    risk = str(round(float(treeRoot["impact"]) * self.probability, 4))
    prob = str(round(self.probability, 4))
    output = "risk: " + risk + "  \tprob: " + prob + "\t: "
    for key in self.CHANGE:
      output += key + " "
    return output

  def toDict(self): #OUTDATED
    risk = round(float(treeRoot["impact"]) * self.probability, 4)
    prob = round(self.probability, 4)
    leafKeys = self.CHANGE
    dit = {
      "risk" : risk,
      "probability" : prob,
      "leafKeys" : leafKeys
      }
    return dit

  def addAttack(self, attackKey, probability, cost):
    if self.attackDict.get(attackKey) != None:
      return False
    self.attackDict[attackKey] = [probability, cost]
    self.probability *= probability
    if(cost < self.minDcost):
      self.minDcost = cost
      self.minDcostNode = attackKey
    return True

  def combine(self, scenario2):
    newScenario = None
    keys = self.attackDict.keys()
    for key in keys:
      if newScenario == None:
        newScenario = Scenario(key, self.attackDict.get(key)[0], self.attackDict.get(key)[1])
      else:
        newScenario.addAttack(key, self.attackDict.get(key)[0], self.attackDict.get(key)[1])
    keys = scenario2.attackDict.keys()
    for key in keys:
      newScenario.addAttack(key, scenario2.attackDict.get(key)[0], scenario2.attackDict.get(key)[1])
    return newScenario

def normalize():
  sum = 0.0
  for node in nodesList:
    if node["key"][0] == "L":
      sum += float(node["probability"])
  for node in nodesList:
    node["probability"] = float(node["probability"]) / sum

def findRoot():
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
  children = findChildren(root)
  for node in children:
    if node["key"][0] != "L":
      return node
  print("Error:: Cannot find attack root node")
  return root

def findNode(key):
  for node in nodesList:
    if node["key"] == key:
      return node
  print("Error:: Could not find node with given key")

def findChildren(node):
  children = list(())
  for e in edgesList:
    if e["from"] == node["key"]:
      children.append(findNode(e["to"]))
  return children

def findScenarios(node):
  if node["key"][0] == "L":  # If leaf node
    singleList = findChildren(node)
    scenarioList = list(())
    scenarioList.append(Scenario(node["key"], node["probability"], singleList[0]["cost"]))
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

'''
Go through all scenarios and make a list of ones above the acceptable risk threshold
Make list of attacks that appear in multiple of these scenarios
Compile combinations of defenses using attacks from the above list and the min cost attacks of a scenario such that each combination includes defenses that
  would protect against all scenarios above the acceptable risk threshold
Find the lowest cost option (or options) for return
'''

#Example JSON insufficient for ADT rn
jsonObj = """
{
  "nodeData": [
    {
      "key": "OR3",
      "text": "placeholderText",
      "probability": "0",
      "impact": "450",
      "color": "red",
      "shape": "andgate"
    },
    {
      "key": "LEAF5",
      "text": "safePath",
      "probability": "8"
    },
    {
      "key": "AND",
      "text": "placeholderText",
      "probability": "0",
      "color": "red",
      "shape": "andgate"
    },
    {
      "key": "OR",
      "text": "placeholderText",
      "probability": "0",
      "color": "lightgreen",
      "shape": "orgate"
    },
    {
      "key": "LEAF",
      "text": "cyberAttack",
      "probability": "1.1"
    },
    {
      "key": "LEAF2",
      "text": "physicalAttack",
      "probability": "8.3"
    },
    {
      "key": "OR2",
      "text": "placeholderText",
      "probability": "0",
      "color": "lightgreen",
      "shape": "orgate"
    },
    {
      "key": "LEAF3",
      "text": "phishingAttack",
      "probability": "7.2"
    },
    {
      "key": "LEAF4",
      "text": "spyware",
      "probability": "3.4"
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

acceptableRisk = treeRoot["acceptableRisk"]
scenarios = findScenarios(attackRoot)

#None of stuff below would work rn
scenList = []
for scen in scenarios:
    scenList.append(scen.toDict())

sendToFrontendJson = json.dumps(scenList)
print(sendToFrontendJson)

#ADT ALG

"""
tree:
{
  nodes :
    root :
      key : $$$
      impact : ###          //impact
      acceptableRisk : ###  //acceptable risk level 
                              //QUESTION: Risk is (impact * probability). Is acceptable risk level a normalized probability multiplied by the impact or an actual risk value?
                              //If it is a normalized probability, why is the impact/risk value meaningful?
    gate :
      key : $$$
    leaf/safe path :
      key : $$$
      probability : ###     //probability
    defense :
      key : $$$
      cost : $$$            //defender cost

  edges :
    from : $$$
    to : $$$
}

scenario:   //just data storage concept, not for returning or receiving
{
  scenarios :
    probability : ###
    min_dcost : ###
    attacks :
      key : $$$
        probability : ###
        dcost : ###
}
"""