# LeetCode Study Plan - 50 Problems in 2 Months

**Goal:** Pass coding interviews at mid-tier companies (Razorpay, PhonePe, Swiggy, Paytm)

**Target:** ₹25L-₹35L roles (SDE-2 level)

**Timeline:** 8 weeks, ~6-7 problems/week, 1-2 hours/day

---

## 📊 Overview

**Week 1-2:** Arrays & Hashing (15 problems - EASY)
**Week 3-4:** Two Pointers & Sliding Window (12 problems - EASY/MEDIUM)
**Week 5-6:** Trees & Graphs (13 problems - MEDIUM)
**Week 7-8:** Dynamic Programming & Final Review (10 problems - MEDIUM)

**Total:** 50 problems (20 easy, 30 medium)

---

## 🎯 Why This Plan Works

**1. Pattern-Based Learning**
- Learn 1 pattern → Apply to 5-10 similar problems
- Interviews ask pattern variations (not random problems)

**2. Realistic for Working Professionals**
- 1-2 hours/day (doable with full-time job)
- Weekends for catch-up/review

**3. Optimized for Mid-Tier Interviews**
- Mid-tier companies focus on Easy/Medium (not Hard)
- Emphasis on common patterns (not obscure algorithms)

**4. Progressive Difficulty**
- Week 1-2: Build confidence with Easy
- Week 3-4: Transition to Medium
- Week 5-8: Master Medium level

---

## 📅 Week 1-2: Arrays & Hashing (Foundation)

**Goal:** Master the most common pattern in interviews

**Time:** 2-3 hours total per problem (read, solve, understand solution)

### **Day 1: Setup & First Problem**

**Problem 1: Two Sum** (Easy)
- **Link:** https://leetcode.com/problems/two-sum/
- **Pattern:** Hash Map for O(n) lookup
- **Why:** Asked in 50% of interviews
- **Key Insight:** Use HashMap to store complements
- **Time:** 1 hour (including setup)

**Ruby Solution:**
```ruby
def two_sum(nums, target)
  hash = {}
  nums.each_with_index do |num, i|
    complement = target - num
    return [hash[complement], i] if hash.key?(complement)
    hash[num] = i
  end
end
```

---

### **Day 2-3: Array Fundamentals**

**Problem 2: Contains Duplicate** (Easy)
- **Link:** https://leetcode.com/problems/contains-duplicate/
- **Pattern:** HashSet for uniqueness check
- **Time:** 30 min

**Problem 3: Valid Anagram** (Easy)
- **Link:** https://leetcode.com/problems/valid-anagram/
- **Pattern:** HashMap for frequency counting
- **Time:** 30 min

**Problem 4: Group Anagrams** (Medium)
- **Link:** https://leetcode.com/problems/group-anagrams/
- **Pattern:** HashMap with sorted string key
- **Time:** 45 min
- **First MEDIUM problem!**

---

### **Day 4-5: More Hashing**

**Problem 5: Top K Frequent Elements** (Medium)
- **Link:** https://leetcode.com/problems/top-k-frequent-elements/
- **Pattern:** HashMap + Bucket Sort
- **Time:** 45 min

**Problem 6: Product of Array Except Self** (Medium)
- **Link:** https://leetcode.com/problems/product-of-array-except-self/
- **Pattern:** Prefix/Suffix arrays
- **Time:** 45 min

**Problem 7: Longest Consecutive Sequence** (Medium)
- **Link:** https://leetcode.com/problems/longest-consecutive-sequence/
- **Pattern:** HashSet for O(1) lookup
- **Time:** 45 min

---

### **Day 6-7: Strings & Review**

**Problem 8: Valid Palindrome** (Easy)
- **Link:** https://leetcode.com/problems/valid-palindrome/
- **Pattern:** Two pointers
- **Time:** 20 min

**Problem 9: Longest Substring Without Repeating Characters** (Medium)
- **Link:** https://leetcode.com/problems/longest-substring-without-repeating-characters/
- **Pattern:** Sliding window + HashSet
- **Time:** 45 min

