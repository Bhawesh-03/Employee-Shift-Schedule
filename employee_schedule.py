import random
from collections import defaultdict

# Constants for shifts and days
SHIFTS = ['Morning', 'Afternoon', 'Evening']
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

class EmployeeScheduleManager:
    def __init__(self):
        self.employee_preferences = defaultdict(dict)  # Stores preferences {employee: {day: shift}}
        self.schedule = {day: {shift: [] for shift in SHIFTS} for day in DAYS}  # Weekly schedule
        self.work_count = defaultdict(int)  # Tracks the number of days each employee works
    
    def add_employee_preference(self, employee, preferences):
        """Add shift preferences for an employee."""
        self.employee_preferences[employee] = preferences
    
    def assign_shifts(self):
        """Assign shifts to employees while considering constraints."""
        # Step 1: Assign shifts based on employee preferences
        for employee, preferences in self.employee_preferences.items():
            days_assigned = 0
            for day, shift in preferences.items():
                if days_assigned < 5 and len(self.schedule[day][shift]) < 2:
                    self.schedule[day][shift].append(employee)
                    self.work_count[employee] += 1
                    days_assigned += 1
        
        # Step 2: Ensure at least 2 employees per shift
        for day in DAYS:
            for shift in SHIFTS:
                while len(self.schedule[day][shift]) < 2:
                    available_employees = [e for e in self.employee_preferences if self.work_count[e] < 5]
                    if available_employees:
                        chosen = random.choice(available_employees)
                        self.schedule[day][shift].append(chosen)
                        self.work_count[chosen] += 1
                    else:
                        break
        
        # Step 3: Resolve conflicts (employees working more than 1 shift per day)
        for day in DAYS:
            assigned_employees = defaultdict(int)
            for shift in SHIFTS:
                for employee in self.schedule[day][shift]:
                    assigned_employees[employee] += 1
            
            for employee, count in assigned_employees.items():
                if count > 1:
                    # Remove extra assignments
                    for shift in SHIFTS:
                        if employee in self.schedule[day][shift]:
                            self.schedule[day][shift].remove(employee)
                            break  # Ensure only one removal
    
    def display_schedule(self):
        """Print the final schedule."""
        for day, shifts in self.schedule.items():
            print(f"\n{day}:")
            for shift, employees in shifts.items():
                print(f"  {shift}: {', '.join(employees) if employees else 'No employees assigned'}")

# Example usage
manager = EmployeeScheduleManager()

# Adding employee shift preferences
manager.add_employee_preference('Alice', {'Monday': 'Morning', 'Tuesday': 'Afternoon', 'Thursday': 'Evening'})
manager.add_employee_preference('Bob', {'Monday': 'Afternoon', 'Wednesday': 'Morning', 'Friday': 'Evening'})
manager.add_employee_preference('Charlie', {'Tuesday': 'Morning', 'Thursday': 'Afternoon', 'Saturday': 'Evening'})
manager.add_employee_preference('David', {'Monday': 'Evening', 'Wednesday': 'Afternoon', 'Friday': 'Morning'})
manager.add_employee_preference('Eve', {'Tuesday': 'Evening', 'Thursday': 'Morning', 'Saturday': 'Afternoon'})
manager.add_employee_preference('Frank', {'Monday': 'Morning', 'Wednesday': 'Afternoon', 'Friday': 'Evening'})

# Assign shifts and display schedule
manager.assign_shifts()
manager.display_schedule()
