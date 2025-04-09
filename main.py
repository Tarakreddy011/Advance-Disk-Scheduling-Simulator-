import matplotlib.pyplot as plt
from collections import deque

# FCFS Algorithm - Unchanged as it's already straightforward
def fcfs(requests, head):
    total_seek = 0
    order = [head]
    current = head
    for request in requests:
        total_seek += abs(request - current)
        order.append(request)
        current = request
    return order, total_seek

# SSTF Algorithm - Using priority queue approach
def sstf(requests, head):
    total_seek = 0
    order = [head]
    current = head
    req_queue = requests.copy()
    
    while req_queue:
        # Find request with minimum seek time
        closest = None
        min_seek = float('inf')
        for req in req_queue:
            seek = abs(req - current)
            if seek < min_seek:
                min_seek = seek
                closest = req
        total_seek += min_seek
        order.append(closest)
        current = closest
        req_queue.remove(closest)
    
    return order, total_seek

# SCAN Algorithm - Using two separate lists for each direction
def scan(requests, head, direction="right", max_cylinder=199):
    total_seek = 0
    order = [head]
    current = head
    
    left_requests = sorted([r for r in requests if r <= head])
    right_requests = sorted([r for r in requests if r > head])
    
    if direction == "right":
        # Move right first
        for req in right_requests:
            total_seek += abs(req - current)
            order.append(req)
            current = req
        # If we have requests beyond, go to end
        if right_requests and current != max_cylinder:
            total_seek += abs(max_cylinder - current)
            order.append(max_cylinder)
            current = max_cylinder
        # Then move left
        for req in reversed(left_requests):
            total_seek += abs(req - current)
            order.append(req)
            current = req
    else:
        # Move left first
        for req in reversed(left_requests):
            total_seek += abs(req - current)
            order.append(req)
            current = req
        # If we have requests beyond, go to start
        if left_requests and current != 0:
            total_seek += abs(0 - current)
            order.append(0)
            current = 0
        # Then move right
        for req in right_requests:
            total_seek += abs(req - current)
            order.append(req)
            current = req
    
    return order, total_seek

# C-SCAN Algorithm - Using circular approach
def cscan(requests, head, direction="right", max_cylinder=199):
    total_seek = 0
    order = [head]
    current = head
    
    # Split requests into two parts
    if direction == "right":
        first_part = sorted([r for r in requests if r >= head])
        second_part = sorted([r for r in requests if r < head])
    else:
        first_part = sorted([r for r in requests if r <= head], reverse=True)
        second_part = sorted([r for r in requests if r > head], reverse=True)
    
    # Process first part
    for req in first_part:
        total_seek += abs(req - current)
        order.append(req)
        current = req
    
    # Handle the jump to the other end
    if direction == "right":
        if current != max_cylinder:
            total_seek += abs(max_cylinder - current)
            order.append(max_cylinder)
        total_seek += max_cylinder  # jump from max to 0
        order.append(0)
        current = 0
    else:
        if current != 0:
            total_seek += abs(0 - current)
            order.append(0)
        total_seek += max_cylinder  # jump from 0 to max
        order.append(max_cylinder)
        current = max_cylinder
    
    # Process second part
    for req in second_part:
        total_seek += abs(req - current)
        order.append(req)
        current = req
    
    return order, total_seek

# LOOK Algorithm - Added as a bonus (similar to SCAN but doesn't go to the end)
def look(requests, head, direction="right", max_cylinder=199):
    total_seek = 0
    order = [head]
    current = head
    
    left_requests = sorted([r for r in requests if r <= head])
    right_requests = sorted([r for r in requests if r > head])
    
    if direction == "right":
        # Move right to the highest request
        for req in right_requests:
            total_seek += abs(req - current)
            order.append(req)
            current = req
        # Then move left to the lowest request
        for req in reversed(left_requests):
            total_seek += abs(req - current)
            order.append(req)
            current = req
    else:
        # Move left to the lowest request
        for req in reversed(left_requests):
            total_seek += abs(req - current)
            order.append(req)
            current = req
        # Then move right to the highest request
        for req in right_requests:
            total_seek += abs(req - current)
            order.append(req)
            current = req
    
    return order, total_seek

# Visualization Function - Enhanced with more details
def plot_movement(order, head, algorithm_name):
    plt.figure(figsize=(12, 6))
    
    # Plot the movement path
    plt.plot(order, marker='o', linestyle='-', label='Head Movement')
    
    # Mark important points
    plt.scatter([0], [head], color='red', s=100, label='Start Position')
    plt.scatter([len(order)-1], [order[-1]], color='green', s=100, label='End Position')
    
    # Add seek distance annotations
    for i in range(1, len(order)):
        x1, x2 = i-1, i
        y1, y2 = order[i-1], order[i]
        plt.annotate(f'{abs(y2-y1)}', 
                    xy=((x1+x2)/2, (y1+y2)/2),
                    xytext=(0, 5), 
                    textcoords='offset points',
                    ha='center')
    
    plt.title(f"Disk Head Movement ({algorithm_name})\nTotal Seek: {sum(abs(order[i]-order[i-1]) for i in range(1, len(order)))}")
    plt.xlabel("Step Number")
    plt.ylabel("Cylinder Number")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Main Program with more options
def main():
    requests = [98, 183, 37, 122, 14, 124, 65, 67]
    head = 53
    
    print("Disk Scheduling Algorithms")
    print("Initial Head Position:", head)
    print("Request Queue:", requests)
    print("\nSelect Algorithm:")
    print("1. First-Come-First-Serve (FCFS)")
    print("2. Shortest Seek Time First (SSTF)")
    print("3. SCAN (Elevator Algorithm)")
    print("4. C-SCAN (Circular SCAN)")
    print("5. LOOK (Improved SCAN)")
    
    choice = int(input("Enter your choice (1-5): "))
    
    algorithms = {
        1: ("FCFS", fcfs),
        2: ("SSTF", sstf),
        3: ("SCAN", scan),
        4: ("C-SCAN", cscan),
        5: ("LOOK", look)
    }
    
    if choice not in algorithms:
        print("Invalid choice!")
        return
    
    name, algorithm = algorithms[choice]
    
    if choice in [3, 4, 5]:
        direction = input("Enter initial direction (left/right): ").lower()
        if direction not in ['left', 'right']:
            direction = 'right'
        order, total_seek = algorithm(requests, head, direction)
        name = f"{name} ({direction})"
    else:
        order, total_seek = algorithm(requests, head)
    
    print("\nResults:")
    print("Processing Order:", order)
    print("Total Seek Time:", total_seek)
    print("Average Seek Time:", total_seek / len(requests))
    
    plot_movement(order, head, name)

if __name__ == "__main__":
    main()