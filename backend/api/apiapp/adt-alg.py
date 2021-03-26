import json
import sys

#NOTE: Whenever the word 'cost' appears in this file, it is meaning cost of defense

class ADTScenario:
  def __init__(self, attackKey, probability, defendedProbability, cost):
    self.probability = float(probability)
    self.postdProbability = -1
    #self.minDcost = cost
    #self.minDcostNode = attackKey
    roi = (defendedProbability - probability) / cost
    self.attackDict = {}
    self.attackDict[attackKey] = {
      "prob" : probability, 
      "dProb" : defendedProbability, 
      "roi" : roi, 
      "cost" : cost
      }

  def __str__(self):
    """Returns nodes in scenario"""
    prob = str(round(self.probability, 5))
    dprob = str(round(self.postdProbability, 5))
    output = "dprob: " + dprob + "  \tprob: " + prob + "\t: "
    for key in self.attackDict.keys():
      output += key + " "
    return output

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
      newScenario.addAttack(key, scenario2.attackDict.get(key).get("prob"), scenario2.attackDict.get(key).get("dProb"), scenario2.attackDict.get(key).get("roi"), scenario2.attackDict.get(key).get("cost"))
    return newScenario

class ADTAnalysis:
  def __init__(self, jsonData):
    self.acceptableRisk = float(jsonData["acceptableRiskThreshold"]) / 10.0
    self.budget = jsonData["defenseBudget"]
    self.budgetLeft = self.budget

    self.nodesList = jsonData["nodeData"]
    self.edgesList = jsonData["edgeData"]
    self.investedNodes = list()

    self.normalize()
    treeRoot = self.findRoot()
    attackRoot = self.findAttackRoot(treeRoot)

    self.impact = float(treeRoot["impact"])
    #self.acceptableRisk = treeRoot["acceptableRisk"] * self.impact #maybe
    #self.budget = treeRoot["budget"]
    
    self.scenarios = self.findScenarios(attackRoot)
    self.scenarios.sort(reverse=True, key=lambda x: x.probability)
    return

  def __str__(self):
    output = "Acceptable Risk: " + str(self.acceptableRisk) + "\n"
    output += "Budget: " + str(self.budget) + "\n"
    output += "Cost: " + str(self.budget - self.budgetLeft) + "\n"
    output += "Defended attacks: "
    for key in self.investedNodes:
        output += key + " "
    output += "\n"
    for scenario in self.scenarios:
      risk = str(round(self.impact * scenario.postdProbability, 5))
      prob = str(round(scenario.probability, 5))
      dprob = str(round(scenario.postdProbability, 5))
      output += "risk: " + risk + "  \tprob: " + dprob + "\tpre-defense prob: " + prob + "\n\t "
      for key in scenario.attackDict.keys():
        output += key + " "
      output += "\n"
    return output

  def normalize(self):
    sum = 0.0
    for node in self.nodesList:
      if node["key"][0] == "L":
        sum += float(node["preDefenseProbability"])
    for node in self.nodesList:
      if node["key"][0] == "L":
        node["preDefenseProbability"] = node["preDefenseProbability"] / sum
        node["postDefenseProbability"] = node["postDefenseProbability"] / sum

  def analyzeTree(self):
    for scenario in self.scenarios: #Go through scenarios sorted by highest risk
      if scenario.probability <= self.acceptableRisk:
          break
      keys = list(scenario.attackDict.keys())
      keys.sort(reverse=True, key=lambda x: scenario.attackDict.get(x).get("roi"))
      prob = scenario.probability
      for key in keys: #for attacks already defended by other runs across scenarios
        if key in self.investedNodes:
          prob = (prob / scenario.attackDict.get(key).get("prob")) * scenario.attackDict.get(key).get("dProb")
          keys.remove(key)
      #acceptable = (scenario.probability * self.impact) > self.acceptableRisk
      for key in keys: #Go through attacks in scenario by highest return on investment
        if prob <= self.acceptableRisk: #prob * self.impact???
          break
        attack = scenario.attackDict.get(key)
        if attack.get("cost") <= self.budgetLeft:
          self.investedNodes.append(key)
          prob = (prob / attack.get("prob")) * attack.get("dProb")
          self.budgetLeft -= attack.get("cost")
    #attackRoot = self.findAttackRoot(self.treeRoot)

    #Go through scenarios in case an attack was defended in a scenario after it had been processed above. 
    # in other words recalculate probability for every scenario
    for scenario in self.scenarios:       
      keys = scenario.attackDict.keys()
      firstRun = True
      recalcProb = 0
      for key in keys: #for attacks already defended by other runs across scenarios
        if firstRun:
          if key in self.investedNodes:
            recalcProb = scenario.attackDict.get(key).get("dProb")
          else:
            recalcProb = scenario.attackDict.get(key).get("prob")
          firstRun = False
        else:
          if key in self.investedNodes:
            recalcProb = recalcProb * scenario.attackDict.get(key).get("dProb")
          else:
            recalcProb = recalcProb * scenario.attackDict.get(key).get("prob")
      scenario.postdProbability = recalcProb
    return

  def findRoot(self):
    for n in self.nodesList:
      if(n["key"] == "ROOT_NODE"):
        return n
    print("Error:: Cannot find root node")
    return None

  def findAttackRoot(self, root):
    children = self.findChildren(root)
    for node in children:
      if node["key"][0] != "S":
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
      scenarioList.append(ADTScenario(node["key"], node["preDefenseProbability"], node["postDefenseProbability"], singleList[0]["defenseCost"]))
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

