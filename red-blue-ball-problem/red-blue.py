from itertools import product
from time import time
import sys

universe = [
    9461587, 7871334, 5997675, 4868524,
    6483210, 8081143, 8548032, 8296679,
    8541031, 9385134, 4446914, 1734483,
    5712289, 4181842, 1430045, 4781945,
    6196470, 6379814, 9225457, 6023386,
    7950188, 3396206, 7451512, 1196930,
    2751186, 8025282, 4443634, 5324739,
    8545397, 1966247
]

length = len(universe) // 2
first = universe[:length]
second = universe[length:]

print(f"Split into {len(first)} + {len(second)} elements")
print(f"Expected iterations per half: 3^{len(first)} = {3**len(first):,}")
print("-" * 60)

def create_sumproducts_optimized(arr, label):
    """Optimized version with progress tracking"""
    sumproducts = {}
    total_iterations = 3 ** len(arr)
    checkpoint = total_iterations // 100  # Update every 1%
    
    start_time = time()
    
    for idx, signs in enumerate(product([-1, 0, 1], repeat=len(arr))):
        # Calculate sum directly without building lists first
        total = sum(val * sign for val, sign in zip(arr, signs))
        
        # Only build red/blue lists when storing (more efficient)
        red = tuple(arr[i] for i, s in enumerate(signs) if s == 1)
        blue = tuple(arr[i] for i, s in enumerate(signs) if s == -1)
        
        sumproducts[total] = (red, blue)
        
        # Progress tracking
        if idx % checkpoint == 0 and idx > 0:
            percent = (idx / total_iterations) * 100
            elapsed = time() - start_time
            rate = idx / elapsed
            eta = (total_iterations - idx) / rate
            
            sys.stdout.write(f"\r{label}: {percent:.1f}% | "
                           f"{idx:,}/{total_iterations:,} | "
                           f"Rate: {rate:,.0f} iter/s | "
                           f"ETA: {eta:.1f}s")
            sys.stdout.flush()
    
    elapsed = time() - start_time
    print(f"\r{label}: 100.0% | {total_iterations:,}/{total_iterations:,} | "
          f"Completed in {elapsed:.2f}s")
    
    return sumproducts

# Generate sumproducts for both halves: reduces the problem size from 3^30 to 3^15 + 3^15
print("\nPhase 1: Generating first half combinations...")
first_sumproducts = create_sumproducts_optimized(first, "First half ")

print("\nPhase 2: Generating second half combinations...")
second_sumproducts = create_sumproducts_optimized(second, "Second half")

# Find matches !A dicitionary lookup is O(1) on average, and hence this will only take O(3^15) time instead of O(3^15^2)
print("\nPhase 3: Finding balanced partitions...")
start_time = time()
results = []


for idx, (sum1, (red1, blue1)) in enumerate(first_sumproducts.items()):
    if -sum1 in second_sumproducts:
        red2, blue2 = second_sumproducts[-sum1]
        red = red1 + red2
        blue = blue1 + blue2
        results.append((red, blue))
    
    # Progress tracking for matching phase
    if idx % 100000 == 0 and idx > 0:
        percent = (idx / len(first_sumproducts)) * 100
        sys.stdout.write(f"\rMatching: {percent:.1f}% | {idx:,}/{len(first_sumproducts):,}")
        sys.stdout.flush()

elapsed = time() - start_time
print(f"\rMatching: 100.0% | {len(first_sumproducts):,}/{len(first_sumproducts):,} | "
      f"Completed in {elapsed:.2f}s")

print("\n" + "=" * 60)
print(f"Found {len(results)} balanced partitions (including duplicates)")
print(f"Unique partitions: {(len(results) + 1) // 2} (accounting for red/blue symmetry)")
print(f"Memory: ~{(sys.getsizeof(first_sumproducts) + sys.getsizeof(second_sumproducts)) / (1024**2):.1f} MB")

# Show detailed results
if results:
    print("\n" + "=" * 60)
    print("DETAILED RESULTS")
    print("=" * 60)
    
    # Show first 5 balanced partitions with full details
    num_to_show = min(5, len(results))
    print(f"\nShowing first {num_to_show} balanced partitions:\n")
    
    for i, (red, blue) in enumerate(results[:num_to_show]):
        print(f"{'='*60}")
        print(f"PARTITION {i+1}")
        print(f"{'='*60}")
        
        red_sum = sum(red)
        blue_sum = sum(blue)
        neither = [x for x in universe if x not in red and x not in blue]
        neither_sum = sum(neither)
        
        print(f"\n🔴 RED TEAM ({len(red)} elements):")
        print(f"   Elements: {list(red)}")
        print(f"   Sum: {red_sum:,}")
        
        print(f"\n🔵 BLUE TEAM ({len(blue)} elements):")
        print(f"   Elements: {list(blue)}")
        print(f"   Sum: {blue_sum:,}")
        
        print(f"\n⚪ NEITHER ({len(neither)} elements):")
        print(f"   Elements: {neither}")
        print(f"   Sum: {neither_sum:,}")
        
        print(f"\n📊 VERIFICATION:")
        print(f"   Red - Blue = {red_sum:,} - {blue_sum:,} = {red_sum - blue_sum:,}")
        print(f"   Balanced: {'✓ YES' if red_sum == blue_sum else '✗ NO'}")
        print(f"   Total accounted: {len(red) + len(blue) + len(neither)}/{len(universe)}")
        print()
    
    # Summary statistics
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)
    
    # Analyze team sizes
    red_sizes = [len(red) for red, blue in results]
    blue_sizes = [len(blue) for red, blue in results]
    
    print(f"\nTotal balanced partitions found: {len(results)}")
    print(f"\nRed team sizes: min={min(red_sizes)}, max={max(red_sizes)}, avg={sum(red_sizes)/len(red_sizes):.1f}")
    print(f"Blue team sizes: min={min(blue_sizes)}, max={max(blue_sizes)}, avg={sum(blue_sizes)/len(blue_sizes):.1f}")
    
    # Find most balanced (equal team sizes)
    most_balanced = min(results, key=lambda x: abs(len(x[0]) - len(x[1])))
    print(f"\nMost balanced team sizes: {len(most_balanced[0])} vs {len(most_balanced[1])}")
    
    print("\n" + "=" * 60)
    print("💡 TIP: Access any result with results[index]")
    print("   Example: red, blue = results[0]")
    print("=" * 60)