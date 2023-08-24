# Python Data Structures Examples

This repository contains Python code examples demonstrating the usage of built-in and user-defined data structures, such as arrays, lists, dictionaries, stacks, queues, hash maps, trees, and heaps. Each example is accompanied by detailed explanations and step-by-step walkthroughs, making it easy for developers to understand and follow along.

These are some of the examples within the Google Collab Notebook

## Built-in Data Structures: Arrays, Lists, and Dictionaries

### Finding Second Largest Element

Given an array of integers, find the second largest element in the array. If the array has less than two elements, return `None`.

```python
def second_largest(arr):
    if len(arr) < 2:
        return None
    largest = second = float('-inf')
    for num in arr:
        if num > largest:
            second = largest
            largest = num
        elif num > second and num != largest:
            second = num
    return second
```

Example usage:

```python
array = [3, 1, 4, 7, 5, 9, 2]
print(second_largest(array))  # Output: 7
```

### Counting Word Frequencies

Given a text string, count the frequency of each word in the text and return a dictionary with the word as the key and the frequency as the value.

```python
def word_frequency(text):
    words = text.split()
    frequency = {}
    for word in words:
        word = word.lower()
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    return frequency
```

Example usage:

```python
text = "This is a simple example of a text. This is not complex."
print(word_frequency(text))
```

Output:

```
{'this': 2, 'is': 2, 'a': 2, 'simple': 1, 'example': 1, 'of': 1, 'text.': 1, 'not': 1, 'complex.': 1}
```

## THIS IS OPTIONAL - You can now try to complete these other exercises by your own :

### Built-in Data Structures: Arrays, Lists, and Dictionaries
#### Arrays and Lists:
- Write a function to find the second largest element in an array.
- Implement a function to reverse an array in-place.
- Given two sorted arrays, merge them into a single sorted array.
- Implement a function to rotate an array to the right by k steps.

#### Dictionaries:
- Create a dictionary to store the frequency of words in a text document.
- Implement a function to find common elements between two lists.
- Given a list of tuples representing student names and their scores, convert it into a dictionary with names as keys and scores as values.
- Write a program to count the frequency of characters in a string using a dictionary.

### User-defined Data Structures: Stack, Queue, HashMap, Tree, Heaps
#### Stack:
- Implement a stack using lists and write push, pop, and peek methods.
- Write a function to check if parentheses in a given string are balanced using a stack.
- Create a stack-based calculator that evaluates postfix expressions.
- Design a function to reverse a string using a stack.

#### Queue:
- Implement a queue using lists and define enqueue and dequeue methods.
- Write a function to generate binary numbers from 1 to n using a queue.
- Implement a circular queue that overwrites oldest items when full.
- Use a queue to perform level-order traversal on a binary tree.

#### HashMap:
- Create a simple hash map that supports insert, retrieve, and delete operations.
- Implement a hash map-based cache with a maximum capacity.
- Solve the problem of finding the first non-repeated character in a string using a hash map.
- Write a program to detect if two strings are anagrams using hash maps.

#### Tree:
- Build a binary search tree (BST) and implement methods for insertion and search.
- Write a function to calculate the height of a binary tree.
- Perform an in-order traversal of a binary tree using recursion and iteration.
- Implement a function to check if a binary tree is a valid BST.

#### Heaps:
- Implement a min-heap and max-heap using lists.
- Write a program to merge k sorted arrays using a min-heap.
- Implement a priority queue using a min-heap to manage tasks with different priorities.
- Design a heap-based algorithm to find the kth largest element in an array.