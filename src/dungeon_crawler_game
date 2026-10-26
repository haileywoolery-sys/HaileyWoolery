import random
import os

# --- GAME CONFIGURATION ---
MAP_WIDTH = 40
MAP_HEIGHT = 15
MAX_ROOMS = 6
ROOM_MIN_SIZE = 4
ROOM_MAX_SIZE = 8

# Tile representations
TILE_EMPTY = " "
TILE_WALL = "#"
TILE_FLOOR = "."
TILE_DOOR_LOCKED = "X"
TILE_DOOR_OPEN = "E"

class Room:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return center_x, center_y

    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

class Item:
    def __init__(self, x, y, item_type):
        self.x = x
        self.y = y
        self.item_type = item_type
        if item_type == "potion":
            self.symbol = "!"
        elif item_type == "sword":
            self.symbol = "/"
        elif item_type == "dungeon_key":
            self.symbol = "K"
        elif item_type == "dragon_blade":
            self.symbol = "B"

class GameCharacter:
    def __init__(self, x, y, name, health, max_health, attack, symbol=None):
        self.x = x
        self.y = y
        self.name = name
        self.health = health
        self.max_health = max_health
        self.attack = attack
        self.symbol = symbol if symbol else name[0]
        self.has_key = False

    def is_alive(self):
        return self.health > 0

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def level_up(self):
        self.max_health += 15
        self.health = self.max_health
        self.attack += 3

