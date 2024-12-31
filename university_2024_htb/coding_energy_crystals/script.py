energy_crystals = input()  
target_energy = input()  

energy_crystals = list(map(int, energy_crystals.strip("[]").split(",")))
target_energy = int(target_energy)

def count_combinations(energy_crystals, target_energy):
    
    dp = [0] * (target_energy + 1)
    
    dp[0] = 1
    
    for crystal in energy_crystals:
        
        for energy in range(crystal, target_energy + 1):
            dp[energy] += dp[energy - crystal]
    
    
    return dp[target_energy]

print(count_combinations(energy_crystals, target_energy))

