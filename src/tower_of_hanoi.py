def hanoi_solver(n):
    """
    Solves the Tower of Hanoi puzzle for n disks.
    Tracks and returns every intermediate game state as a multiline string.
    """
    # 1. Initialize rods. The source rod ('A') gets disks stacked from largest 
    # to smallest, e.g., if n=3, rods['A'] = [3, 2, 1] (top disk is at index -1)
    rods = {
        'A': list(range(n, 0, -1)),
        'B': [],
        'C': []
    }
    
    states = []

    def save_state():
        """Captures a snapshot representation of all 3 rods and saves it."""
        state_str = f"{rods['A']} {rods['B']} {rods['C']}"
        states.append(state_str)

    def _solve(disks, source, destination, auxiliary):
        """
        Recursive helper function that moves a specified number of disks 
        from a source rod to a destination rod using an auxiliary rod.
        """
        # Base Case: When moving only 1 disk, shift it directly to destination
        if disks == 1:
            disk = rods[source].pop()      # Pop from top of source
            rods[destination].append(disk) # Push onto destination
            save_state()                   # Log the board update
            return

        # Recursive Step: 
        # 1. Move n-1 disks out of the way (from source to auxiliary)
        _solve(disks - 1, source, auxiliary, destination)
        
        # 2. Move the largest remaining single disk from source to destination
        disk = rods[source].pop()
        rods[destination].append(disk)
        save_state()
        
        # 3. Move the n-1 disks back on top of the largest disk (auxiliary to destination)
        _solve(disks - 1, auxiliary, destination, source)

    # Capture the starting layout before any moves are made
    save_state()
    
    # Run the recursive puzzle solver only if there are disks present
    if n > 0:
        _solve(n, source='A', destination='C', auxiliary='B')
        
    # Return all intermediate state configurations joined by newlines
    return "\n".join(states)

# Print raw output representation to inspect newline breaks clearly
print(repr(hanoi_solver(2)))
