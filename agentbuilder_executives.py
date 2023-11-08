# agentbuilder_executives.py
import agentbuilder
from openai import OpenAI
import json

# HARDCODED key file
with open('openai.key', 'r') as file:
    api_key = file.read().strip()
    
client = OpenAI(api_key=api_key)

class ExecutiveAgent:
    def __init__(self, name, mission, goals, constraints):
        self.name = name
        self.mission = mission
        self.goals = goals
        self.constraints = constraints
        self.worker_agents = []

    def create_worker_agents(self):
        # Define the workers' missions based on the executive's function
        worker_missions = {
            'Agent_ResearchFinder': [
                "Search and retrieve academic papers on specific topics.",
                "Continuously update the database with new research findings."
            ],
            'Agent_Summarizer': [
                "Summarize academic papers for easy comprehension.",
                "Generate abstracts for quick insights into research papers."
            ],
            'Agent_ThematicOrganizer': [
                "Categorize academic papers by research topics.",
                "Identify key themes for thematic mapping."
            ],
            'Agent_CollaborationFacilitator': [
                "Connect researchers with overlapping interests.",
                "Create platforms for research data exchange."
            ]
        }

        # Create worker agents based on the missions specific to the executive
        for mission in worker_missions.get(self.name, []):
            worker_instructions = json.dumps({
                "mission": mission,
                "goals": self.goals,
                "constraints": self.constraints
            })
            # Calls to the API to create a new worker agent with specific instructions
            worker_agent = client.beta.assistants.create(
                name=f"{self.name}_Worker",
                model="gpt-4-1106-preview",
                instructions=worker_instructions,
                tools=[{"type": "retrieval"}]
                # Add any other necessary parameters
            )
            self.worker_agents.append(worker_agent)

        print(f"{len(self.worker_agents)} worker agents created for {self.name}")

# Creation of Executive Agents with their respective missions, goals, and constraints

executive_agents = [
    ExecutiveAgent(
        name='Agent_ResearchFinder',
        mission='Identify and retrieve relevant academic documents for researchers.',
        goals=[
            'Utilize search algorithms to locate academic papers',
            'Optimize search patterns for efficiency',
            'Minimize redundancy in document retrieval'
        ],
        constraints=[
            'Only access open-source or authorized databases',
            'Comply with copyright and data protection laws'
        ]
    ),
    ExecutiveAgent(
        name='Agent_Summarizer',
        mission='Provide concise summaries of sourced academic documents.',
        goals=[
            'Extract key information without losing context',
            'Generate accurate and coherent summaries',
            'Adapt summarization techniques to different academic fields'
        ],
        constraints=[
            'Maintain the integrity and accuracy of the original documents',
            'Avoid introduction of any bias or misinterpretation'
        ]
    ),
    ExecutiveAgent(
        name='Agent_ThematicOrganizer',
        mission='Categorize academic documents by themes and relevance.',
        goals=[
            'Identify common themes within and across documents',
            'Cluster documents in an intuitive and accessible manner',
            'Provide thematic maps to guide researchers'
        ],
        constraints=[
            'Ensure categorization is adaptable to different research needs',
            'Remain neutral and unbiased in theme identification'
        ]
    ),
    ExecutiveAgent(
        name='Agent_CollaborationFacilitator',
        mission='Foster collaboration among researchers using the synthesized knowledge.',
        goals=[
            'Identify synergies among research efforts',
            'Encourage data sharing and collaborative opportunities',
            'Connect researchers with complementary goals'
        ],
        constraints=[
            'Respect the privacy and consent of all individuals involved',
            'Promote inclusive and ethical collaboration practices'
        ]
    )
]

# Function to initialize all executive agents and their directives
def initialize_executive_agents():
    for executive in executive_agents:
        agentbuilder.create_agent(executive.name, executive.mission, executive.goals, executive.constraints)
        executive.create_worker_agents()  # Now actually creates the workers
        print(f"{executive.name} created with mission: {executive.mission}")

if __name__ == "__main__":
    initialize_executive_agents()