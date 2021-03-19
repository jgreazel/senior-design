import json
import sys

#NOTE: Whenever the word 'cost' appears in this file, it is meaning cost of defense

class ADTScenario:
  def __init__(self, attackKey, probability, defendedProbability, cost):
    self.probability = float(probability)
    #self.minDcost = cost
    #self.minDcostNode = attackKey
    roi = (defendedProbability - probability) / cost
    self.attackDict[attackKey] = {
      "prob" : probability, 
      "dProb" : defendedProbability, 
      "roi" : roi, 
      "cost" : cost
      }

  def addAttack(self, attackKey, probability, defendedProbability, roi, cost):
    if self.attackDict.get(attackKey) != None:
      return False
    self.attackDict[attackKey] = {
      "prob" : probability, 
      "dProb" : defendedProbability, 
      "roi" : roi, 
      "cost" : cost
      }
    self.probability *= probability
    return True

  def combine(self, scenario2):
    newScenario = None
    keys = self.attackDict.keys()
    for key in keys:
      if newScenario == None:
        newScenario = ADTScenario(key, self.attackDict.get(key).get("prob"), self.attackDict.get(key).get("dProb"), self.attackDict.get(key).get("cost"))
      else:
        newScenario.addAttack(key,  self.attackDict.get(key).get("prob"), self.attackDict.get(key).get("dProb"), self.attackDict.get(key).get("roi"), self.attackDict.get(key).get("cost"))
    keys = scenario2.attackDict.keys()
    for key in keys:
      newScenario.addAttack(key, scenario2.attackDict.get(key).get("prob"), scenario2.attackDict.get(key).get("dProb"), scenario2.attackDict.get(key).get("roi"), scenario2.attackDict.get(key).get("cost")])
    return newScenario

class ADTAnalysis:
  def __init__(self, jsonData):
    self.nodesList = jsonData["nodeData"]
    self.edgesList = jsonData["edgeData"]
    self.investedNodes = list()

    self.normalize()

    treeRoot = self.findRoot()
    attackRoot = self.findAttackRoot(treeRoot)

    self.acceptableRisk = treeRoot["acceptableRisk"]
    self.impact = treeRoot["impact"]
    self.budget = treeRoot["budget"]
    self.budgetLeft = budget
    self.scenarios = self.findScenarios(attackRoot)
    self.scenarios.sort(reverse=True, key=lambda x: x.probability)
    return

  def normalize(self):
    sum = 0.0
    for node in self.nodesList:
      if node["key"][0] == "L":
        sum += float(node["probability"])
    for node in self.nodesList:
      node["probability"] = float(node["probability"]) / sum
      node["defendedProbability"] = float(node["defendedProbability"]) / sum

  def analyzeTree(self):
    #TODO
    defendedKeys = []
    for scenario in self.scenarios: #Go through scenarios sorted by highest risk
      keys = scenario.attackDict.keys()
      keysByRoi = keys.sort(reverse=True, key=lambda x: scenario.attackDict.get(x).get("roi"))
      for key in keysByRoi: #for attacks already defended by other runs across scenarios
        if key in defendedKeys:
          scenario.probability = (scenario.probability / scenario.attackDict.get(key).get("prob")) * scenario.attackDict.get(key).get("dProb")
          keysByRoi.remove(key)
      acceptable = (scenario.probability * self.impact) > self.acceptableRisk
      for key in keysByRoi: #Go through attacks in scenario by highest return on investment
        if acceptable:
          #break?
        attack = scenario.attackDict.get(key)
        if attack.get("cost") <= budgetLeft:
          defendedKeys.append(key)
          scenario.probability = (scenario.probability / attack.get("prob")) * attack.get("dProb")
          self.budgetLeft -= attack.get("cost")
        
    #attackRoot = self.findAttackRoot(self.treeRoot)
    return

  def findRoot(self):
    root = None
    for n in self.nodesList:
      hasParent = False
      # Check if node exists as a destination in edge list
      for e in self.edgesList:
        if e["to"] == n["key"]:
          hasParent = True
          break
      if not hasParent:
        root = n
        break
    if root is None:
        print("Error:: Cannot find root node")
    return root

  def findAttackRoot(self, root):
    children = self.findChildren(root)
    for node in children:
      if node["key"][0] != "L":
        return node
    print("Error:: Cannot find attack root node")
    return root

  def findNode(self, key):
    for node in self.nodesList:
      if node["key"] == key:
        return node
    print("Error:: Could not find node with given key")

  def findChildren(self, node):
    children = list(())
    for e in self.edgesList:
      if e["from"] == node["key"]:
        children.append(self.findNode(e["to"]))
    return children

  def findScenarios(self, node):
    if node["key"][0] == "L":  # If leaf node
      singleList = self.findChildren(node)
      scenarioList = list(())
      scenarioList.append(ADTScenario(node["key"], node["probability"], node["defendedProbability"], singleList[0]["cost"]))
      return scenarioList
    elif node["key"][0] == "O":  # If OR node
      scenarioList = list(())
      children = self.findChildren(node)
      for child in children:
        childScenarios = self.findScenarios(child)
        for scenario in childScenarios:
          scenarioList.append(scenario)
        return scenarioList
    elif node["key"][0] == "A":  # If AND node
      scenarioList = list(())
      tempList = list(())
      childLists = list(())  # List of lists
      children = self.findChildren(node)
      for child in children:  # Create list of child scenario lists
        childLists.append(self.findScenarios(child))
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
#jsonData = json.loads(jsonObj)

#nodesList = jsonData["nodeData"]
#edgesList = jsonData["edgeData"]

#normalize()

#treeRoot = findRoot()
#attackRoot = findAttackRoot(treeRoot)

#acceptableRisk = treeRoot["acceptableRisk"]
#scenarios = findScenarios(attackRoot)

#None of stuff below would work rn
#scenList = []
#for scen in scenarios:
#    scenList.append(scen.toDict())

def backendRequest(frontendJson):
  jsonData = json.loads(frontendJson)
  analysis = ADTAnalysis(jsonData)
  sendToFrontendJson = json.dumps(scenList)
  print(sendToFrontendJson)
  return sendToFrontendJson

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
