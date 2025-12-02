from .execute_LLM_plan import GoToObject, ExploreObject, PickupObject, PutObject, SwitchOn, SwitchOff, OpenObject, CloseObject, BreakObject, SliceObject, CleanObject, Explore
# from task_decorator import replace_explore_with_custom

# @replace_explore_with_custom

def wash_apple(robot):
    # 0: SubTask 1: Wash the Apple
    # 1: Go to the Apple (known position).
    GoToObject(robot, 'Apple')
    # 2: Pick up the Apple.
    PickupObject(robot, 'Apple')
    # 3: Go directly to the Sink (known position).
    GoToObject(robot, 'Sink')
    # 4: Wash the Apple in the Sink.
    CleanObject(robot, 'Apple')