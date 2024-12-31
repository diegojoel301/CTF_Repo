"""
Exclusivity: Frontier Cluster
Welcome back, Space Cowboy. The Minutemen have intercepted a cryptic signal from the Frontier Board—a corrupted data stream filled with duplicate entries. Hidden within this mess are critical coordinates that could lead us closer to the legendary Starry Spur.

Your mission is to sift through this chaotic stream and extract the unique entries. These coordinates must be preserved in the order they were received to maintain their integrity. Any duplicates are remnants of the Board's sabotage—eliminate them swiftly.

Once you've completed the task, report the refined list to Lena Starling. Time is of the essence, Cowboy—the resistance is counting on you!

Example
Input
String Input: 7 3 7 9 1 3 5 9

Output
String Expected Output: 7 3 9 1 5
"""
def main():
    input_string = input().strip()
    
    coordinates = input_string.split()
    unique_coordinates = []
    seen = set()
    
    for coord in coordinates:
        if coord not in seen:
            unique_coordinates.append(coord)
            seen.add(coord)
    
    print(" ".join(unique_coordinates))

if __name__ == "__main__":
    main()