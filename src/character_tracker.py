class GameCharacter:
    """
    Represents a playable character in a game, tracking attributes like 
    level, experience points (XP), health, and mana using secure properties.
    """
    def __init__(self, name, char_class="warrior"):
        # Private/protected backing attributes initialization
        self._name = name
        self.char_class = char_class.lower()  # Stores class in lowercase for easier checking
        self._level = 1
        self.xp = 0
        self._mana = 50
        self._health = 100
        
        # Configure class-specific baseline combat statistics
        if self.char_class == "warrior":
            self.max_hp = 120
            self.attack = 15
            self.defense = 10
        elif self.char_class == "mage":
            self.max_hp = 80
            self.attack = 20
            self.defense = 4
        else:  # Default/Fallback class setup (e.g., rogue or custom)
            self.max_hp = 100
            self.attack = 12
            self.defense = 7

        # Initialize current vital pools utilizing the boundary-checking setters
        self.health = self.max_hp  # Sets health to the class max instead of hardcoded 100
        self.mana = self._mana

    @property
    def name(self):
        """Read-only property for the character's name."""
        return self._name

    @property
    def level(self):
        """Property getter that securely returns the current level."""
        return self._level

    @property
    def max_mana(self):
        """Read-only property representing the maximum allowable mana pool."""
        return 50

    @property
    def health(self):
        """Getter for current health."""
        return self._health

    @health.setter
    def health(self, value):
        """Setter that keeps health securely bounded between 0 and the class max_hp."""
        self._health = max(0, min(value, self.max_hp))

    @property
    def mana(self):
        """Getter for current mana."""
        return self._mana

    @mana.setter
    def mana(self, value):
        """Setter that keeps mana securely bounded between 0 and max_mana (50)."""
        self._mana = max(0, min(value, self.max_mana))

    def gain_xp(self, amount):
        """
        Adds XP to the character's pool. If the accumulated XP meets or 
        exceeds the level threshold, triggers a level up.
        """
        self.xp += amount
        print(f"\n✨ {self.name} gained {amount} XP!")
        
        # Progression formula: Level 1 requires 100 XP, Level 2 requires 200 XP, etc.
        xp_needed = self._level * 100
        if self.xp >= xp_needed:
            self.xp -= xp_needed  # Carry over leftover XP to the next level threshold
            self.level_up()  

    def level_up(self):
        """
        Increments the character's level by 1, permanently raises structural stats, 
        and completely restores health and mana.
        """
        self._level = self._level + 1
            
        # Permanent stat scaling rewards
        self.max_hp += 15
        self.attack += 3
        self.defense += 2
        
        # Complete pool restoration upon level up
        self.health = self.max_hp  
        self.mana = self.max_mana  
        
        print(f"🎉 {self.name} leveled up to level {self.level}!")

    def __str__(self):
        """Returns a basic text overview of the character's current state."""
        return f"Name: {self.name}\nLevel: {self.level}\nHealth: {self.health}/{self.max_hp}\nMana: {self.mana}/{self.max_mana}"

    def display_stats(self):
        """Prints the string representation of the character to the console."""
        print(self) 


# --- Quick Demonstration ---
if __name__ == "__main__":
    # Create a warrior instance (will leverage the fixed variable configuration)
    hero = GameCharacter(name="Aragorn", char_class="warrior")
    print(hero)  

    # Simulate earning enough progression points to level up
    hero.gain_xp(150)
    hero.display_stats()

    print("\n💥 Simulating damage and healing limits...")
    # Attempting to drop values beneath absolute zero floor limits
    hero.health -= 150  
    hero.mana -= 100
    print(f"After massive drops -> HP: {hero.health}, Mana: {hero.mana}")

    # Attempting to inflate values beyond ceiling maximum limits
    hero.health += 500  
    hero.mana += 500
    print(f"After massive gains -> HP: {hero.health}, Mana: {hero.mana}")