def trimJson(jso):
  fluffStrs = ["text", "color", "shape", ]
  for node in jso["nodeData"]:
    keys = list(node.keys())
    for key in keys:
      if key in fluffStrs:
        del node[key]
  fluffStrs = ["fromPort", "toPort", "key"]
  for edge in jso["edgeData"]:
    keys = list(edge.keys())
    for key in keys:
      if key in fluffStrs:
        del edge[key]
        
def backendRequest(frontendJson):
  jsonData = json.loads(frontendJson)
  trimJson(jsonData)
  analysis = ADTAnalysis(jsonData)
  analysis.analyzeTree()
  print("\n")
  print(analysis)

  #sendToFrontendJson = json.dumps(scenList)
  #print(sendToFrontendJson)
  #return sendToFrontendJson

#Example JSON insufficient for ADT rn
jsonObj1 = """
{
    "acceptableRiskThreshold": 0.01,
    "defenseBudget": 600,
    "nodeData": [{
        "key": "ROOT_NODE",
        "text": "Root Node",
        "impact": 5300
    }, {
        "key": "SAFE_PATH",
        "text": "Safe Path",
        "probability": 1
    }, {
        "key": "AND",
        "color": "red",
        "shape": "andgate"
    }, {
        "key": "OR",
        "color": "green",
        "shape": "orgate"
    }, {
        "key": "AND2",
        "color": "red",
        "shape": "andgate"
    }, {
        "key": "OR2",
        "color": "green",
        "shape": "orgate"
    }, {
        "key": "LEAF",
        "text": "placeholderText",
        "preDefenseProbability": 5,
        "postDefenseProbability": 2
    }, {
        "key": "LEAF2",
        "text": "placeholderText",
        "preDefenseProbability": 8,
        "postDefenseProbability": 4
    }, {
        "key": "LEAF3",
        "text": "placeholderText",
        "preDefenseProbability": 2,
        "postDefenseProbability": 1
    }, {
        "key": "LEAF4",
        "text": "placeholderText",
        "preDefenseProbability": 1,
        "postDefenseProbability": 0.5
    }, {
        "key": "LEAF5",
        "text": "placeholderText",
        "preDefenseProbability": 2,
        "postDefenseProbability": 1
    }, {
        "key": "LEAF6",
        "text": "placeholderText",
        "preDefenseProbability": 8,
        "postDefenseProbability": 6
    }, {
        "key": "LEAF7",
        "text": "placeholderText",
        "preDefenseProbability": 4,
        "postDefenseProbability": 3
    }, {
        "key": "DEFENSE_NODE",
        "text": "Defense",
        "defenseCost": 500
    }, {
        "key": "DEFENSE_NODE2",
        "text": "Defense",
        "defenseCost": 200
    }, {
        "key": "DEFENSE_NODE3",
        "text": "Defense",
        "defenseCost": 350
    }, {
        "key": "DEFENSE_NODE4",
        "text": "Defense",
        "defenseCost": 300
    }, {
        "key": "DEFENSE_NODE5",
        "text": "Defense",
        "defenseCost": 200
    }, {
        "key": "DEFENSE_NODE6",
        "text": "Defense",
        "defenseCost": 100
    }, {
        "key": "DEFENSE_NODE7",
        "text": "Defense",
        "defenseCost": 250
    }],
    "edgeData": [{
        "from": "ROOT_NODE",
        "to": "AND",
        "fromPort": "b",
        "toPort": "t",
        "key": -1
    }, {
        "from": "ROOT_NODE",
        "to": "SAFE_PATH",
        "fromPort": "b",
        "toPort": "t",
        "key": -2
    }, {
        "from": "AND",
        "to": "OR",
        "fromPort": "b",
        "toPort": "t",
        "key": -3
    }, {
        "from": "AND",
        "to": "AND2",
        "fromPort": "b",
        "toPort": "t",
        "key": -4
    }, {
        "from": "AND",
        "to": "LEAF",
        "fromPort": "b",
        "toPort": "t",
        "key": -5
    }, {
        "from": "OR",
        "to": "LEAF2",
        "fromPort": "b",
        "toPort": "t",
        "key": -6
    }, {
        "from": "OR",
        "to": "LEAF4",
        "fromPort": "b",
        "toPort": "t",
        "key": -7
    }, {
        "from": "OR",
        "to": "LEAF3",
        "fromPort": "b",
        "toPort": "t",
        "key": -8
    }, {
        "from": "OR2",
        "to": "LEAF5",
        "fromPort": "b",
        "toPort": "t",
        "key": -9
    }, {
        "from": "OR2",
        "to": "LEAF6",
        "fromPort": "b",
        "toPort": "t",
        "key": -10
    }, {
        "from": "AND2",
        "to": "LEAF7",
        "fromPort": "b",
        "toPort": "t",
        "key": -11
    }, {
        "from": "AND2",
        "to": "OR2",
        "fromPort": "b",
        "toPort": "t",
        "key": -12
    }, {
        "from": "LEAF2",
        "to": "DEFENSE_NODE",
        "fromPort": "b",
        "toPort": "t",
        "key": -13
    }, {
        "from": "LEAF3",
        "to": "DEFENSE_NODE2",
        "fromPort": "b",
        "toPort": "t",
        "key": -14
    }, {
        "from": "LEAF4",
        "to": "DEFENSE_NODE3",
        "fromPort": "b",
        "toPort": "t",
        "key": -15
    }, {
        "from": "LEAF5",
        "to": "DEFENSE_NODE5",
        "fromPort": "b",
        "toPort": "t",
        "key": -16
    }, {
        "from": "LEAF6",
        "to": "DEFENSE_NODE6",
        "fromPort": "b",
        "toPort": "t",
        "key": -17
    }, {
        "from": "LEAF7",
        "to": "DEFENSE_NODE7",
        "fromPort": "b",
        "toPort": "t",
        "key": -18
    }, {
        "from": "LEAF",
        "to": "DEFENSE_NODE4",
        "fromPort": "b",
        "toPort": "t",
        "key": -19
    }]
}
"""

