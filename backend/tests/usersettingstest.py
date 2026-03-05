# Madison Boyd
#Iteration 3
#CSC 405
#3/2/2025


import unittest
# We use absolute imports starting from the root 'backend'
from backend.services.usersettings import update_wishlist, get_settings

class TestUserSettings(unittest.TestCase):
    
    def test_add_wishlist(self):
        """Test that we can add an item to the wishlist."""
        # Clean slate: clear history for a pure test
        settings = get_settings()
        settings.wishlist.clear() 
        
        # Test adding a new item
        result = update_wishlist("New Gadget")
        self.assertTrue(result)
        self.assertIn("New Gadget", settings.wishlist)

    def test_duplicate_wishlist(self):
        """Test that adding a duplicate returns False."""
        settings = get_settings()
        settings.wishlist.clear()
        
        update_wishlist("New Gadget")
        # Try adding the same item again
        result = update_wishlist("New Gadget")
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
