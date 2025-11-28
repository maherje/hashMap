# Name: Jeffrey Maher
# OSU Email: maherje@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6
# Due Date: August 13, 2024
# Description: Implement Hash Map classes utilizing 1)Chaining and 2)Open Addressing.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Takes a key and value pair and either updates the key/value in the hash table (key already exists) or inserts a
        new key/value pair in the hash table (key doesn't already exist). If the current load factor of the table is
        greater than or equal to 0.5, the table capacity is doubled.
        """

        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # See if the key is already in the table. If so, update the value.
        if self.contains_key(key):
            key_location = self.find_key(key)
            self._buckets[key_location].value = value
            return

        # Key isn't in the table. Create a new hash entry and place it in the table.
        new_key_value_pair = HashEntry(key, value)
        initial_hash = self.get_hash(key)
        hash = initial_hash
        probe_attempt = 1

        # Look for a spot in the table for the key. Probe if necessary.
        while self._buckets[hash] is not None and not self._buckets[hash].is_tombstone:
            hash = (initial_hash + probe_attempt ** 2) % self.get_capacity()
            probe_attempt += 1

        # Now that a suitable hash has been found, update the array and increment the size.
        self._size += 1
        self._buckets[hash] = new_key_value_pair

    def resize_table(self, new_capacity: int) -> None:
        """
        Takes a new capacity and updates the capacity of the hash map table. If the new capacity is less than the
        current number of elements in the table, do nothing.
        """

        # If the new capacity is less than current hash table size, do nothing.
        if new_capacity < self._size:
            return

        # New capacity must be a prime number.
        if self._is_prime(new_capacity):
            self._capacity = new_capacity
        else:
            self._capacity = self._next_prime(new_capacity)

        # Get the data from the table before clearing it out.
        data = self._buckets
        self._buckets = DynamicArray()
        self._size = 0
        for _ in range(self._capacity):
            self._buckets.append(None)

        # Transfer entries from the copy back into the new, larger capacity table.
        for index in range(data.length()):
            if data[index] is not None and not data[index].is_tombstone:
                self.put(data[index].key, data[index].value)

    def table_load(self) -> float:
        """
        Returns the table load factor.
        """

        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Return the number of empty buckets in the table.
        """

        return self.get_capacity() - self.get_size()

    def get(self, key: str) -> object:
        """
        Takes a key and returns the value associated with the key in the hash table. Returns None if the key is not in
        the hash table.
        """

        hash = self.get_hash(key)

        key_location = self.find_key(key)

        if key_location > -1:
            return self._buckets[key_location].value

        return None

    def contains_key(self, key: str) -> bool:
        """
        Takes a key and returns True if the key is in the hash table, otherwise returns False
        """

        # If the table is empty it will not contain the key.
        if self.get_size() == 0:
            return False

        initial_hash = self.get_hash(key)
        hash = initial_hash
        probe_attempt = 1

        # Look for key matches that are not tombstones until None is encountered.
        while self._buckets[hash] is not None:
            if not self._buckets[hash].is_tombstone and self._buckets[hash].key == key:
                return True
            hash = (initial_hash + probe_attempt ** 2) % self._capacity
            probe_attempt += 1

        return False

    def remove(self, key: str) -> None:
        """
        Takes a key and removes the key along with it's associated value from the hash table. This method does nothing
        if the key is not in the hash table.
        """

        key_location = self.find_key(key)

        # The key was not located.
        if key_location < 0:
            return

        # Decrease the size of the table and mark the entry as a tombstone.
        self._size -= 1
        self._buckets[key_location].is_tombstone = True

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of key/value pairs from the table. The order of
        key/value pairs is not specified.
        """

        arr = DynamicArray()

        # The hash table is iterable.
        for item in self:
            arr.append((item.key, item.value))

        return arr

    def clear(self) -> None:
        """
        Clears the hash table contents while leaving the table capacity unchanged.
        """

        self._size = 0
        self._buckets = DynamicArray()

        for _ in range(self._capacity):
            self._buckets.append(None)

    def __iter__(self):
        """
        Iterator method for the HashMap class.
        """

        # Initialize an index for the iterator.
        self._index = 0

        return self

    def __next__(self):
        """
        Next method for the HashMap class. Provides a means for moving between active key/value pairs in the table.
        """

        # Try to find the next active entry in the table (Non-None and Non-Tombstone entries).
        try:
            while self._buckets[self._index] is None or self._buckets[self._index].is_tombstone:
                self._index += 1
            value = self._buckets[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1

        return value

    def find_key(self, key) -> int:
        """
        Takes a key and returns the key's hash index in the table.
        """

        initial_hash = self.get_hash(key)
        hash = initial_hash
        probe_attempt = 1

        # Search for the key, probing different hash values as necessary.
        while self._buckets[hash] is not None:
            if not self._buckets[hash].is_tombstone and self._buckets[hash].key == key:
                return hash
            hash = (initial_hash + probe_attempt ** 2) % self._capacity
            probe_attempt += 1

        return -1

    def get_hash(self, key) -> int:
        """
        Takes a key and returns its hash integer.
        """

        return self._hash_function(key) % self.get_capacity()


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
