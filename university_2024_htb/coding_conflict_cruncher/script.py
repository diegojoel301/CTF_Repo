"""
ConflictCruncher
Welcome back, Space Cowboy. The Minutemen have uncovered multiple encrypted data streams from the Frontier Board. These streams contain critical intelligence, but their keys overlap in ways that cause conflicts.

Your mission is to merge these conflicting data streams into a single dictionary. When conflicts arise (identical keys), you must apply the Frontier Protocol: retain the value from the second dictionary and discard the conflicting value from the first.

Complete this task swiftly and accurately, Cowboy, and report the unified dictionary back to Lena Starling. The fate of the resistance may depend on it!

Example
Input
String Dict input: {'a': 1, 'b': 2, 'c': 3}, {'b': 4, 'd': 5}

Output
Merged Output: {'a': 1, 'b': 4, 'c': 3, 'd': 5}

"""

dict1_str = input()
dict2_str = input()

dict1 = eval(dict1_str)
dict2 = eval(dict2_str)

merged_dict = dict1.copy()
merged_dict.update(dict2)

print(merged_dict)

