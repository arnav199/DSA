"""Solutions extracted from DSA.xlsx in Python 3.

The workbook mixes direct LeetCode problems, linked-list practice tasks, and a few
algorithm templates. This module keeps the solutions grouped by topic and uses
simple, reusable Python implementations.
"""

from collections import Counter
from heapq import heappop, heappush
from itertools import count as heap_count
from typing import Callable, List, Optional, Sequence


class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next


# ---------------------------------------------------------------------------
# Helpers for linked list practice
# ---------------------------------------------------------------------------


def build_linked_list(values: Sequence[int]) -> Optional[ListNode]:
    dummy = ListNode()
    tail = dummy
    for value in values:
        tail.next = ListNode(value)
        tail = tail.next
    return dummy.next


def linked_list_to_list(head: Optional[ListNode]) -> List[int]:
    values: List[int] = []
    current = head
    while current:
        values.append(current.val)
        current = current.next
    return values


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        return two_sum(nums, target)


# ---------------------------------------------------------------------------
# Array
# ---------------------------------------------------------------------------


def two_sum(nums: List[int], target: int) -> List[int]:
    seen = {}
    for index, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], index]
        seen[num] = index
    return []


def remove_duplicates_sorted_array(nums: List[int]) -> int:
    if not nums:
        return 0

    write = 1
    for read in range(1, len(nums)):
        if nums[read] != nums[write - 1]:
            nums[write] = nums[read]
            write += 1
    return write


def remove_element(nums: List[int], value: int) -> int:
    write = 0
    for num in nums:
        if num != value:
            nums[write] = num
            write += 1
    return write


def search_insert_position(nums: List[int], target: int) -> int:
    left, right = 0, len(nums)
    while left < right:
        mid = (left + right) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left


def merge_sorted_array(nums1: List[int], m: int, nums2: List[int], n: int) -> List[int]:
    i = m - 1
    j = n - 1
    k = m + n - 1

    while j >= 0:
        if i >= 0 and nums1[i] > nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1
    return nums1


def best_time_buy_sell_stock(prices: List[int]) -> int:
    min_price = float("inf")
    best_profit = 0
    for price in prices:
        min_price = min(min_price, price)
        best_profit = max(best_profit, price - min_price)
    return best_profit


def majority_element(nums: List[int]) -> int:
    candidate = None
    count = 0
    for num in nums:
        if count == 0:
            candidate = num
            count = 1
        elif num == candidate:
            count += 1
        else:
            count -= 1
    return candidate


def contains_duplicate(nums: List[int]) -> bool:
    return len(nums) != len(set(nums))


def missing_number(nums: List[int]) -> int:
    answer = len(nums)
    for index, num in enumerate(nums):
        answer ^= index ^ num
    return answer


def move_zeroes(nums: List[int]) -> None:
    write = 0
    for read, num in enumerate(nums):
        if num != 0:
            nums[write] = num
            write += 1
    for index in range(write, len(nums)):
        nums[index] = 0


def array_partition(nums: List[int]) -> int:
    nums = sorted(nums)
    return sum(nums[::2])


def max_consecutive_ones(nums: List[int]) -> int:
    best = 0
    current = 0
    for num in nums:
        if num == 1:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def single_number(nums: List[int]) -> int:
    answer = 0
    for num in nums:
        answer ^= num
    return answer


# ---------------------------------------------------------------------------
# String
# ---------------------------------------------------------------------------


def roman_to_integer(s: str) -> int:
    values = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1000,
    }
    total = 0
    for index, char in enumerate(s):
        if index + 1 < len(s) and values[char] < values[s[index + 1]]:
            total -= values[char]
        else:
            total += values[char]
    return total


def longest_common_prefix(strs: List[str]) -> str:
    if not strs:
        return ""

    prefix = strs[0]
    for word in strs[1:]:
        while not word.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix


def valid_parentheses(s: str) -> bool:
    pairs = {
        ")": "(",
        "]": "[",
        "}": "{",
    }
    stack = []
    for char in s:
        if char in pairs:
            if not stack or stack.pop() != pairs[char]:
                return False
        else:
            stack.append(char)
    return not stack


def find_first_occurrence(haystack: str, needle: str) -> int:
    return haystack.find(needle)


