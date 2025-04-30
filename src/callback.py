import os
import json
import time
from datetime import datetime

class CallbackHandler:
    """Utility class to handle step callbacks in CrewAI agents"""
    
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.current_session = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_dir = os.path.join(log_dir, self.current_session)
        os.makedirs(self.session_dir, exist_ok=True)
        
        # Create a session log file
        self.session_log = os.path.join(self.session_dir, "session.log")
        with open(self.session_log, "w") as f:
            f.write(f"Session started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    def step_callback(self, step, agent_name):
        """Callback function for CrewAI agents to log their steps"""
        # Get timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Check if step is an AgentFinish object or has step_number attribute
        is_agent_finish = not hasattr(step, 'step_number')
        
        # Create log message
        if is_agent_finish:
            log_message = f"\n[{timestamp}] {agent_name} - Final Result:"
            # For AgentFinish objects, the output might be in the 'return_values' attribute or directly accessible
            output = getattr(step, 'return_values', {}).get('output', getattr(step, 'output', str(step)))
            task = "Task completed"
            step_number = "final"
        else:
            log_message = f"\n[{timestamp}] {agent_name} - Step {step.step_number}:"
            output = step.output
            task = step.task
            step_number = step.step_number
        
        log_message += f"\nTask: {task[:150]}..." if len(task) > 150 else f"\nTask: {task}"
        log_message += f"\nOutput: {output[:150]}..." if len(output) > 150 else f"\nOutput: {output}"
        
        # Print to console
        print(log_message)
        
        # Write to session log
        with open(self.session_log, "a") as f:
            f.write(log_message + "\n")
        
        # Save step details to a JSON file
        step_file = os.path.join(self.session_dir, f"{agent_name.replace(' ', '_')}_step_{step_number}.json")
        step_data = {
            "timestamp": timestamp,
            "agent_name": agent_name,
            "step_number": step_number,
            "task": task,
            "output": output
        }
        
        with open(step_file, "w") as f:
            json.dump(step_data, f, indent=2)
        
        return step

def print_progress_bar(iteration, total, prefix='', suffix='', length=50, fill='█'):
    """
    Call in a loop to create terminal progress bar
    """
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()

def timed_execution(func):
    """Decorator to time function execution"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Function '{func.__name__}' took {execution_time:.2f} seconds to execute")
        return result
    return wrapper 