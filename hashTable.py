# This class creates a chaining hash table to store all of the packages based off package ID.
class chainingHash:
    def __init__(self):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(10):
            self.table.append([])

    # Inserts a new item into the hash table.
    # space-time complexity O(n)
    def insert(self, key, item):  # does both insert and update
        # get the bucket list where this item will go.
        bucket = int(key) % len(self.table)
        bucket_list = self.table[bucket]

        # update key if it is already in the bucket
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                kv[1] = item
                return True

        # if not, insert the item to the end of the bucket list.
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.
    # space-time complexity O(n)
    def search(self, key):
        # get the bucket list where this key would be.
        bucket = int(key) % len(self.table)
        bucket_list = self.table[bucket]
        # print(bucket_list)

        # search for the key in the bucket list
        for kv in bucket_list:
            # print (key_value)
            if int(kv[0]) == int(key):
                return kv[1]  # value
        return None

    # Removes an item with matching key from the hash table.
    # space-time complexity O(n)
    def remove(self, key):
        # get the bucket list where this item will be removed from.
        bucket = int(key) % len(self.table)
        bucket_list = self.table[bucket]
        # remove the item from the bucket list if it is present.
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                self.table[bucket].remove([kv[0], kv[1]])
                return True

    # Returns the chaining hash table.
    def getTable(self):
        return self.table