jsonObj2 = """
{
    "acceptableRiskThreshold": 2,
    "defenseBudget": 550,
    "nodeData": [{
        "key": "ROOT_NODE",
        "impact": 200
    }, {
        "key": "SAFE_PATH",
        "probability": "0"
    }, {
        "key": "OR"
    }, {
        "key": "AND"
    }, {
        "key": "AND2"
    }, {
        "key": "OR2"
    }, {
        "key": "LEAF",
        "preDefenseProbability": 5,
        "postDefenseProbability": 2
    }, {
        "key": "LEAF2",
        "preDefenseProbability": 7,
        "postDefenseProbability": 3
    }, {
        "key": "LEAF3",
        "preDefenseProbability": 9,
        "postDefenseProbability": 3
    }, {
        "key": "DEFENSE_NODE",
        "text": "Defense",
        "defenseCost": 150
    }, {
        "key": "DEFENSE_NODE2",
        "text": "Defense",
        "defenseCost": 200
    }, {
        "key": "DEFENSE_NODE3",
        "text": "Defense",
        "defenseCost": 100
    }],
    "edgeData": [{
        "from": "ROOT_NODE",
        "to": "SAFE_PATH",
        "key": -1
    }, {
        "from": "ROOT_NODE",
        "to": "OR",
        "key": -2
    }, {
        "from": "OR",
        "to": "LEAF",
        "key": -3
    }, {
        "from": "OR",
        "to": "AND",
        "key": -4
    }, {
        "from": "AND",
        "to": "LEAF2",
        "key": -5
    }, {
        "from": "AND",
        "to": "LEAF3",
        "key": -6
    }, {
        "from": "LEAF",
        "to": "DEFENSE_NODE",
        "key": -7
    }, {
        "from": "LEAF2",
        "to": "DEFENSE_NODE2",
        "key": -8
    }, {
        "from": "LEAF3",
        "to": "DEFENSE_NODE3",
        "key": -9
    }]
}
"""


backendRequest(jsonObj1)
#jsonData = json.loads(jsonObj)
#trimJson(jsonData)
#print(json.dumps(jsonData))


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
