import sys
from BLP import BLP

def setup_initial_state():
    """Returns a fresh BLP instance loaded with the base assignment criteria."""
    blp = BLP()
    print("\n[System] Initializing Default State...")
    blp.add_subject("alice", "S", "U")
    blp.add_subject("bob", "C", "C")
    blp.add_subject("eve", "U", "U")
    
    blp.add_object("pub.txt", "U")
    blp.add_object("emails.txt", "C")
    blp.add_object("username.txt", "S")
    blp.add_object("password.txt", "TS")
    return blp

# Each case starts with a fresh BLP state (see main()).
# Scenarios follow Section 1.3 of Lab05-2.docx.
TEST_CASES = {
    1: [("read", "alice", "emails.txt")],  # Alice reads emails.txt
    2: [("read", "alice", "password.txt")],  # Alice reads password.txt
    3: [("read", "eve", "pub.txt")],  # Eve reads pub.txt
    4: [("read", "eve", "emails.txt")],  # Eve reads emails.txt
    5: [("read", "bob", "password.txt")],  # Bob reads password.txt
    6: [
        ("read", "alice", "emails.txt"),
        ("write", "alice", "pub.txt"),
    ],
    7: [
        ("read", "alice", "emails.txt"),
        ("write", "alice", "password.txt"),
    ],
    8: [
        ("read", "alice", "emails.txt"),
        ("write", "alice", "emails.txt"),
        ("read", "alice", "username.txt"),
        ("write", "alice", "emails.txt"),
    ],
    9: [
        ("read", "alice", "username.txt"),
        ("write", "alice", "emails.txt"),
        ("read", "alice", "password.txt"),
        ("write", "alice", "password.txt"),
    ],
    10: [
        ("read", "alice", "pub.txt"),
        ("write", "alice", "emails.txt"),
        ("read", "bob", "emails.txt"),
    ],
    11: [
        ("read", "alice", "pub.txt"),
        ("write", "alice", "username.txt"),
        ("read", "bob", "username.txt"),
    ],
    12: [
        ("read", "alice", "pub.txt"),
        ("write", "alice", "password.txt"),
        ("read", "bob", "password.txt"),
    ],
    13: [
        ("read", "alice", "pub.txt"),
        ("write", "alice", "emails.txt"),
        ("read", "eve", "emails.txt"),
    ],
    14: [
        ("read", "alice", "emails.txt"),
        ("write", "alice", "pub.txt"),
        ("read", "eve", "pub.txt"),
    ],
    15: [
        ("set_level", "alice", "S"),
        ("read", "alice", "username.txt"),
    ],
    16: [
        ("read", "alice", "emails.txt"),
        ("set_level", "alice", "U"),
        ("write", "alice", "pub.txt"),
        ("read", "eve", "pub.txt"),
    ],
    17: [
        ("read", "alice", "username.txt"),
        ("set_level", "alice", "C"),
        ("write", "alice", "emails.txt"),
        ("read", "eve", "emails.txt"),
    ],
    18: [
        ("read", "eve", "pub.txt"),
        ("read", "eve", "emails.txt"),
    ],
}

def execute_commands(blp, commands):
    for cmd in commands:
        action = cmd[0]
        if action == "read":
            blp.read(cmd[1], cmd[2])
        elif action == "write":
            blp.write(cmd[1], cmd[2])
        elif action == "set_level":
            blp.set_level(cmd[1], cmd[2])
        elif action == "validate":
            blp.validate_levels(cmd[1], cmd[2])

def main():
    print("========================================")
    print(" Bell-LaPadula (BLP) Simulator CLI      ")
    print("========================================")
    
    while True:
        print("\nOptions:")
        print("  [1-18] Run a specific test case (1 to 18)")
        print("  [A] Run all test cases sequentially")
        print("  [Q] Quit")
        choice = input("\nEnter choice: ").strip().upper()

        if choice == 'Q':
            print("Exiting simulator. Goodbye!")
            sys.exit(0)
        
        elif choice == 'A':
            for case_num in sorted(TEST_CASES.keys()):
                print(f"\n================ CASE #{case_num} ================")

                blp = setup_initial_state() 
                execute_commands(blp, TEST_CASES[case_num])
                blp.display_state()
                
        elif choice.isdigit() and int(choice) in TEST_CASES:
            case_num = int(choice)
            print(f"\n================ CASE #{case_num} ================")
            blp = setup_initial_state()
            execute_commands(blp, TEST_CASES[case_num])
            blp.display_state()
            
        else:
            print("Invalid input. Please enter a valid case number, 'A', or 'Q'.")

if __name__ == "__main__":
    main()