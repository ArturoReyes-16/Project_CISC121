# Project_CISC121
# Binary Search 
## Demo Video
https://github.com/user-attachments/assets/7c199d61-9bee-428d-8dbe-14947dea8aaf
## Edge Cases Screenshots
### Edge Case 1: Input out of bounds

When the target value (child's weight) is outside the search array (dosage table) the simulation continues to allow the user to see by themselves the error. Output is all ranges are discarded (RED) and error message "The weight is out of bounds! No valid dosage range found."

<img width="1218" height="770" alt="Out of bounds edge case" src="https://github.com/user-attachments/assets/d77f33df-a190-4d48-b211-3a9ae39b22d2" />
### Edge Case 2: Incorrect user input


When the user does not choose the correct button (LEFT, RIGHT, or DONE), the simulation stops and gives feedback to the user. 

<img width="1218" height="770" alt="Incorrect input edge case" src="https://github.com/user-attachments/assets/13102e32-2b70-40c2-8349-4fa51b8c66ef" />

## Problem Breakdown & Computational Thinking 
I chose **Binary Search** as it is the most efficient of the searching algorithms on worst case scenario, so its understanding is of high importance. Also, I wanted the app to be useful in solving a real life scenario related to health and wellness. So, for the topic of choosing the correct dosage amount to give Tylenol to a child, binary search seemed the most appropiate algorithm. 

### **Decomposition** 
- Take user input (child’s weight)
- Store dosage ranges (the table)
- Perform binary search logic (midpoint, left/right decisions)
- Handle user decisions (buttons: left, right, done)
- Update the UI (messages + table colors)

### **Abstraction**
- User doesn’t see indices, loops, or calculations
- They just click buttons (left/right/done)
- The table visually shows progress (red/yellow/green)

### **Pattern Recognition**
Binary search follows the same pattern at every step:
- Find the middle range
- Compare target weight to that range
- Decide: go left, go right, or done
- Repeat until found

### **Algorithm Design**
Input (user weight and button choice) -> Process (Binary search comparison and range update) -> Output (feedback message and updated visual table)
## Steps to run
1. Clone repository
2. Install gradio using:
```
pip install gradio
```
or 
```
python -m pip install gradio
```
3. Run and follow the local host link provided 

## Hugging Face Link
Alternatively, follow this link to access the app:

https://huggingface.co/spaces/ArturoReyes-16/Child_Tylenol_Dosage_Assistant_Binary_Search_Simulator

## Author & Acknoledgement
ChatGPT was used to debug parts of the code, assist with implementing Gradio features, and improve comments. All final code and design decisions were implemented by me.  