def length_of_last_word(s: str) -> int:
    index = len(s) - 1
    while index >= 0 and s[index] == " ":
        index -= 1

    length = 0
    while index >= 0 and s[index] != " ":
        length += 1
        index -= 1
    return length


def valid_palindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True


def isomorphic_strings(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False

    st = {}
    ts = {}
    for left_char, right_char in zip(s, t):
        if st.get(left_char, right_char) != right_char:
            return False
        if ts.get(right_char, left_char) != left_char:
            return False
        st[left_char] = right_char
        ts[right_char] = left_char
    return True


def valid_anagram(s: str, t: str) -> bool:
    return Counter(s) == Counter(t)


def word_pattern(pattern: str, s: str) -> bool:
    words = s.split()
    if len(pattern) != len(words):
        return False

    p_to_w = {}
    w_to_p = {}
    for char, word in zip(pattern, words):
        if p_to_w.get(char, word) != word or w_to_p.get(word, char) != char:
            return False
        p_to_w[char] = word
        w_to_p[word] = char
    return True


def reverse_string(chars: List[str]) -> None:
    left, right = 0, len(chars) - 1
    while left < right:
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1


def reverse_vowels(s: str) -> str:
    vowels = set("aeiouAEIOU")
    chars = list(s)
    left, right = 0, len(chars) - 1
    while left < right:
        while left < right and chars[left] not in vowels:
            left += 1
        while left < right and chars[right] not in vowels:
            right -= 1
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1
    return "".join(chars)


def first_unique_character(s: str) -> int:
    counts = Counter(s)
    for index, char in enumerate(s):
        if counts[char] == 1:
            return index
    return -1


def is_subsequence(s: str, t: str) -> bool:
    iterator = iter(t)
    return all(char in iterator for char in s)


def rotate_string(s: str, goal: str) -> bool:
    return len(s) == len(goal) and goal in (s + s)


def valid_word(word: str) -> bool:
    if len(word) < 3 or not word.isalnum():
        return False

    vowels = set("aeiouAEIOU")
    has_vowel = False
    has_consonant = False
    for char in word:
        if char.isalpha():
            if char in vowels:
                has_vowel = True
            else:
                has_consonant = True
    return has_vowel and has_consonant


# ---------------------------------------------------------------------------
# Linked List
# ---------------------------------------------------------------------------


def count_nodes(head: Optional[ListNode]) -> int:
    count = 0
    current = head
    while current:
        count += 1
        current = current.next
    return count


def print_nodes(head: Optional[ListNode]) -> List[int]:
    return linked_list_to_list(head)


def insert_element_at_beginning(head: Optional[ListNode], value: int) -> ListNode:
    return ListNode(value, head)


def insert_element_at_end(head: Optional[ListNode], value: int) -> ListNode:
    new_node = ListNode(value)
    if not head:
        return new_node

    current = head
    while current.next:
        current = current.next
    current.next = new_node
    return head


def insert_element_at_middle(head: Optional[ListNode], value: int) -> ListNode:
    if not head:
        return ListNode(value)

    length = count_nodes(head)
    target_index = length // 2
    if target_index == 0:
        return insert_element_at_beginning(head, value)

    dummy = ListNode(0, head)
    previous = dummy
    for _ in range(target_index):
        previous = previous.next
    previous.next = ListNode(value, previous.next)
    return dummy.next


def insert_element_at_specific_position(
    head: Optional[ListNode], value: int, position: int
) -> ListNode:
    dummy = ListNode(0, head)
    previous = dummy
    steps = max(position - 1, 0)
    for _ in range(steps):
        if not previous.next:
            break
        previous = previous.next
    previous.next = ListNode(value, previous.next)
    return dummy.next


def delete_element_at_beginning(head: Optional[ListNode]) -> Optional[ListNode]:
    return head.next if head else None


def delete_element_at_end(head: Optional[ListNode]) -> Optional[ListNode]:
    if not head or not head.next:
        return None

    current = head
    while current.next and current.next.next:
        current = current.next
    current.next = None
    return head


def delete_element_at_middle(head: Optional[ListNode]) -> Optional[ListNode]:
    if not head:
        return None

    length = count_nodes(head)
    target_index = length // 2
    dummy = ListNode(0, head)
    previous = dummy
    for _ in range(target_index):
        previous = previous.next
    if previous.next:
        previous.next = previous.next.next
    return dummy.next


def delete_element_at_specific_position(
    head: Optional[ListNode], position: int
) -> Optional[ListNode]:
    if not head:
        return None

    dummy = ListNode(0, head)
    previous = dummy
    steps = max(position - 1, 0)
    for _ in range(steps):
        if not previous.next:
            return dummy.next
        previous = previous.next
    if previous.next:
        previous.next = previous.next.next
    return dummy.next


def linked_list_cycle(head: Optional[ListNode]) -> bool:
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


def linked_list_cycle_ii(head: Optional[ListNode]) -> Optional[ListNode]:
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            break
    else:
        return None

    slow = head
    while slow is not fast:
        slow = slow.next
        fast = fast.next
    return slow


def reverse_linked_list(head: Optional[ListNode]) -> Optional[ListNode]:
    previous = None
    current = head
    while current:
        next_node = current.next
        current.next = previous
        previous = current
        current = next_node
    return previous


def reverse_linked_list_ii(
    head: Optional[ListNode], left: int, right: int
) -> Optional[ListNode]:
    if not head or left == right:
        return head

    dummy = ListNode(0, head)
    previous = dummy
    for _ in range(left - 1):
        previous = previous.next

    current = previous.next
    for _ in range(right - left):
        next_node = current.next
        current.next = next_node.next
        next_node.next = previous.next
        previous.next = next_node
    return dummy.next


def merge_two_linked_list(
    list1: Optional[ListNode], list2: Optional[ListNode]
) -> Optional[ListNode]:
    dummy = ListNode()
    tail = dummy
    while list1 and list2:
        if list1.val <= list2.val:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next
    tail.next = list1 if list1 else list2
    return dummy.next


def remove_duplicates_from_sorted_list(head: Optional[ListNode]) -> Optional[ListNode]:
    current = head
    while current and current.next:
        if current.val == current.next.val:
            current.next = current.next.next
        else:
            current = current.next
    return head


def rotate_list(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    if not head or not head.next or k == 0:
        return head

    length = 1
    tail = head
    while tail.next:
        tail = tail.next
        length += 1

    k %= length
    if k == 0:
        return head

    tail.next = head
    steps_to_new_tail = length - k - 1
    new_tail = head
    for _ in range(steps_to_new_tail):
        new_tail = new_tail.next

    new_head = new_tail.next
    new_tail.next = None
    return new_head


# ---------------------------------------------------------------------------
# Searching
# ---------------------------------------------------------------------------


def peak_element(nums: List[int]) -> int:
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] < nums[mid + 1]:
            left = mid + 1
        else:
            right = mid
    return left


def valid_perfect_square(num: int) -> bool:
    left, right = 1, num
    while left <= right:
        mid = (left + right) // 2
        square = mid * mid
        if square == num:
            return True
        if square < num:
            left = mid + 1
        else:
            right = mid - 1
    return False


def binary_search(nums: List[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def intersection_of_two_arrays(nums1: List[int], nums2: List[int]) -> List[int]:
    return list(set(nums1) & set(nums2))


def find_first_and_last_position(nums: List[int], target: int) -> List[int]:
    def bound(find_left: bool) -> int:
        left, right = 0, len(nums)
        while left < right:
            mid = (left + right) // 2
            if nums[mid] > target or (find_left and nums[mid] == target):
                right = mid
            else:
                left = mid + 1
        return left

    left = bound(True)
    if left == len(nums) or nums[left] != target:
        return [-1, -1]
    return [left, bound(False) - 1]


def first_bad_version(n: int, is_bad_version: Callable[[int], bool]) -> int:
    left, right = 1, n
    while left < right:
        mid = (left + right) // 2
        if is_bad_version(mid):
            right = mid
        else:
            left = mid + 1
    return left


# ---------------------------------------------------------------------------
# Sorting
# ---------------------------------------------------------------------------


def chocolate_distribution_problem(arr: List[int], m: int) -> int:
    if m <= 1 or len(arr) < m:
        return 0

    arr = sorted(arr)
    return min(arr[index + m - 1] - arr[index] for index in range(len(arr) - m + 1))


def pair_with_given_difference(arr: List[int], k: int) -> bool:
    k = abs(k)
    arr = sorted(arr)
    left, right = 0, 1
    while left < len(arr) and right < len(arr):
        if left == right:
            right += 1
            continue

        difference = arr[right] - arr[left]
        if difference == k:
            return True
        if difference < k:
            right += 1
        else:
            left += 1
    return False


def sort_colors(nums: List[int]) -> None:
    low = 0
    mid = 0
    high = len(nums) - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1


def sort_list(head: Optional[ListNode]) -> Optional[ListNode]:
    if not head or not head.next:
        return head

    slow = head
    fast = head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    mid = slow.next
    slow.next = None

    left = sort_list(head)
    right = sort_list(mid)
    return merge_two_linked_list(left, right)


def sort_array(nums: List[int]) -> List[int]:
    return sorted(nums)


def kth_largest_element(nums: List[int], k: int) -> int:
    heap: List[int] = []
    for num in nums:
        if len(heap) < k:
            heappush(heap, num)
        elif num > heap[0]:
            heappop(heap)
            heappush(heap, num)
    return heap[0]


def merge_k_sorted_lists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    heap = []
    unique = heap_count()
    for node in lists:
        if node:
            heappush(heap, (node.val, next(unique), node))

    dummy = ListNode()
    tail = dummy
    while heap:
        _, _, node = heappop(heap)
        tail.next = node
        tail = tail.next
        if node.next:
            heappush(heap, (node.next.val, next(unique), node.next))
    tail.next = None
    return dummy.next


# ---------------------------------------------------------------------------
# Stack
# ---------------------------------------------------------------------------


valid_parenthesis_stack = valid_parentheses


class MinStack:
    def __init__(self):
        self.stack: List[tuple[int, int]] = []

    def push(self, val: int) -> None:
        current_min = val if not self.stack else min(val, self.stack[-1][1])
        self.stack.append((val, current_min))

    def pop(self) -> None:
        if self.stack:
            self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]

    def get_min(self) -> int:
        return self.getMin()


class QueueUsingStack:
    def __init__(self):
        self.in_stack: List[int] = []
        self.out_stack: List[int] = []

    def push(self, x: int) -> None:
        self.in_stack.append(x)

    def _shift(self) -> None:
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())

    def pop(self) -> int:
        self._shift()
        return self.out_stack.pop()

    def peek(self) -> int:
        self._shift()
        return self.out_stack[-1]

    def empty(self) -> bool:
        return not self.in_stack and not self.out_stack


# ---------------------------------------------------------------------------
# Techniques / templates
# ---------------------------------------------------------------------------


def two_pointer_two_sum_sorted(nums: List[int], target: int) -> List[int]:
    left, right = 0, len(nums) - 1
    while left < right:
        current = nums[left] + nums[right]
        if current == target:
            return [left, right]
        if current < target:
            left += 1
        else:
            right -= 1
    return [-1, -1]


def sliding_window_max_sum(nums: List[int], k: int) -> int:
    if k <= 0 or k > len(nums):
        return 0

    window = sum(nums[:k])
    best = window
    for index in range(k, len(nums)):
        window += nums[index] - nums[index - k]
        best = max(best, window)
    return best


def prefix_sum_range_sum(nums: List[int], left: int, right: int) -> int:
    prefix = [0]
    for num in nums:
        prefix.append(prefix[-1] + num)
    return prefix[right + 1] - prefix[left]


def binary_search_answer(lo: int, hi: int, predicate: Callable[[int], bool]) -> int:
    while lo < hi:
        mid = (lo + hi) // 2
        if predicate(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def monotonic_stack_next_greater(nums: List[int]) -> List[int]:
    result = [-1] * len(nums)
    stack: List[int] = []
    for index, num in enumerate(nums):
        while stack and nums[stack[-1]] < num:
            result[stack.pop()] = num
        stack.append(index)
    return result


# ---------------------------------------------------------------------------
# Aliases for repeated workbook entries
# ---------------------------------------------------------------------------


search_insert_position_searching = search_insert_position
sort_0s_1s_2s = sort_colors
