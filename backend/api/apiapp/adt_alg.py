import json
import sys

#NOTE: Whenever the word 'cost' appears in this file, it is meaning cost of defense

class ADTScenario:
  def __init__(self, attackKey, probability, defendedProbability, cost):
    self.probability = float(probability)
    self.postdProbability = float(probability)
    self.riskPercentage = -1
    self.postdRiskPercentage = -1
    roi = (probability - defendedProbability) / cost
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
    self.postdProbability = self.probability
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
    self.acceptableRisk = float(jsonData["acceptableRiskThreshold"]) / 100
    self.budget = jsonData["defenseBudget"]
    self.budgetLeft = self.budget

    self.nodesList = jsonData["nodeData"]
    self.edgesList = jsonData["edgeData"]
    self.investedNodes = list()
    
    self.normalizeTree()
    treeRoot = self.findRoot()
    self.safePathProb = 0 #Is set in findAttackRoot()
    self.sumRiskValue = 0
    attackRoot = self.findAttackRoot(treeRoot)

    self.impact = float(treeRoot["impact"])
    
    self.scenarios = self.findScenarios(attackRoot)
    self.findRisk()
    self.scenarios.sort(reverse=True, key=lambda x: x.riskPercentage)
    self.analyzeTree()
    self.scenarios.sort(reverse=True, key=lambda x: x.postdRiskPercentage)
    return

  def __str__(self):
    output = "Acceptable Risk: " + str(self.acceptableRisk) + "\n"
    output += "Budget: " + str(self.budget) + "\n"
    output += "Cost: " + str(self.budget - self.budgetLeft) + "\n"
    output += "Safe Prob: " + str(self.safePathProb) + "\n"
    output += "Defended attacks: "
    for key in self.investedNodes:
        output += key + " "
    output += "\n"
    for scenario in self.scenarios:
      risk = str(round(scenario.riskPercentage, 5))
      drisk = str(round(scenario.postdRiskPercentage, 5))
      prob = str(round(scenario.probability, 5))
      dprob = str(round(scenario.postdProbability, 5))
      output += "Risk: " + drisk + "\tpre-defense Risk: " + risk + "\n"
      output += "Prob: " + dprob + "\tpre-defense Prob: " + prob + "\n\t "
      for key in scenario.attackDict.keys():
        output += key + " "
      output += "\n"
    return output

  def toDict(self):
    """Returns dictionary representation of ADTAnalysis (information not already in given JSON)"""
    defendedNodes = []
    for key in self.investedNodes:
        for node in self.nodesList:
          if node["key"] == key:
            defendedNodes.append([key, node["text"]])
    dit = {
      "cost" : (self.budget - self.budgetLeft),
      "defendedAttacks" : defendedNodes,
      "attackScenarios" : []
    }
    for scenario in self.scenarios:
      keys = list(scenario.attackDict.keys())
      keyTextPairs = []
      for key in keys:
        for node in self.nodesList:
          if node["key"] == key:
            keyTextPairs.append([key, node["text"]])
      scendit = {
        "risk" : scenario.postdRiskPercentage,
        "preDefenseRisk" : scenario.riskPercentage,
        "attacks" : keyTextPairs
      }
      dit["attackScenarios"].append(scendit)
    return dit

  def normalizeTree(self):
    sum = 0.0
    for node in self.nodesList:
      if node["key"][0] == "L":
        sum += float(node["preDefenseProbability"])
      elif node["key"][0] == "S":
        sum += float(node["probability"])
    for node in self.nodesList:
      if node["key"][0] == "L":
        node["preDefenseProbability"] = float(node["preDefenseProbability"]) / sum
        #added a try and except because I think I'm sending bad data
        try:
          node["postDefenseProbability"] = float(node["postDefenseProbability"]) / sum
        except:
          do_nothing = 0
      elif node["key"][0] == "S":
        node["probability"] = float(node["probability"]) / sum

  def findRoot(self):
    for n in self.nodesList:
      if(n["key"] == "ROOT_NODE"):
        return n
    print("Error:: Cannot find root node")
    return None

  def findAttackRoot(self, root):
    #Assumes properly constructed tree
    children = self.findChildren(root)
    root = None
    for node in children:
      if node["key"][0] != "S":
        root = node
      else:
        self.safePathProb = node["probability"]
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
    if(node == None):
      print("Error: No node found")
    else:
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

  def findRisk(self):
    if(self.scenarios == None):
      print("Error: No scenarios found")
    else:
      sum = self.safePathProb
      for scenario in self.scenarios:
        sum += scenario.probability
      for scenario in self.scenarios:
        scenario.riskPercentage = scenario.probability / sum
        scenario.postdRiskPercentage = scenario.probability / sum
      self.sumRiskValue = sum

  def recalculateRisk(self):
    sum = self.safePathProb
    for scenario in self.scenarios:
      #currentProb = 0
      keys = list(scenario.attackDict.keys())
      firstRun = True
      for key in keys:
        if firstRun:
          if key in self.investedNodes:
            currentProb = scenario.attackDict.get(key).get("dProb")
          else:
            currentProb = scenario.attackDict.get(key).get("prob")
          firstRun = False
        else:
          if key in self.investedNodes:
            currentProb *= scenario.attackDict.get(key).get("dProb")
          else:
            currentProb *= scenario.attackDict.get(key).get("prob")
      #sum += currentProb
      scenario.postdProbability = currentProb
    for scenario in self.scenarios:
      #scenario.postdRiskPercentage = scenario.postdProbability / sum
      scenario.postdRiskPercentage = scenario.postdProbability / self.sumRiskValue

  def analyzeTree(self):
    for scenario in self.scenarios: #Go through scenarios sorted by highest risk
      if scenario.postdRiskPercentage <= self.acceptableRisk:
        continue
      keys = list(scenario.attackDict.keys())
      keys.sort(reverse=True, key=lambda x: scenario.attackDict.get(x).get("roi"))

      for key in keys: #Go through attacks in scenario by highest return on investment
        if scenario.postdRiskPercentage <= self.acceptableRisk:
          break
        attack = scenario.attackDict.get(key)
        if attack.get("cost") <= self.budgetLeft:
          self.investedNodes.append(key)
          self.budgetLeft -= attack.get("cost")
          self.recalculateRisk()


def trimJson(jso):
  fluffStrs = ["color", "shape"]
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
  sendToFrontendJson = json.dumps(analysis.toDict())
  return sendToFrontendJson

