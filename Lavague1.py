from openai import OpenAI

client = OpenAI()

# #Sample query
# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "tell me a joke"},
#     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#   ]
# )
# print(completion.choices[0].message)

from lavague.drivers.selenium import SeleniumDriver
from lavague.core import ActionEngine, WorldModel
from lavague.core.agents import WebAgent

# Set up our three key components: Driver, Action Engine, World Model
driver = SeleniumDriver(headless=False, no_load_strategy=True)
action_engine = ActionEngine(driver)
world_model = WorldModel()

# Create Web Agent
agent = WebAgent(world_model, action_engine)

# Set URL
agent.get("https://magic-studio-stage.delightfulforest-40b0615c.centralindia.azurecontainerapps.io/login")

# Run agent with a specific objective
# agent.run("Go on the quicktour of PEFT")
agent.run("""You are an expert at world knowledge. Your goal is to create an assistant for Abhibus.
          
          Here's how you CAN acheive it by following the below steps: 
          Note: Do not open multiple windows
          Step 1: Login to Magic Studio stage and by using this email - divya@slanglabs.in and password - abc@123. You don't have to verify your account. 
          Step 2: if "Change your password" pop ups click on "ok" button.
          IMPORTANT:
          Step 3: Click on "Create Assistant" button on extreme left side to enter the assistant creation flow and then enter this link in "App URL" field - https://play.google.com/store/apps/details/AbhiBus_Bus_Ticket_Booking_App?id=com.app.abhibus&hl=en_IE , and then click on "Generate App Details" button and wait until all the fields are filled and then click on "Next: Add Capabilities" button. 
          Step 4: Now, Click on "Add New Capability" button on the top right and then click on "Domain FAQ" capability and then click on "Import" button within that section and wait for the spinner to stop.
          Step 5: Now, Click on "Add New Capability" button on the top right and then click on "Create custom capability" and then click on "Add a description for your capability" input box within that section and type "ability to search and book bus tickets from a source to a destination on a date for the given number of passengers. It must support the type of bus and type of seats preferred. "  and click on Generate capability button. wait for the spinner to stop.
          VERY IMPORTANT: MAINTAIN MAXIMUM ATTENTION:
          Step 5: Now in "Edit Capability" scroll to the bottom hit "compile" button at the bottom. 
          step 6: wait for the "Done " buttton to appear.
          Step 7: Click on "Done"
         
          """, display=True)