class DungeonCrawler:
    def __init__(self):
        self.dungeon_level = 1
        self.player = None
        self.player_inventory = {"potion": 0, "sword": 0, "dungeon_key": 0, "dragon_blade": 0}
        self.door_x = None
        self.door_y = None
        self.door_open = False
        
        self.generate_dungeon_floor()

    def generate_dungeon_floor(self):
        self.map_data = [[TILE_WALL for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        self.rooms = []
        self.monsters = []
        self.items = []
        self.door_open = False
        self.log_messages = [f"Entered Floor {self.dungeon_level}! Loot items and clear enemies."]

        # Determine if this level is a milestone Boss Floor or a Key Floor for the next Boss
        self.is_boss_floor = (self.dungeon_level % 10 == 0)
        self.is_key_floor = (self.dungeon_level % 10 == 9)
        
        if self.is_boss_floor:
            self.log_messages = [f" FLOOR {self.dungeon_level}: THE DRAGON'S LAIR! Prepare yourself!"]
        elif self.is_key_floor:
            self.log_messages = [f" FLOOR {self.dungeon_level}: A minion holds a key. Find it to unlock the boss floor!"]
        else:
            self.log_messages = [f"Entered Floor {self.dungeon_level}! Clear enemies to open the door."]
        
        # 1. Procedural room generation
        for _ in range(MAX_ROOMS):
            w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            x = random.randint(1, MAP_WIDTH - w - 2)
            y = random.randint(1, MAP_HEIGHT - h - 2)

            new_room = Room(x, y, w, h)
            if any(new_room.intersect(other) for other in self.rooms):
                continue

            self.create_room(new_room)

            if len(self.rooms) > 0:
                prev_x, prev_y = self.rooms[-1].center()
                new_x, new_y = new_room.center()
                if random.random() < 0.5:
                    self.create_h_tunnel(prev_x, new_x, prev_y)
                    self.create_v_tunnel(prev_y, new_y, new_x)
                else:
                    self.create_v_tunnel(prev_y, new_y, prev_x)
                    self.create_h_tunnel(prev_x, new_x, new_y)

            self.rooms.append(new_room)

        # 2. Setup Player Location
        start_x, start_y = self.rooms[0].center()
        if self.player is None:
            self.player = GameCharacter(start_x, start_y, "Hero", 100, 100, 15)
        else:
            self.player.x = start_x
            self.player.y = start_y

        # 3. Setup Escape Door Location
        self.door_x, self.door_y = self.rooms[-1].center()
        self.map_data[self.door_y][self.door_x] = TILE_DOOR_LOCKED

        # 4. Populate monsters and items based on floor type
        if self.is_boss_floor:
            #spawn Boss Dragon in boss room
            bx, by = self.rooms[len(self.rooms) // 2].center()
            boss_health = 150 + (self.dungeon_level * 5)
            boss_attack = 18 + (self.dungeon_level // 2)
            self.monsters.append(GameCharacter(bx, by, "Boss Dragon", boss_health, boss_health, boss_attack, "D"))
        else:
            # Spawn Monsters in intermediate rooms
            monster_types = [("Orc", 30, 6), ("Goblin", 15, 4), ("Troll", 50, 10)]
            for room in self.rooms[1:-1]:
                mx, my = room.center()
                m_name, m_hp, m_atk = random.choice(monster_types)
                scale = 1 + (self.dungeon_level * 0.1)
                self.monsters.append(GameCharacter(mx, my, m_name, int(m_hp * scale), int(m_hp * scale), int(m_atk * scale)))

                
                if random.random() < 0.25:
                    # 25% chance for a room to spawn a loose floor item nearby
                    item_type = "potion" if random.random() < 0.7 else "sword"
                    self.items.append(Item(mx + 1, my, item_type))

            if self.is_key_floor and self.monsters:
                # Spawn a key on a random monster for the next boss floor
                key_holder = random.choice(self.monsters)
                key_holder.has_key = True

            self.check_door_status()

    def create_room(self, room):
        for y in range(room.y1, room.y2):
            for x in range(room.x1, room.x2):
                self.map_data[y][x] = TILE_FLOOR

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.map_data[y][x] = TILE_FLOOR

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.map_data[y][x] = TILE_FLOOR

    def check_door_status(self):
        if not self.door_open and not any(m.is_alive() for m in self.monsters):
            if not self.door_open:
                self.door_open = True
                self.map_data[self.door_y][self.door_x] = TILE_DOOR_OPEN
                if self.is_boss_floor:
                    self.add_log("The Dragon has been slain! The exit door snaps open!")
                else:
                    self.add_log("A loud grinding sound echoes... The exit door is now open!")

        # no key dropped yet, so the door remains locked for the next boss floor
        if self.is_key_floor:
            has_key_on_floor = any(item.item_type == "dungeon_key" for item in self.items)
            has_key_monster = any((m.has_key and m.is_alive()) for m in self.monsters)

            if self.player_inventory["dungeon_key"] == 0 and not has_key_on_floor and not has_key_monster:
                spawn_x = self.door_x - 1 if self.map_data[self.door_y][self.door_x - 1] == TILE_FLOOR else self.door_x
                self.items.append(Item(spawn_x, self.door_y, "dungeon_key"))
                self.add_log("A Dungeon Key has appeared near the exit door! Pick it up to unlock the next Boss Floor!")
            
    def add_log(self, text):
        self.log_messages.append(text)
        if len(self.log_messages) > 4:
            self.log_messages.pop(0)

    def draw_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        display_map = [row[:] for row in self.map_data]

        for item in self.items:
            display_map[item.y][item.x] = item.symbol  # Show item symbol
        
        # Draw monsters on top of items
        for m in self.monsters:
            if m.is_alive():
                display_map[m.y][m.x] = m.symbol

        # Draw player on top
        if self.player.is_alive():
            display_map[self.player.y][self.player.x] = self.player.symbol

        for row in display_map:
            print("".join(row))

        print("─" * MAP_WIDTH)
        print(f" Floor: {self.dungeon_level} | HP: {self.player.health}/{self.player.max_health} | Attack: {self.player.attack}")
        print("─" * MAP_WIDTH)
        for msg in self.log_messages:
            print(f"> {msg}")

    def handle_turn(self, action):
        dx, dy = 0, 0
        if action == 'w': dy = -1
        elif action == 's': dy = 1
        elif action == 'a': dx = -1
        elif action == 'd': dx = 1
        else: return

        new_x = self.player.x + dx
        new_y = self.player.y + dy

        # 1. Combat check against alive monsters/bosses
        target_monster = next((m for m in self.monsters if m.x == new_x and m.y == new_y and m.is_alive()), None)
        
        if target_monster:
            damage = random.randint(self.player.attack - 3, self.player.attack + 3)
            target_monster.take_damage(damage)
            self.add_log(f"You strike {target_monster.name} for {damage} damage!")
            
            if not target_monster.is_alive():
                self.add_log(f"You vanquished the {target_monster.name}!")

                # check key drops 
                if target_monster.has_key:
                    self.items.append(Item(target_monster.x, target_monster.y, "dungeon_key"))
                    self.add_log(f"The {target_monster.name} dropped a Dungeon Key! You can now unlock the next Boss Floor!")

                # Boss Drop mechanics
                if target_monster.name == "Boss Dragon":
                    self.items.append(Item(target_monster.x, target_monster.y, "dragon_blade"))
                    self.add_log("The Boss Dragon dropped the legendary Dragon Blade! Your attack has increased significantly!")
                
                # Monster loot drop mechanics (50% chance to drop an item right where they died)
                if random.random() < 0.5:
                    drop_type = "potion" if random.random() < 0.7 else "sword"
                    self.items.append(Item(target_monster.x, target_monster.y, drop_type))
                    self.add_log(f"The {target_monster.name} dropped a shiny object!")
                
                self.check_door_status()
            
            self.run_enemy_turn()
            return

        # 2. Door Intercept and Progression Logic
        if new_x == self.door_x and new_y == self.door_y:
            if self.door_open:
                # Boss floor progression logic
                if (self.dungeon_level + 1) % 10 == 0:
                    if self.player_inventory["dungeon_key"] >= 1:
                        self.player_inventory["dungeon_key"] -= 1
                        self.add_log("You used a Dungeon Key to unlock the Boss Floor!")
                    else:
                        self.add_log("Gate is sealed. A Dungeon Key is required to unlock the Boss Floor!")
                        return
                    
                self.dungeon_level += 1
                self.player.level_up()
                self.generate_dungeon_floor()
                return
            else:
                self.add_log("The door is magically sealed. Defeat all monsters first.")
                return

        # 3. Environment Navigation Movement
        if self.map_data[new_y][new_x] in (TILE_FLOOR, TILE_DOOR_OPEN):
            self.player.x = new_x
            self.player.y = new_y

            # 4. Item pickup tracking
            standing_on_item = next((item for item in self.items if item.x == self.player.x and item.y == self.player.y), None)
            if standing_on_item:
                if standing_on_item.item_type == "potion":
                    heal_amt = 30
                    self.player.health = min(self.player.max_health, self.player.health + heal_amt)
                    self.add_log(f"You drank a Health Potion and restored {heal_amt} HP!")
                elif standing_on_item.item_type == "sword":
                    atk_bonus = 4
                    self.player.attack += atk_bonus
                    self.add_log(f"You found a sharper Sword! Attack increased by +{atk_bonus}!")
                elif standing_on_item.item_type == "dragon_blade":
                    atk_bonus = 10
                    self.player.attack += atk_bonus
                    self.add_log(f"You wield a legendary Dragon Blade! Attack increased by +{atk_bonus}!")
                elif standing_on_item.item_type == "dungeon_key":
                    self.player_inventory["dungeon_key"] += 1
                    self.add_log("You picked up a Dungeon Key! Use it to unlock the next Boss Floor!")  
                
                # Remove item from floor tracking index
                self.items.remove(standing_on_item)

        else:
            self.add_log("The wall blocks your path.")

        # 5. Enemy Response Turns
        self.run_enemy_turn()

    def run_enemy_turn(self):
        for m in self.monsters:
            if m.is_alive():
                # Boss Dragon has extended sensory range of 8 tiles 
                aggro_range = 8 if m.name == "Boss Dragon" else 5

                if abs(m.x - self.player.x) <= aggro_range and abs(m.y - self.player.y) <= aggro_range:
                    if abs(m.x - self.player.x) + abs(m.y - self.player.y) == 1:
                        # Boss Dragon special attack chance
                        if m.name == "Boss Dragon" and random.random() < 0.4:
                            m_dmg = random.randint(m.attack, m.attack + 6)
                            self.player.take_damage(m_dmg)
                            self.add_log(f"{m.name} breathes fire on you for {m_dmg} fire damage!")
                        else:
                            # Regular monster attack
                            m_dmg = random.randint(m.attack - 1, m.attack + 2)
                            self.player.take_damage(m_dmg)
                            self.add_log(f"{m.name} hits you for {m_dmg} damage!")

                        self.player.take_damage(m_dmg)
                    
                    else:
                        mx_step = 1 if self.player.x > m.x else -1 if self.player.x < m.x else 0
                        my_step = 1 if self.player.y > m.y else -1 if self.player.y < m.y else 0

                        next_mx = m.x + mx_step
                        next_my = m.y + my_step

                        # stops monsters from moving into the player's space
                        if next_mx == self.player.x and next_my == self.player.y:
                            continue

                        other_monster_occupancy = any(
                            other_m.x == next_mx and other_m.y == next_my and other_m.is_alive()
                            for other_m in self.monsters
                            if other_m != m
                        )
                        if other_monster_occupancy:
                            continue

                        if self.map_data[next_my][next_mx] == TILE_FLOOR:
                            m.x = next_mx
                            m.y = next_my

    def run(self):
        while self.player.is_alive():
            self.draw_screen()
            try:
                user_input = input("\nMove (WASD) or 'q' to quit: ").lower().strip()
                if user_input == 'q':
                    print("Exiting dungeon... Goodbye!")
                    break
                if user_input:
                    self.handle_turn(user_input)
            except (KeyboardInterrupt, EOFError):
                break
        else:
            self.draw_screen()
            print(f"\n💀 Game Over! You perished on Floor {self.dungeon_level}. 💀")

if __name__ == "__main__":
    game = DungeonCrawler()
    game.run()