**Problem 10: Encode and Decode Strings** (Medium)
- **Link:** https://leetcode.com/problems/encode-and-decode-strings/ (Premium)
- **Alternative:** https://www.lintcode.com/problem/659/ (Free)
- **Pattern:** String manipulation
- **Time:** 30 min

---

### **Week 1-2 Review (Day 11-14)**

**Day 11-12:** Re-solve problems 1-10 from memory (no peeking!)
**Day 13-14:** Add 5 more Easy problems for confidence

**Bonus Problems (Easy):**
11. Best Time to Buy and Sell Stock
12. Valid Parentheses
13. Merge Two Sorted Lists (linked list intro)
14. Maximum Subarray
15. Climbing Stairs (DP intro)

**Week 1-2 Total:** 15 problems (8 easy, 7 medium)

---

## 📅 Week 3-4: Two Pointers & Sliding Window

**Goal:** Master efficiency patterns (replace brute force)

### **Day 15-16: Two Pointers Basics**

**Problem 16: 3Sum** (Medium)
- **Link:** https://leetcode.com/problems/3sum/
- **Pattern:** Sorted array + two pointers
- **Time:** 1 hour (challenging!)
- **Key Insight:** Sort first, then use two pointers

**Problem 17: Container With Most Water** (Medium)
- **Link:** https://leetcode.com/problems/container-with-most-water/
- **Pattern:** Two pointers (greedy approach)
- **Time:** 45 min

---

### **Day 17-19: Sliding Window**

**Problem 18: Minimum Window Substring** (Hard - but important!)
- **Link:** https://leetcode.com/problems/minimum-window-substring/
- **Pattern:** Sliding window + HashMap
- **Time:** 1.5 hours (hardest so far, but worth it!)
- **Why:** Common in real interviews

**Problem 19: Longest Repeating Character Replacement** (Medium)
- **Link:** https://leetcode.com/problems/longest-repeating-character-replacement/
- **Pattern:** Sliding window + frequency count
- **Time:** 45 min

**Problem 20: Permutation in String** (Medium)
- **Link:** https://leetcode.com/problems/permutation-in-string/
- **Pattern:** Sliding window + HashMap
- **Time:** 45 min

---

### **Day 20-22: Mixed Practice**

