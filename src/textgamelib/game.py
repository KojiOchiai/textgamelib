from dataclasses import dataclass

@dataclass
class GameObject:
    """Base class representing a game object"""
    name: str
    description: str
    location: str | None = None

@dataclass 
class Room:
    """Class representing a location in the game"""
    id: str
    name: str
    description: str
    exits: dict[str, str] | None = None  # direction: destination room_id
    items: list[GameObject] | None = None

    def __post_init__(self) -> None:
        if self.exits is None:
            self.exits = {}
        if self.items is None:
            self.items = []

class Player:
    """Class representing the player"""
    def __init__(self, name: str) -> None:
        self.name = name
        self.inventory: list[GameObject] = []
        self.current_room: str | None = None

class Game:
    """Main class for managing the game state"""
    def __init__(self) -> None:
        self.rooms: dict[str, Room] = {}
        self.player: Player | None = None
        self.game_objects: dict[str, GameObject] = {}

    def add_room(self, room: Room) -> None:
        """Add a room to the game"""
        self.rooms[room.id] = room

    def add_object(self, obj: GameObject) -> None:
        """Add a game object to the game"""
        self.game_objects[obj.name] = obj

    def start_game(self, player_name: str, starting_room_id: str) -> None:
        """Initialize and start the game"""
        self.player = Player(player_name)
        self.player.current_room = starting_room_id

    def get_current_room(self) -> Room | None:
        """Get the room where the player is currently located"""
        if self.player and self.player.current_room:
            return self.rooms.get(self.player.current_room)
        return None

    def move_player(self, direction: str) -> bool:
        """Move the player in the specified direction"""
        current_room = self.get_current_room()
        if not current_room:
            return False
            
        next_room_id = current_room.exits.get(direction)
        if next_room_id:
            self.player.current_room = next_room_id
            return True
        return False



if __name__ == "__main__":
    # Create a few rooms
    room1 = Room(id="room1", name="Entrance Hall", description="A large hall with a grand staircase.")
    room2 = Room(id="room2", name="Library", description="A quiet room filled with books.")
    room3 = Room(id="room3", name="Kitchen", description="A room with a large dining table and a fireplace.")

    # Set exits for the rooms
    room1.exits = {"north": "room2"}
    room2.exits = {"south": "room1", "east": "room3"}
    room3.exits = {"west": "room2"}

    # Create a game object
    key = GameObject(name="key", description="A small rusty key.")

    # Initialize the game
    game = Game()

    # Add rooms to the game
    game.add_room(room1)
    game.add_room(room2)
    game.add_room(room3)

    # Add object to the game
    game.add_object(key)

    # Start the game with a player
    game.start_game(player_name="Hero", starting_room_id="room1")

    # Test moving the player and show room descriptions
    current_room = game.get_current_room()
    print(f"Current Room: {current_room.name} - {current_room.description}")
    
    if game.move_player("north"):
        current_room = game.get_current_room()
        print(f"Moved north to: {current_room.name} - {current_room.description}")
    else:
        print("Cannot move north.")

    if game.move_player("east"):
        current_room = game.get_current_room()
        print(f"Moved east to: {current_room.name} - {current_room.description}")
    else:
        print("Cannot move east.")

    if game.move_player("west"):
        current_room = game.get_current_room()
        print(f"Moved west to: {current_room.name} - {current_room.description}")
    else:
        print("Cannot move west.")
