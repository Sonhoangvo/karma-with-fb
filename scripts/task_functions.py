from .execute_LLM_plan import GoToObject, ExploreObject, PickupObject, PutObject, SwitchOn, SwitchOff, OpenObject, CloseObject, BreakObject, SliceObject, CleanObject, Explore
# from task_decorator import replace_explore_with_custom

# @replace_explore_with_custom

def turn_off_light_then_turn_on_light(robot):
    # 0: SubTask 1: Turn off the light
    # 1: Go to the LightSwitch.
    GoToObject(robot, 'LightSwitch')
    # 2: Turn off the light.
    SwitchOff(robot, 'LightSwitch')
    # 3: Turn on the light immediately after.
    SwitchOn(robot, 'LightSwitch')