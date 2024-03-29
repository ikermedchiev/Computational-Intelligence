import enum


# Enum representing the directions an ant can take.
class Direction(enum.Enum):
    east = 0
    north = 1
    west = 2
    south = 3

    # Direction to an int.
    # @param dir the direction.
    # @return an integer from 0-3.
    @classmethod
    def dir_to_int(cls, dir):
        return dir.value
    
    @classmethod
    def inv_dir(cls, dir):
        newval = (dir.value + 2) % 4
        return Direction(newval)


