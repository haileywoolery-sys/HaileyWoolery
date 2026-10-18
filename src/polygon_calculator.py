class Rectangle:
    """
    Represents a standard 2D Rectangle shape. 
    Provides geometric calculations and text-based visualizations.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def set_width(self, width):
        """Updates the rectangle's horizontal width."""
        self.width = width

    def set_height(self, height):
        """Updates the rectangle's vertical height."""
        self.height = height

    def get_area(self):
        """Calculates Area: width * height."""
        return self.width * self.height

    def get_perimeter(self):
        """Calculates Perimeter: 2 * (width + height)."""
        return 2 * (self.width + self.height)

    def get_diagonal(self):
        """Calculates Diagonal: Uses the Pythagorean theorem √(w² + h²)."""
        return ((self.width ** 2) + (self.height ** 2)) ** 0.5

    def get_picture(self):
        """
        Returns a string representation of the rectangle using asterisks (*).
        Returns a warning string if dimensions exceed 50 units.
        """
        if self.width > 50 or self.height > 50:
            return "Too big for picture."
        
        # Build one row of asterisks followed by a newline character
        single_line = "*" * self.width + "\n"
        # Duplicate that row vertically by multiplying it by the height
        return single_line * self.height

    def get_amount_inside(self, shape):
        """
        Calculates how many times another shape can cleanly fit inside this one 
        without being rotated. Uses integer division (//).
        """
        # Determine how many columns and rows of the smaller shape can fit
        horizontal_fit = self.width // shape.width
        vertical_fit = self.height // shape.height
        # Total capacity is columns multiplied by rows
        return horizontal_fit * vertical_fit

    def __str__(self):
        """Returns the formal string formatting for a Rectangle instance."""
        return f"Rectangle(width={self.width}, height={self.height})"


class Square(Rectangle):
    """
    Represents a Square, inheriting core behavior from Rectangle.
    Overrides setters to ensure that width and height always stay identical.
    """
    def __init__(self, side):
        # Passes the single side length as both width and height to the parent Rectangle class
        super().__init__(side, side)

    def set_side(self, side):
        """Simultaneously updates both sides of the square to keep them equal."""
        self.width = side
        self.height = side

    def set_width(self, width):
        """Overrides Rectangle behavior: Changing width automatically updates height."""
        self.set_side(width)

    def set_height(self, height):
        """Overrides Rectangle behavior: Changing height automatically updates width."""
        self.set_side(height)

    def __str__(self):
        """Overrides standard Rectangle string to present as a distinct Square instance."""
        return f"Square(side={self.width})"