**Problem 21: Find All Anagrams in a String** (Medium)
- **Link:** https://leetcode.com/problems/find-all-anagrams-in-a-string/
- **Pattern:** Sliding window (similar to #20)
- **Time:** 30 min (should be easier now!)

**Problem 22: Trapping Rain Water** (Hard)
- **Link:** https://leetcode.com/problems/trapping-rain-water/
- **Pattern:** Two pointers
- **Time:** 1 hour
- **Why:** Shows problem-solving skills

**Problem 23: Remove Nth Node From End of List** (Medium)
- **Link:** https://leetcode.com/problems/remove-nth-node-from-end-of-list/
- **Pattern:** Two pointers (fast/slow)
- **Time:** 30 min

---

### **Week 3-4 Review (Day 23-28)**

**Day 23-25:** Re-solve problems 16-23
**Day 26-28:** Add 4 more Medium problems

**Bonus Problems (Medium):**
24. Reverse Linked List
25. Linked List Cycle
26. Reorder List
27. Find Minimum in Rotated Sorted Array

**Week 3-4 Total:** 12 problems (all medium!)

---

## 📅 Week 5-6: Trees & Graphs

**Goal:** Master recursive thinking and BFS/DFS

### **Day 29-31: Binary Trees Basics**

**Problem 28: Invert Binary Tree** (Easy)
- **Link:** https://leetcode.com/problems/invert-binary-tree/
- **Pattern:** Recursion
- **Time:** 20 min
- **Why:** Famous "Google interview question"

**Problem 29: Maximum Depth of Binary Tree** (Easy)
- **Link:** https://leetcode.com/problems/maximum-depth-of-binary-tree/
- **Pattern:** DFS recursion
- **Time:** 20 min

**Problem 30: Same Tree** (Easy)
- **Link:** https://leetcode.com/problems/same-tree/
- **Pattern:** Recursion
- **Time:** 20 min

**Problem 31: Subtree of Another Tree** (Easy)
- **Link:** https://leetcode.com/problems/subtree-of-another-tree/
- **Pattern:** Recursion (combine #30 logic)
- **Time:** 30 min

---

### **Day 32-34: Tree Traversals**

**Problem 32: Binary Tree Level Order Traversal** (Medium)
- **Link:** https://leetcode.com/problems/binary-tree-level-order-traversal/
- **Pattern:** BFS with queue
- **Time:** 45 min

**Problem 33: Validate Binary Search Tree** (Medium)
- **Link:** https://leetcode.com/problems/validate-binary-search-tree/
- **Pattern:** DFS with range checking
- **Time:** 45 min

**Problem 34: Kth Smallest Element in a BST** (Medium)
- **Link:** https://leetcode.com/problems/kth-smallest-element-in-a-bst/
- **Pattern:** In-order traversal
- **Time:** 45 min

---

### **Day 35-37: Graphs (BFS/DFS)**

**Problem 35: Number of Islands** (Medium)
- **Link:** https://leetcode.com/problems/number-of-islands/
- **Pattern:** DFS on grid (2D array)
- **Time:** 45 min
- **Key:** Treat grid as graph

**Problem 36: Clone Graph** (Medium)
- **Link:** https://leetcode.com/problems/clone-graph/
- **Pattern:** DFS + HashMap
- **Time:** 45 min

**Problem 37: Pacific Atlantic Water Flow** (Medium)
- **Link:** https://leetcode.com/problems/pacific-atlantic-water-flow/
- **Pattern:** Multi-source BFS/DFS
- **Time:** 1 hour

---

### **Week 5-6 Review (Day 38-42)**

**Day 38-40:** Re-solve trees/graphs problems
**Day 41-42:** Add 3 more tree problems

**Bonus Problems:**
38. Lowest Common Ancestor of BST (Easy/Medium)
39. Binary Tree Right Side View (Medium)
40. Construct Binary Tree from Preorder and Inorder (Medium)

**Week 5-6 Total:** 13 problems (4 easy, 9 medium)

---

## 📅 Week 7-8: Dynamic Programming & Review

**Goal:** Understand DP basics + review all patterns

### **Day 43-45: DP Basics**

**Problem 41: Climbing Stairs** (Easy - if not done)
- **Link:** https://leetcode.com/problems/climbing-stairs/
- **Pattern:** 1D DP
- **Time:** 20 min

**Problem 42: House Robber** (Medium)
- **Link:** https://leetcode.com/problems/house-robber/
- **Pattern:** 1D DP
- **Time:** 45 min

**Problem 43: Coin Change** (Medium)
- **Link:** https://leetcode.com/problems/coin-change/
- **Pattern:** 1D DP (unbounded knapsack)
- **Time:** 1 hour

---

### **Day 46-48: More DP**

**Problem 44: Longest Increasing Subsequence** (Medium)
- **Link:** https://leetcode.com/problems/longest-increasing-subsequence/
- **Pattern:** 1D DP
- **Time:** 45 min

**Problem 45: Word Break** (Medium)
- **Link:** https://leetcode.com/problems/word-break/
- **Pattern:** 1D DP + HashSet
- **Time:** 45 min

**Problem 46: Combination Sum** (Medium)
- **Link:** https://leetcode.com/problems/combination-sum/
- **Pattern:** Backtracking (DP-related)
- **Time:** 45 min

---

### **Week 7-8 Final Review (Day 49-56)**

**Day 49-50:** Add 4 more mixed problems

**Bonus Problems:**
47. Decode Ways (Medium DP)
48. Unique Paths (Medium DP)
49. Palindromic Substrings (Medium)
50. Maximum Product Subarray (Medium)

**Day 51-56: FULL REVIEW**
- **Day 51:** Review all Arrays & Hashing (1-15)
- **Day 52:** Review Two Pointers & Sliding Window (16-27)
- **Day 53:** Review Trees (28-40)
- **Day 54:** Review Graphs (35-37)
- **Day 55:** Review DP (41-50)
- **Day 56:** Mock interview with friend (pick 2-3 random problems, 45 min each)

**Week 7-8 Total:** 10 problems (1 easy, 9 medium)

---

## 📊 Final Summary

**50 Problems Breakdown:**
- **Easy:** 20 problems (build confidence)
- **Medium:** 30 problems (interview level)
- **Hard:** 0-2 problems (bonus, not required for mid-tier)

**By Pattern:**
- Arrays & Hashing: 15 problems
- Two Pointers: 8 problems
- Sliding Window: 4 problems
- Trees: 10 problems
- Graphs: 3 problems
- Dynamic Programming: 10 problems

**Time Investment:**
- Total: ~60-70 hours (1-1.5 hours/day for 8 weeks)
- Per problem: 30-60 min average

---

## 🎯 How to Solve Each Problem

**Step 1: Read Problem (5 min)**
- Understand: inputs, outputs, constraints
- Identify: pattern (array? tree? graph?)

**Step 2: Brute Force Solution (10 min)**
- Think out loud: "I could loop through everything..."
- Don't code yet, just think

**Step 3: Optimize (15 min)**
- Identify bottleneck: "Nested loops = O(n²)"
- Think: "Can I use HashMap for O(1) lookup?"
- Draw example on paper

**Step 4: Code Solution (15 min)**
- Write clean code
- Test with example inputs
- Handle edge cases

**Step 5: Review (10 min)**
- Read official solution (even if you solved it!)
- Learn alternative approaches
- Note time/space complexity

**Total: 45-60 min per problem**

---

## 💡 Study Tips

### **1. Use Ruby (Your Comfort Zone)**
- Interviews often allow any language
- Ruby's clean syntax helps you focus on logic (not syntax)
- Hash/Array methods are powerful (`.each_with_index`, `.key?`, etc.)

### **2. When Stuck (Don't Spend >45 Min)**
- Spend 20-30 min trying yourself
- If stuck, read hints (not full solution!)
- If still stuck, read solution, understand it, code from memory next day

### **3. Understand, Don't Memorize**
- Don't memorize solutions
- Understand the PATTERN
- Ask: "What makes this a sliding window problem?"

### **4. Practice Out Loud**
- Talk through your approach (like real interview)
- Explain: "I'm using a HashMap because..."
- Practice with friend or record yourself

### **5. Track Your Progress**
```
| Date | Problem | Pattern | Difficulty | Time | Solved? | Notes |
|------|---------|---------|------------|------|---------|-------|
| Mar 1 | Two Sum | HashMap | Easy | 30m | ✅ | Easy once I saw pattern |
| Mar 2 | 3Sum | Two Pointers | Medium | 60m | ❌ | Need to review sorting |
```

---

## 🚨 Common Mistakes to Avoid

### ❌ **Mistake 1: Doing Too Many Problems**
**Bad:** "I'll do 200 problems in 2 months!"
- **Result:** Burnout, shallow understanding

**Good:** 50 problems, deep understanding
- **Result:** Can solve variations in interview

---

### ❌ **Mistake 2: Only Easy Problems**
**Bad:** Do 50 easy problems
- **Result:** Fail medium interviews

**Good:** 20 easy + 30 medium
- **Result:** Ready for mid-tier interviews

---

### ❌ **Mistake 3: Not Reviewing**
**Bad:** Solve problem once, never revisit
- **Result:** Forget everything in 2 weeks

**Good:** Solve → Review next day → Review 1 week later
- **Result:** Patterns stick

---

### ❌ **Mistake 4: Jumping to Hard**
**Bad:** Start with "Median of Two Sorted Arrays" (Hard)
- **Result:** Frustration, give up

**Good:** Easy → Medium → Hard
- **Result:** Build confidence progressively

---

## 📱 Resources

**Primary Platform:**
- **LeetCode** (https://leetcode.com) - Main study platform

**Alternative (for Premium problems):**
- **LintCode** (https://www.lintcode.com) - Free alternatives

**Study Guides:**
- **Neetcode.io** (https://neetcode.io) - Best pattern-based roadmap
- **Grind 75** (https://grind75.com) - Alternative study plan

**Cheat Sheets:**
- Time complexity chart: https://www.bigocheatsheet.com
- Python/Ruby DS: Built-in methods reference

**Interview Practice:**
- **Pramp** (https://pramp.com) - Free mock interviews with peers

---

## 🎯 What to Do After 50 Problems

**Option 1: Apply Now (Recommended)**
- You're ready for mid-tier interviews (Razorpay, Swiggy, Paytm)
- 50 problems = 70th percentile (better than most candidates)
- You can learn more during interview process

**Option 2: Do 25 More (If Time Allows)**
- Add more medium problems
- Focus on weak areas (DP, graphs)
- Total: 75 problems = 85th percentile

**Option 3: Mock Interviews**
- Do 5-10 mock interviews on Pramp
- Practice explaining thought process
- Get feedback

---

## 📅 Daily Schedule Example

**Weekday (1.5 hours):**
- **6:30-7:00 PM:** Warm up with 1 easy problem (30 min)
- **7:00-8:00 PM:** 1 medium problem (60 min)

**Weekend (3 hours):**
- **Saturday:** 2 medium problems (2 hours) + review (1 hour)
- **Sunday:** Review week's problems + 1 new problem

**Flexibility:**
- Busy day? Do 1 easy problem (20 min)
- Extra time? Do 2 problems
- Sick? Skip, don't force it

---

## 🚀 Week-by-Week Checklist

### **Week 1-2: Arrays & Hashing**
- [ ] Day 1: Two Sum
- [ ] Day 2-3: Contains Duplicate, Valid Anagram, Group Anagrams
- [ ] Day 4-5: Top K, Product Except Self, Longest Consecutive
- [ ] Day 6-7: Valid Palindrome, Longest Substring, Encode/Decode
- [ ] Day 8-14: Review + 5 bonus easy problems
- [ ] **Goal:** 15 problems done ✅

### **Week 3-4: Two Pointers & Sliding Window**
- [ ] Day 15-16: 3Sum, Container With Most Water
- [ ] Day 17-19: Minimum Window, Longest Repeating, Permutation
- [ ] Day 20-22: Anagrams, Trapping Rain, Remove Nth Node
- [ ] Day 23-28: Review + 4 bonus linked list problems
- [ ] **Goal:** 12 problems done ✅

### **Week 5-6: Trees & Graphs**
- [ ] Day 29-31: Invert Tree, Max Depth, Same Tree, Subtree
- [ ] Day 32-34: Level Order, Validate BST, Kth Smallest
- [ ] Day 35-37: Number of Islands, Clone Graph, Pacific Atlantic
- [ ] Day 38-42: Review + 3 bonus tree problems
- [ ] **Goal:** 13 problems done ✅

### **Week 7-8: DP & Review**
- [ ] Day 43-45: Climbing Stairs, House Robber, Coin Change
- [ ] Day 46-48: LIS, Word Break, Combination Sum
- [ ] Day 49-50: 4 bonus DP problems
- [ ] Day 51-56: Full review of all 50 problems
- [ ] **Goal:** 10 problems done + ready for interviews! ✅

---

## 💰 Expected Interview Performance

**After 50 Problems:**

**Easy Problems:** 90%+ success rate
- You should solve these comfortably in <20 minutes

**Medium Problems:** 60-70% success rate
- Good enough for mid-tier companies (Razorpay, Swiggy, Paytm)

**Hard Problems:** 20-30% success rate
- Not needed for mid-tier (they rarely ask Hard)

**Interview Readiness:**
- ✅ Mid-tier companies (₹25L-₹35L): READY
- ⚠️ FAANG (₹50L-₹80L): Need 75-100 problems
- ❌ FAANG L5+ (₹1Cr+): Need 150+ problems

---

## 🎯 Final Tips

1. **Consistency > Intensity**
   - 1 hour/day for 60 days > 10 hours on Sunday

2. **Understand > Memorize**
   - Ask "Why?" not "What?"

3. **Practice Out Loud**
   - Explain your thinking (like real interview)

4. **Don't Give Up**
   - First 20 problems are hardest
   - After 30 problems, patterns click

5. **Apply While Learning**
   - Don't wait to be "perfect"
   - After 40 problems, start applying

---

**Start today. In 8 weeks, you'll be crushing ₹25L-₹35L interviews.** 🚀

**Day 1 starts NOW: Go solve "Two Sum"!** ✅
