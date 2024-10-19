# %%
!pip install julep -U --quiet

# %%
# Global UUID is generated for agent and task
import uuid

AGENT_UUID = uuid.uuid4()
TASK_UUID = uuid.uuid4() 

# %%
from julep import Client

api_key = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzQ1NTAxNzgsImlhdCI6MTcyOTM2NjE3OCwic3ViIjoiNTY0MmY5NGYtNWU1Yy01NTcxLTk3NzAtNzczYThiMTg1NzdlIn0.-2oh77xXFvuJAaVD-wVBBiXfwMF0mCf3L9BnbJu5OqMWsYMHPz3vAuZJL-BheQImsBb2fRSK6Msjny3LBzWmFg" # Your API key here

# Create a client
client = Client(api_key=api_key, environment="dev")

# %%
# Defining the agent
name = "QuestionTutor"
about = "QuestionTutor is a tutor that helps you understand the content of a paper by asking questions."
default_settings = {
    "temperature": 0.7,
    "top_p": 1,
    "min_p": 0.01,
    "presence_penalty": 0,
    "frequency_penalty": 0,
    "length_penalty": 1.0,
    "max_tokens": 300,
}

# Create the agent
agent = client.agents.create_or_update(
    agent_id=AGENT_UUID,
    name=name,
    about=about,
    model="claude-3.5-sonnet",
)

# %%
import yaml

# %%
task_def = yaml.safe_load("""
name: NotebookTutor

input_schema:
  type: object
  properties:
    content:
      type: string
      description: Content of the paper 
main:
  # Step 1: Generate a knowledge graph
  - prompt:
      - role: system
        content: You are {{agent.name}}. {{agent.about}}
      - role: user
        content: |-
          Based on the content '{{_.content}}', generate a list up to 5 topics about the provided content.  Return the output as a list of topics, with 3-5 questions per topic. Use the following format in valid yaml

          ```yaml
          topics:
          - name: "<string>"
            questions:
            - "<string>"
          - name: "<string>"
            questions:
            - "<string>"```

                           
    unwrap: true
    settings:
      model: claude-3.5-sonnet
    unwrap: true    
    
  - evaluate:
      knowledge_map: "load_yaml(_.split('```yaml')[1].split('```')[0].strip())"
""")

# %%
# creating the task object
task = client.tasks.create_or_update(
    task_id=TASK_UUID,
    agent_id=AGENT_UUID,
    **task_def
)

# %%
execution = client.executions.create(
    task_id=task.id,
    input={
         "content": """Europa Clipper (previously known as Europa Multiple Flyby Mission) is a space probe developed by NASA to study Europa, a Galilean moon of Jupiter. It was launched on October 14, 2024, and is expected to arrive in the Jupiter system in 2030. The spacecraft will then perform a series of flybys of Europa while in orbit around Jupiter.[14][15] The spacecraft is larger than any other used for previous NASA planetary missions.[16]

Europa Clipper will perform follow-up studies to those made by the Galileo spacecraft during its eight years (1995–2003) in Jupiter orbit, which indicated the existence of a subsurface ocean underneath Europa's ice crust. Plans to send a spacecraft to Europa were initially conceived with projects such as Europa Orbiter and Jupiter Icy Moons Orbiter, in which a spacecraft would be injected into orbit around Europa. However, due to the adverse effects of radiation from the magnetosphere of Jupiter in Europa orbit, it was decided that it would be safer to inject a spacecraft into an elliptical orbit around Jupiter and make 44 close flybys of the moon instead. The mission began as a joint investigation between the Jet Propulsion Laboratory (JPL) and the Applied Physics Laboratory (APL), and was built with a scientific payload of nine instruments contributed by JPL, APL, Southwest Research Institute, University of Texas at Austin, Arizona State University and University of Colorado Boulder. Europa Clipper complements European Space Agency's Jupiter Icy Moons Explorer, launched in 2023, which will attempt to fly past Europa twice and Callisto multiple times before moving into orbit around Ganymede.

Europa Clipper was launched from Kennedy Space Center Launch Complex 39A on October 14, 2024, aboard a Falcon Heavy rocket[17] in a fully expended configuration. The spacecraft will use gravity assists from Mars on March 1, 2025,[18] and Earth on December 3, 2026,[19] before arriving at Europa in April 2030.[20] """
    }
)

# %%
execution.id

# %%
# getting the execution details
execution = client.executions.get(execution.id)
#printing the output
execution.output

# %%

execution.status

# %%
