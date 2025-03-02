<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Employee Shift Scheduler</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid black; padding: 10px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h2>Employee Shift Scheduler</h2>
    <label for="employeeName">Employee Name:</label>
    <input type="text" id="employeeName">
    <button onclick="addEmployee()">Add Employee</button>
    <div id="employees"></div>
    <button onclick="assignShifts()">Generate Schedule</button>
    <h2>Weekly Schedule</h2>
    <div id="scheduleOutput"></div>

    <script>
        class EmployeeScheduleManager {
            constructor() {
                this.SHIFTS = ['Morning', 'Afternoon', 'Evening'];
                this.DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
                this.employeePreferences = {}; 
                this.schedule = {};
                this.workCount = {};
                
                this.DAYS.forEach(day => {
                    this.schedule[day] = {};
                    this.SHIFTS.forEach(shift => {
                        this.schedule[day][shift] = [];
                    });
                });
            }

            addEmployeePreference(employee, preferences) {
                this.employeePreferences[employee] = preferences;
                this.workCount[employee] = 0;
            }

            assignShifts() {
                for (let employee in this.employeePreferences) {
                    let daysAssigned = 0;
                    for (let day in this.employeePreferences[employee]) {
                        let preferredShifts = this.employeePreferences[employee][day];
                        for (let shift of preferredShifts) {
                            if (daysAssigned < 5 && this.schedule[day][shift].length < 2 && !this.isEmployeeScheduled(employee, day)) {
                                this.schedule[day][shift].push(employee);
                                this.workCount[employee]++;
                                daysAssigned++;
                                break;
                            }
                        }
                    }
                }
                this.displaySchedule();
            }

            isEmployeeScheduled(employee, day) {
                return this.SHIFTS.some(shift => this.schedule[day][shift].includes(employee));
            }

            displaySchedule() {
                let output = '<table><tr><th>Day</th><th>Morning</th><th>Afternoon</th><th>Evening</th></tr>';
                this.DAYS.forEach(day => {
                    output += `<tr><td>${day}</td>`;
                    this.SHIFTS.forEach(shift => {
                        let employees = this.schedule[day][shift].join(', ') || 'None';
                        output += `<td>${employees}</td>`;
                    });
                    output += '</tr>';
                });
                output += '</table>';
                document.getElementById('scheduleOutput').innerHTML = output;
            }
        }

        const manager = new EmployeeScheduleManager();

        function addEmployee() {
            let name = document.getElementById("employeeName").value;
            if (!name) return;

            let preferences = {};
            manager.DAYS.forEach(day => {
                preferences[day] = [...manager.SHIFTS].sort(() => Math.random() - 0.5); // Random priority
            });
            manager.addEmployeePreference(name, preferences);
            document.getElementById("employeeName").value = "";
        }
    </script>
</body>
</html>
