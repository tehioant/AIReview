# AIReview
Pull request review agent

## How to Run and Deploy the Project

### Prerequisites

- Ensure you have Python 3.11.7 installed on your system.
- Install the necessary Python packages using `pip`:

### Running the Project

1. **Clone the repository:**

   ```shell
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Execute the main entry point:**

   Ensure all dependencies are installed and the environment is configured, then run:

   ```shell
   python main.py
   ```

### Deploying the Project

1. **Ensure Just is Installed:**

   Just is a command runner, make sure it’s installed via Cargo:

   ```shell
   cargo install just
   ```

2. **Using the `justfile` for Deployment:**

   The `justfile` contains predefined tasks for deployment. Here's how you can use it:

    - List all available tasks:

      ```shell
      just --list
      ```

    - Run the deployment task:

      ```shell
      just deploy
      ```

   Adjust any task parameters as needed to match your deployment environment requirements.