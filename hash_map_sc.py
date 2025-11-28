# Name: Jeffrey Maher
# OSU Email: maherje@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: assignment 6
# Due Date: August 13, 2024
# Description: Implement Hash Map classes utilizing 1)Chaining and 2)Open Addressing.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        Takes a key and a value and either updates the hash map if the key already exists or creates a new entry in the
        hash map with the new key and value pair.
        """

        # If the current load factor of the table is >= 1, double the array size.
        if self.table_load() >= 1:
            self.resize_table(2 * self.get_capacity())

        hash = self.get_hash(key)

        # If the key exists, it can be removed and replaced with the new (key, value) pair.
        if self._buckets[hash].remove(key):
            self._buckets[hash].insert(key, value)
        # The key doesn't exist, so we add it at its hash location and increment the table size.
        else:
            self._buckets[hash].insert(key, value)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Updates the table capacity to the new value. If the new capacity is less than 1, this method will do nothing. If
        the capacity is 1 or higher the method will make sure it is a prime number.
        """

        if new_capacity < 1:
            return

        if self._is_prime(new_capacity):
            self._capacity = new_capacity
        else:
            self._capacity = self._next_prime(new_capacity)

        # Get the data from the table before clearing it out.
        data = self.get_keys_and_values()
        self.clear()

        # Reload the hash table with its new capacity.
        for index in range(data.length()):
            self.put(data[index][0], data[index][1])

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """

        return self.get_size() / self.get_capacity()

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """

        num_empty_buckets = 0

        # Step through every bucket in the table.
        # Check if the bucket is empty and increment the empty bucket count if appropriate.
        for index in range(self._capacity):
            if self._buckets[index].length() == 0:
                num_empty_buckets += 1

        return num_empty_buckets

    def get(self, key: str) -> object:
        """
        Takes a key and returns the value associated with that key. Returns None if the key is not in the hash table.
        """

        hash = self.get_hash(key)

        # The linked list at the key's hash location.
        ll = self._buckets[hash]

        if ll.length() < 1:
            # There is nothing in this hash bucket.
            return None

        node = ll.contains(key)

        if node is None:
            return None
        else:
            return node.value

    def contains_key(self, key: str) -> bool:
        """
        Takes a key and returns True if that key is in the hash map, otherwise returns False.
        """

        hash = self.get_hash(key)

        # The linked list at the key's hash location.
        ll = self._buckets[hash]

        if ll.length() > 0:
            if ll.contains(key):
                return True

        return False

    def remove(self, key: str) -> None:
        """
        Takes a key and attempts to remove it along with its associated value from the hash map. Method does nothing if
        the key is not in the hash table.
        """

        hash = self.get_hash(key)

        if self._buckets[hash].remove(key):
            # Removal was successful, reduce table size by 1.
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index has a tuple (key, value) from the hash map. Key order is not specified.
        """

        # Initialize the return array.
        arr = DynamicArray()

        # Step through each bucket in the table. If the linked list has contents, add to the return array.
        for index in range(self._buckets.length()):
            ll = self._buckets[index]
            if ll.length() > 0:
                for node in ll:
                    arr.append((node.key, node.value))

        return arr

    def clear(self) -> None:
        """
        Clears the contents of the hash map without changing the underlying table capacity.
        """

        self._buckets = DynamicArray()

        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._size = 0

    def get_hash(self, key) -> int:
        """
        Takes a key and returns its hash integer.
        """

        return self._hash_function(key) % self.get_capacity()


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Takes a dynamic array of at least one value of possibly unsorted values. Returns a tuple containing in order, the
    mode and the frequency value of the mode. Executes with O(n) time complexity.
    """

    map = HashMap()

    # Step through the input array and fill the hash map with keys and their frequencies.
    for index in range(da.length()):
        key = da[index]
        # If key is already in the table, add 1 to the frequency.
        if map.contains_key(key):
            freq = map.get(key)
            map.put(key, freq + 1)
        # Key isn't in the table, add it with frequency 1.
        else:
            map.put(key, 1)

    # Initialize the return array of keys and their frequencies.
    arr = DynamicArray()
    max_freq = 0

    # Step through the array again, this time to compare frequency values.
    for index in range(da.length()):
        key = da[index]
        # See if the key is still in the table (They are removed after first occurrence in the input array).
        if map.contains_key(key):
            freq = map.get(key)
            if freq > max_freq:
                # New max, clear the array and add the new key and its frequency.
                arr = DynamicArray()
                arr.append(key)
                max_freq = freq
            elif freq == max_freq:
                # This key matches the frequency of the current max, add it to the array.
                arr.append(key)
            # We only need to access the keys in the hash table once. The key can now be removed to avoid adding twice.
            map.remove(key)

    return arr, max_freq



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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
