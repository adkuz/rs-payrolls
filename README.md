# README

## Project Overview

This project provides tools to verify serbian payroll reports and generate annual summaries using Python. 

### Features:
1. **Verify Reports**: Validate payroll data for a specific year.  
   Command:  
   ```bash
   python3 invariants.py data/payrolls-2023.json 2023
   ```

2. **Generate Annual Summary**: Create a summarized annual payroll report.  
   Command:  
   ```bash
   python3 check_p4o.py data/payrolls-2023.json
   ```

---

## Setup Instructions

### 1. Create a Virtual Environment

It is recommended to use a virtual environment to manage dependencies.  

Run the following commands:  
```bash
python3 -m venv .venv
source .venv/bin/activate
```

To deactivate the virtual environment later:  
```bash
deactivate
```

---

### 2. Prepare the `data` Directory

Create a `data` directory to store your input files:  
```bash
mkdir data
```

Place your payroll data (e.g., `payrolls-2023.json`) in the `data` directory.

---

### 3. Template for Payroll Data

You can use the `template.json` file as a base to structure your payroll reports. Modify it according to your specific requirements.  

---

## Usage

### Verify Reports
Run the following command to validate payroll data for the year 2023:  
```bash
python3 invariants.py data/payrolls-2023.json 2023
```

### Generate Annual Summary
Run the following command to create a summarized report:  
```bash
python3 check_p4o.py data/payrolls-2023.json
```

---

## Notes

- Ensure the input JSON files conform to the expected structure, which can be derived from `template.json`.
- The script outputs validation results and annual summaries to the console or specified output files.

Happy coding! 🚀