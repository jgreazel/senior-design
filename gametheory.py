import nashpy as nash

def nasheq(impacts, attack_costs, defense_costs):
  """
  Computes the nash equilibrium for the given impacts, attack costs,
  and defense costs. Currently expects 1D parameters of equal length.

  Returns an equilibria generator.
  """
  payoff_attacker = []
  for i in range(len(defense_costs)):
      payoff_row = []
      for j in range(len(impacts)):
          if i == j:
              payoff_row.append(defense_costs[i])
          else:
              payoff_row.append(defense_costs[i] + impacts[i] - attack_costs[i])
      payoff_attacker.append(payoff_row)

  game = nash.Game(payoff_attacker)
  eqs = game.support_enumeration()
  return eqs