import unittest

from artworks_core import format_artworks_by_params


class TestFormatArtworksByParams(unittest.IsolatedAsyncioTestCase):

    async def test_empty_data(self):
        """Test when data is empty."""
        result = await format_artworks_by_params([], {'sort': ['date_asc']})
        self.assertEqual(result, [])

    async def test_no_sort_param(self):
        """Test when no sort parameter is provided."""
        data = [{"title": "Artwork A"}, {"title": "Artwork B"}]
        result = await format_artworks_by_params(data, {})
        self.assertEqual(result, data)

    async def test_sort_by_date_asc(self):
        """Test sorting by date ascending."""
        data = [
            {"title": "Artwork A", "date_start": 2000},
            {"title": "Artwork B", "date_start": 1990},
        ]
        result = await format_artworks_by_params(data, {'sort': ['date_asc']})
        self.assertEqual(result, [
            {"title": "Artwork B", "date_start": 1990},
            {"title": "Artwork A", "date_start": 2000},
        ])

    async def test_sort_by_date_desc(self):
        """Test sorting by date descending."""
        data = [
            {"title": "Artwork A", "date_start": 2000},
            {"title": "Artwork B", "date_start": 1990},
        ]
        result = await format_artworks_by_params(data, {'sort': ['date_desc']})
        self.assertEqual(result, [
            {"title": "Artwork A", "date_start": 2000},
            {"title": "Artwork B", "date_start": 1990},
        ])

    async def test_sort_by_title_asc(self):
        """Test sorting by title ascending."""
        data = [
            {"title": "B Artwork"},
            {"title": "A Artwork"},
        ]
        result = await format_artworks_by_params(data, {'sort': ['title_asc']})
        self.assertEqual(result, [
            {"title": "A Artwork"},
            {"title": "B Artwork"},
        ])

    async def test_invalid_sort_type(self):
        """Test when an invalid sort type is provided."""
        data = [
            {"title": "B Artwork"},
            {"title": "A Artwork"},
        ]
        result = await format_artworks_by_params(data, {'sort': ['invalid_type']})
        self.assertEqual(result, data)

if __name__ == "__main__":
    unittest.main()
