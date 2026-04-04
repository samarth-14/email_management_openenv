from environment import EmailEnvironment

print("Testing Email Environment...")
print("=" * 50)

# Create environment
env = EmailEnvironment()

# Test Easy Task
print("\n[TEST] Easy Task")
state = env.reset(task_type="easy")
print(f"Email from: {state['email']['sender']}")
print(f"Subject: {state['email']['subject']}")

# Test action
action = {"category": "spam"}
new_state, reward, done = env.step(action)
print(f"Reward: {reward}")

# Test Medium Task
print("\n[TEST] Medium Task")
state = env.reset(task_type="medium")
print(f"Email from: {state['email']['sender']}")
print(f"Subject: {state['email']['subject']}")

# Test action
action = {"response_text": "Thank you for your email. I will look into this issue."}
new_state, reward, done = env.step(action)
print(f"Reward: {reward}")

# Test Hard Task
print("\n[TEST] Hard Task")
state = env.reset(task_type="hard")
print(f"Email from: {state['email']['sender']}")
print(f"Subject: {state['email']['subject']}")

# Test action
action = {"response_text": "I understand the urgency. We can move the deadline to April 12th to accommodate your launch."}
new_state, reward, done = env.step(action)
print(f"Reward: {reward}")

print("\n" + "=" * 50)
print("All tests passed! ✅")