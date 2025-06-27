# DataAnalytics-NBA
Historical Statistics on NBA Champions

## Getting Started

This guide will help you set up the development environment for the DataAnalytics-NBA project.

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setting up the Virtual Environment

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <repository-url>
   cd DataAnalytics-NBA
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:

   **On macOS/Linux**:
   ```bash
   source venv/bin/activate
   ```

   **On Windows**:
   ```bash
   venv\Scripts\activate
   ```

4. **Verify the virtual environment is active**:
   ```bash
   which python  # Should point to your venv directory
   pip list      # Should show only basic packages
   ```

### Installing Dependencies

1. **Install required packages** (if you have a requirements.txt file):
   ```bash
   pip install -r requirements.txt
   ```

2. **Or install packages individually** (if no requirements.txt exists):
   ```bash
   pip install <package-name>
   ```

3. **Verify installation**:
   ```bash
   pip list
   ```

### Running the Project

1. **Make sure your virtual environment is activated**:
   ```bash
   source venv/bin/activate  # macOS/Linux
   # or
   venv\Scripts\activate     # Windows
   ```

2. **Run your project**:
   ```bash
   python main.py
   ```
   

### Deactivating the Virtual Environment

When you're done working on the project:
```bash
deactivate
```

### Troubleshooting

- **If you get permission errors**: Make sure you have write permissions in the project directory
- **If packages fail to install**: Try upgrading pip first: `pip install --upgrade pip`
- **If you need to recreate the environment**: Delete the `venv` folder and repeat the setup steps
- **If Black formatting fails**: Make sure you're in the virtual environment and Black is installed

### Notes

- Always activate the virtual environment before working on the project
- The virtual environment keeps project dependencies isolated from your system Python
- Remember to add `venv/` to your `.gitignore` file if it's not already there
