# %%
from julep import Client
from consts import clipper_input, api_key
import uuid
import yaml

AGENT_UUID = uuid.uuid4()
TASK_UUID = uuid.uuid4()
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
task_def = yaml.safe_load(open("agents.yaml"))

# %%
# creating the task object
task = client.tasks.create_or_update(task_id=TASK_UUID, agent_id=AGENT_UUID, **task_def)

# %%
execution = client.executions.create(task_id=task.id, input={"content": clipper_input})


# %%
# getting the execution details
execution = client.executions.get(execution.id)
# printing the output
print(execution.status, execution.output)

# %%

from pprint import pprint


for step in client.executions.transitions.list(execution_id=execution.id).items:
    print("___")
    pprint(step.dict())

# %%
print(execution.status)

# %%
