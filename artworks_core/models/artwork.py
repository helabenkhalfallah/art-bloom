from tortoise import Model, fields


class Artwork(Model):
    """
    Represents an artwork entity in the database.

    Fields:
        - id (IntField): Primary key identifier for the artwork.
        - title (TextField): Title or name of the artwork.
        - artist_title (TextField): Name of the artist who created the artwork.
        - place_of_origin (TextField): Geographic location where the artwork originated.
        - thumbnail (TextField): URL of the artwork's thumbnail image.
        - date_start (IntField): Year the artwork was started (e.g., 1870).
        - date_end (IntField): Year the artwork was completed (e.g., 1875).
        - date_display (TextField): Human-readable date range for the artwork (e.g., "1870-1875").
        - artist_display (TextField): Detailed information about the artist.
        - description (TextField): Full description of the artwork.
        - short_description (TextField): Brief summary of the artwork.
        - classification_title (TextField): Classification category for the artwork (e.g., "Painting").
        - style_title (TextField): Artistic style of the artwork (e.g., "Impressionism").
        - medium_display (TextField): Medium or materials used in the artwork (e.g., "Oil on canvas").
        - material_titles (JSONField): List of materials used (e.g., ["Oil", "Canvas"]).
        - term_titles (JSONField): Related terms or tags (e.g., ["Starry Night", "Van Gogh"]).
        - category_titles (JSONField): Categories associated with the artwork (e.g., ["Fine Art"]).

    Methods:
        - __str__(): Returns a string representation of the artwork.
        - to_dict(): Converts the artwork instance into a dictionary for serialization.
    """

    id = fields.IntField(pk=True)  # Primary key
    title = fields.TextField(null=True)  # Title of the artwork
    artist_title = fields.TextField(null=True)  # Artist's name
    place_of_origin = fields.TextField(null=True)  # Place of origin
    thumbnail = fields.TextField(null=True)  # Thumbnail URL
    date_start = fields.IntField(null=True)  # Start year (e.g., 1870)
    date_end = fields.IntField(null=True)  # End year (e.g., 1875)
    date_display = fields.TextField(null=True)  # Human-readable date (e.g., "1870-1875")
    artist_display = fields.TextField(null=True)  # Additional artist information
    description = fields.TextField(null=True)  # Detailed description of the artwork
    short_description = fields.TextField(null=True)  # Short summary
    classification_title = fields.TextField(null=True)  # Classification (e.g., "Painting")
    style_title = fields.TextField(null=True)  # Artistic style (e.g., "Impressionism")
    medium_display = fields.TextField(null=True)  # Medium used (e.g., "Oil on canvas")
    material_titles = fields.JSONField(null=True)  # List of materials used (stored as JSON)
    term_titles = fields.JSONField(null=True)  # Related terms or tags (stored as JSON)
    category_titles = fields.JSONField(null=True)  # Categories (stored as JSON)

    def __str__(self):
        """
        Returns a string representation of the artwork.

        Returns:
            str: A string in the format "title by artist_title".
        """
        return f"{self.title} by {self.artist_title}"

    def to_dict(self):
        """
        Converts the Artwork instance into a dictionary for JSON serialization.

        Returns:
            dict: A dictionary representation of the artwork with all fields.
        """
        return {
            "id": self.id,
            "title": self.title,
            "artist_title": self.artist_title,
            "place_of_origin": self.place_of_origin,
            "thumbnail": self.thumbnail,
            "date_start": self.date_start,
            "date_end": self.date_end,
            "date_display": self.date_display,
            "artist_display": self.artist_display,
            "description": self.description,
            "short_description": self.short_description,
            "classification_title": self.classification_title,
            "style_title": self.style_title,
            "medium_display": self.medium_display,
            "material_titles": self.material_titles,
            "term_titles": self.term_titles,
            "category_titles": self.category_titles,
        }
