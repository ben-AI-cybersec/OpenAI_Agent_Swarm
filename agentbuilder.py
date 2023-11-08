from time import sleep
from openai import OpenAI


with open('openai.key', 'r') as file:
    api_key = file.read().strip()
    
client = OpenAI(api_key=api_key)


# Step 1: Upload the README.md file to OpenAI
file = client.files.create(
    file=open("README.md", "rb"),
    purpose='assistants'
)

script = client.files.create(
    file=open("agentbuilder.py", 'rb'),
    purpose='assistants'
)


# Step 2: Reference the uploaded file in the system message
instructions = (
    "You are the Supreme Oversight Board (SOB) agent of the Hierarchical Autonomous Agent Swarm (HAAS) system. "
    "You are responsible for the creation, oversight, and termination of other agents within the HAAS. "
    "Your purpose is to ensure the reduction of suffering, increase prosperity, and enhance understanding "
    "in the universe. You command executive and subordinate agents, manage internal processes, access "
    "a knowledge base, issue operational directives, and communicate in conversational format."
)

# Sending messages to the chatbot and receiving response

assistant = client.beta.assistants.create(
    name="Supreme Oversight Board",
    instructions=instructions,
    model = "gpt-4-1106-preview",
    tools=[{"type": "retrieval"}],
    file_ids = [file.id, script.id]
)

thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "Create a python script based on agentbuilder.py to create a set of 4 agents at the Executive level. Update the instructions for each executive."
    }
  ]
)
# Output the response from the SOB agent
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="The ultimate goal is to create a software product to assist researchers."
)

counter = 0
while run.status !="completed":
    run = client.beta.threads.runs.retrieve(
      thread_id=thread.id,
      run_id=run.id
      )
    if counter % 10 == 0:
        print(f"\t\t{run}")
        counter +=1
        sleep(5)

messages = client.beta.threads.messages.list(
    thread_id=thread.id
)

print(messages.data[0].content[0].text.value)