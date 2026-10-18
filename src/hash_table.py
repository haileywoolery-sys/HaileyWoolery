class HashTable:
    """
    A custom implementation of a Hash Table data structure.
    Uses separate chaining (via nested dictionaries) to handle hash collisions.
    """
    def __init__(self):
        # The primary storage. Maps numerical hash keys to a secondary dictionary:
        # { hash_key: { original_string_key: value } }
        self.collection = {}

    def hash(self, key: str) -> int:
        """
        A basic hashing function.
        Sums up the ASCII code values of every character in the key string.
        """
        hash_value = 0
        for char in key:
            hash_value += ord(char)  # ord() gets the integer ASCII/Unicode value of a character
        return hash_value

    def add(self, key: str, value) -> None:
        """
        Inserts a key-value pair into the hash table.
        If a collision occurs, it appends to the inner dictionary.
        """
        hash_key = self.hash(key)
        
        # If this hash value hasn't been generated before, initialize an inner bucket (dictionary)
        if hash_key not in self.collection:
            self.collection[hash_key] = {}
            
        # Store the value inside the bucket mapped directly to the original un-hashed key string
        self.collection[hash_key][key] = value

    def remove(self, key: str) -> None:
        """
        Removes a key-value pair from the hash table by its original string key.
        Cleans up empty buckets to optimize memory management.
        """
        hash_key = self.hash(key)
        
        # Check if the bucket exists
        if hash_key in self.collection:
            # Check if the specific key string exists within that bucket
            if key in self.collection[hash_key]:
                del self.collection[hash_key][key]
                
                # Memory cleanup: If the collision bucket is now completely empty, delete it
                if not self.collection[hash_key]:
                    del self.collection[hash_key]

    def lookup(self, key: str):
        """
        Searches the hash table for a specific string key.
        Returns the associated value if found, or None if it doesn't exist.
        """
        hash_key = self.hash(key)
        
        # Verify both the bucket index and the precise string key exist before extracting
        if hash_key in self.collection and key in self.collection[hash_key]:
            return self.collection[hash_key][key]
        return None
