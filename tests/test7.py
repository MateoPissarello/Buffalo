# Number of organisms who are homo_dominant (k), hetero (m), and homo_recessive (n)
k = 18
m = 27
n = 20
t = k + m + n

# Probabilities of first selection
Pk, Pm, Pn = k / t, m / t, n / t

# A few variables I made to clean up my equations
t1 = t - 1
k1 = k - 1
m1 = m - 1
n1 = n - 1

# Dictionary where the keys are probabilities of first selection and second selection, so "Pktk" /
# means selecting a k and then another k.
variables_dict = {
    "Pktk": Pk * k1 / t1,
    "Pktm": Pk * m / t1,
    "Pktn": Pk * n / t1,
    "Pmtk": Pm * k / t1,
    "Pmtm": Pm * m1 / t1,
    "Pmtn": Pm * n / t1,
    "Pntk": Pn * k / t1,
    "Pntm": Pn * m / t1,
    "Pntn": Pn * n1 / t1,
}

# I made this for loop to modify the values in the previous dict. to update the probability /
# of two organisms producing an offspring with the dominant phenotype
for variable in variables_dict:
    if variable.count("n") == 1 and variable.count("m") == 1:
        variables_dict[variable] = variables_dict[variable] * 0.5
        continue
    if variable.count("m") == 2:
        variables_dict[variable] = variables_dict[variable] * 0.75
        continue
    if variable.count("n") == 2:
        variables_dict[variable] = variables_dict[variable] * 0
        continue
    else:
        continue


# This takes the dictionary and adds up the values to find the total probability
def find_P_dominantphenotype(dict):
    probabilities = list(dict.values())
    result = sum(probabilities)
    return result


probability = find_P_dominantphenotype(variables_dict)
print(probability)
