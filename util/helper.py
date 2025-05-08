from common.constants import ActionNames, Constants



def printRoleMenu(roleConfig):
    print("=" * 40)
    print(f"{roleConfig['roleName']} Menu")
    print("=" * 40)
    for i, action in enumerate(roleConfig['actions']):
        print(f"\t{i + 1}. {action['title']}")
    print(f"\nEnter '{Constants.EXIT_COMMAND}' to exit the application.\n")


def getActionChoiceForRole(roleId: int):
    roleConfig = next((role for role in Constants.RoleConfigurations if role["roleId"] == roleId), None)

    if not roleConfig:
        print("No actions available for this role.")
        return None

    while True:
        printRoleMenu(roleConfig)
        choice = input("Please select an option: ").strip()

        if choice.lower() == Constants.EXIT_COMMAND:
            print("Exiting application...")
            return None

        if not choice.isdigit():
            print("Invalid input! Please enter a number corresponding to the menu options.")
            continue

        choice_num = int(choice)
        if 1 <= choice_num <= len(roleConfig['actions']):
            return roleConfig['actions'][choice_num - 1]
        else:
            print("Invalid option! Please try again.")