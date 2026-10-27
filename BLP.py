class BLP:
    def __init__(self):
        # Security levels and their hierarchy are defined here as well as subjects and objects
        self.SECURITY_LEVELS = {"U": 0, "C": 1, "S": 2, "TS": 3}
        self.subjects = {}
        self.objects = {}

    # Checking if the security level is valid/exists
    def _is_valid_level(self, level):
        return level in self.SECURITY_LEVELS

    # Here we check if the subject and objects security levels match to enforce no read up and no write down for BLP
    def validate_levels(self, subject_id, object_id):
        if subject_id not in self.subjects or object_id not in self.objects:
            print(f"> FAIL: Subject '{subject_id}' or Object '{object_id}' not found.")
            return False
        
        # Getting current security level of subject and object
        subj_level = self.subjects[subject_id]['current_level']
        obj_level = self.objects[object_id]['level']
        
        # Returns true or false depending on if the security levels match or not
        if subj_level == obj_level:
            print(f"> VALIDATE MATCH: {subject_id} ({subj_level}) == {object_id} ({obj_level})")
            return True
        else:
            print(f"> VALIDATE NO MATCH: {subject_id} ({subj_level}) != {object_id} ({obj_level})")
            return False

    # Function to add a subject with their current and maximal security levels
    def add_subject(self, subject_id, max_level, start_level):
        if subject_id in self.subjects:
            print(f"> FAIL: Subject '{subject_id}' already exists.")
            return False
        if not self._is_valid_level(max_level) or not self._is_valid_level(start_level):
            print(f"> FAIL: Invalid level for '{subject_id}'. Use U, C, S, or TS.")
            return False
        if self.SECURITY_LEVELS[start_level] > self.SECURITY_LEVELS[max_level]:
            print(f"> FAIL: Start level {start_level} > Max level {max_level} for '{subject_id}'.")
            return False

        self.subjects[subject_id] = {
            'max_level': max_level,
            'current_level': start_level
        }
        return True

    # Function to add an object and its security level
    def add_object(self, object_id, level):
        if object_id in self.objects:
            print(f"> FAIL: Object '{object_id}' already exists.")
            return False
        if not self._is_valid_level(level):
            print(f"> FAIL: Invalid security level '{level}' for '{object_id}'.")
            return False

        self.objects[object_id] = {'level': level}
        return True

    # Function to set the level of a subject when needed to enforce no read up
    def set_level(self, subject_id, new_level):
        if subject_id not in self.subjects:
            print(f"> FAIL: Subject '{subject_id}' not found.")
            return False
        if not self._is_valid_level(new_level):
            print(f"> FAIL: Invalid level '{new_level}'. Use U, C, S, or TS.")
            return False

        subj = self.subjects[subject_id]
        subj_curr_num = self.SECURITY_LEVELS[subj['current_level']]
        subj_max_num = self.SECURITY_LEVELS[subj['max_level']]
        new_lvl_num = self.SECURITY_LEVELS[new_level]

        print(f"> Action: {subject_id} SET LEVEL to {new_level}...")

        # BLP prevents a subject from lowering their level to enforce no write down so it must be denied
        if new_lvl_num < subj_curr_num:
            print(f"> DENY: Cannot lower level from {subj['current_level']} to {new_level}.")
            return False
        # Subjects must be denied raising their security level past their maximal security level
        if new_lvl_num > subj_max_num:
            print(f"> DENY: New level {new_level} exceeds max level {subj['max_level']}.")
            return False
        if new_lvl_num == subj_curr_num:
            print(f"> INFO: Level already {new_level}. No change.")
            return True

        print(f"> ALLOW: Level changed to {new_level}.")
        self.subjects[subject_id]['current_level'] = new_level
        return True

    # Function to allow or deny a subject read access to an object
    def read(self, subject_id, object_id):
        if subject_id not in self.subjects or object_id not in self.objects:
            print(f"> FAIL: Subject '{subject_id}' or Object '{object_id}' not found.")
            return False

        subj = self.subjects[subject_id]
        obj = self.objects[object_id]

        subj_curr_num = self.SECURITY_LEVELS[subj['current_level']]
        subj_max_num = self.SECURITY_LEVELS[subj['max_level']]
        obj_lvl_num = self.SECURITY_LEVELS[obj['level']]

        print(f"> Action: {subject_id} READ {object_id}...")

        if obj_lvl_num <= subj_curr_num:
            print(f"> ALLOW: Obj Lvl ({obj['level']}) <= Subj Curr ({subj['current_level']}).")
            return True
            
        if obj_lvl_num <= subj_max_num:
            print(f"> ALLOW: Obj Lvl ({obj['level']}) <= Subj Max ({subj['max_level']}).")
            print(f"> INFO: Raising {subject_id}'s current level to {obj['level']}.")
            self.subjects[subject_id]['current_level'] = obj['level']
            return True

        print(f"> DENY: No Read Up! Obj Lvl ({obj['level']}) > Subj Max ({subj['max_level']}).")
        return False

    # Function to allow or deny a subject read access to an object
    def write(self, subject_id, object_id):
        if subject_id not in self.subjects or object_id not in self.objects:
            print(f"> FAIL: Subject '{subject_id}' or Object '{object_id}' not found.")
            return False

        subj = self.subjects[subject_id]
        obj = self.objects[object_id]

        subj_curr_num = self.SECURITY_LEVELS[subj['current_level']]
        obj_lvl_num = self.SECURITY_LEVELS[obj['level']]

        print(f"> Action: {subject_id} WRITE {object_id}...")

        if subj_curr_num <= obj_lvl_num:
            print(f"> ALLOW: Subj Curr ({subj['current_level']}) <= Obj Lvl ({obj['level']}).")
            return True

        print(f"> DENY: No Write Down! Subj Curr ({subj['current_level']}) > Obj Lvl ({obj['level']}).")
        return False

    # Shows the current state of the system
    def display_state(self):
        print("\n--- Current BLP State ---")
        for pid, s in self.subjects.items():
            print(f"  [Subject] {pid}: Curr={s['current_level']}, Max={s['max_level']}")
        for oid, o in self.objects.items():
            print(f"  [Object]  {oid}: Lvl={o['level']}")
        print("-------------------------\n")