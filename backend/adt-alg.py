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
    self.acceptableRisk = jsonData["acceptableRiskThreshold"]
    self.budget = jsonData["defenseBudget"]
    self.budgetLeft = self.budget

    self.nodesList = jsonData["nodeData"]
    self.edgesList = jsonData["edgeData"]
    self.investedNodes = list()

    self.normalize()
    treeRoot = self.findRoot()
    attackRoot = self.findAttackRoot(treeRoot)

    self.impact = treeRoot["impact"]
    #self.acceptableRisk = treeRoot["acceptableRisk"] * self.impact #maybe
    #self.budget = treeRoot["budget"]
    
    self.scenarios = self.findScenarios(attackRoot)
    self.scenarios = self.scenarios.sort(reverse=True, key=lambda x: x.probability)
    return

  def __str__(self):
    # TODO: 
    scens = self.scenarios.sort(reverse=True, key=lambda x: x.probability)
    output = ""
    for scenario in scens:
      risk = str(round(self.impact * scenario.probability, 4))
      prob = str(round(scenario.probability, 4))
      dprob = str(round(scenario.postdProbability, 4))
      output += "risk: " + risk + "  \tdprob: " + dprob + "\tprob: " + prob + "\t: "
      for key in scenario.attackDict.keys():
        output += key + " "
    return output

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
      if scenario.probability <= self.acceptableRisk:
          break
      keys = scenario.attackDict.keys()
      keysByRoi = keys.sort(reverse=True, key=lambda x: scenario.attackDict.get(x).get("roi"))
      prob = scenario.probability
      for key in keysByRoi: #for attacks already defended by other runs across scenarios
        if key in defendedKeys:
          prob = (prob / scenario.attackDict.get(key).get("prob")) * scenario.attackDict.get(key).get("dProb")
          keysByRoi.remove(key)
      #acceptable = (scenario.probability * self.impact) > self.acceptableRisk
      for key in keysByRoi: #Go through attacks in scenario by highest return on investment
        if prob <= self.acceptableRisk: #prob * self.impact???
          break
        attack = scenario.attackDict.get(key)
        if attack.get("cost") <= self.budgetLeft:
          defendedKeys.append(key)
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
          if key in defendedKeys:
            recalcProb = scenario.attackDict.get(key).get("dProb")
          else:
            recalcProb = scenario.attackDict.get(key).get("prob")
          firstRun = False
        else:
          if key in defendedKeys:
            recalcProb = recalcProb * scenario.attackDict.get(key).get("dProb")
          else:
            recalcProb = recalcProb * scenario.attackDict.get(key).get("prob")
      scenario.postdProbability = recalcProb
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
    "nodeData": [{
        "key": "ROOT_NODE",
        "text": "Root Node",
        "impact": 500
    }, {
        "key": "SAFE_PATH",
        "text": "Safe Path",
        "probability": 2
    }, {
        "key": "OR",
        "color": "green",
        "shape": "orgate"
    }, {
        "key": "AND",
        "color": "red",
        "shape": "andgate"
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
        "preDefenseProbability": 9,
        "postDefenseProbability": 5
    }, {
        "key": "LEAF2",
        "text": "placeholderText",
        "preDefenseProbability": 3,
        "postDefenseProbability": 1
    }, {
        "key": "LEAF3",
        "text": "placeholderText",
        "preDefenseProbability": 2,
        "postDefenseProbability": 1
    }, {
        "key": "LEAF4",
        "text": "placeholderText",
        "preDefenseProbability": 4,
        "postDefenseProbability": 2
    }, {
        "key": "LEAF5",
        "text": "placeholderText",
        "preDefenseProbability": 5,
        "postDefenseProbability": 1
    }, {
        "key": "LEAF6",
        "text": "placeholderText",
        "preDefenseProbability": 8,
        "postDefenseProbability": 6
    }, {
        "key": "DEFENSE_NODE",
        "text": "Defense",
        "defenseCost": 100
    }, {
        "key": "DEFENSE_NODE2",
        "text": "Defense",
        "defenseCost": 300
    }, {
        "key": "DEFENSE_NODE3",
        "text": "Defense",
        "defenseCost": 250
    }, {
        "key": "DEFENSE_NODE4",
        "text": "Defense",
        "defenseCost": 50
    }, {
        "key": "DEFENSE_NODE5",
        "text": "Defense",
        "defenseCost": 80
    }, {
        "key": "DEFENSE_NODE6",
        "text": "Defense",
        "defenseCost": 250
    }],
    "edgeData": [{
        "from": "ROOT_NODE",
        "to": "SAFE_PATH",
        "fromPort": "b",
        "toPort": "t",
        "key": -1
    }, {
        "from": "ROOT_NODE",
        "to": "OR",
        "fromPort": "b",
        "toPort": "t",
        "key": -2
    }, {
        "from": "OR",
        "to": "AND2",
        "fromPort": "b",
        "toPort": "t",
        "key": -3
    }, {
        "from": "OR",
        "to": "AND",
        "fromPort": "b",
        "toPort": "t",
        "key": -4
    }, {
        "from": "AND2",
        "to": "OR2",
        "fromPort": "b",
        "toPort": "t",
        "key": -5
    }, {
        "from": "OR",
        "to": "LEAF6",
        "fromPort": "b",
        "toPort": "t",
        "key": -6
    }, {
        "from": "OR2",
        "to": "LEAF3",
        "fromPort": "b",
        "toPort": "t",
        "key": -7
    }, {
        "from": "OR2",
        "to": "LEAF4",
        "fromPort": "b",
        "toPort": "t",
        "key": -8
    }, {
        "from": "AND2",
        "to": "LEAF5",
        "fromPort": "b",
        "toPort": "t",
        "key": -9
    }, {
        "from": "AND",
        "to": "LEAF",
        "fromPort": "b",
        "toPort": "t",
        "key": -10
    }, {
        "from": "AND",
        "to": "LEAF2",
        "fromPort": "b",
        "toPort": "t",
        "key": -11
    }, {
        "from": "LEAF",
        "to": "DEFENSE_NODE",
        "fromPort": "b",
        "toPort": "t",
        "key": -12
    }, {
        "from": "LEAF2",
        "to": "DEFENSE_NODE2",
        "fromPort": "b",
        "toPort": "t",
        "key": -13
    }, {
        "from": "LEAF3",
        "to": "DEFENSE_NODE3",
        "fromPort": "b",
        "toPort": "t",
        "key": -14
    }, {
        "from": "LEAF4",
        "to": "DEFENSE_NODE4",
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
    }]
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
