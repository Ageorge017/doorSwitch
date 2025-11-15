from utils.led import signal_error, continuous_blink
import time

class Logger:
    _loggerInstance = None 

    def __new__(cls, *args, **kwargs):
        """Controls instance creation, ensuring only one exists."""
        if cls._loggerInstance is None:
            cls._loggerInstance = super(Logger, cls).__new__(cls)
            cls._loggerInstance._initialized = False
        return cls._loggerInstance

    def __init__(self, name="PicoW"):
        """Initializes the logger configuration."""
        if self._initialized:
            return

        self.name = name
        self.level = "INFO"
        self.message_queue = []  # Queue to store log messages
        self._initialized = True
        
        self.log(f"Logger initialized ({self.name}).", "SETUP")


    def log(self, message, level="INFO"):
        """Logs a message to the console with a timestamp."""
        current_time_str = "00:00:00" 
        try:
            (year, month, mday, hour, minute, second, weekday, yearday) = time.localtime()
            current_time_str = f"{hour:02d}:{minute:02d}:{second:02d}"
        except:
            pass

        log_entry = {
            "timestamp": current_time_str,
            "level": level,
            "name": self.name,
            "message": message
        }
        
        # Check if we need to flush the queue (50+ items and not a fatal log)
        if len(self.message_queue) >= 50 and level != "FATAL":
            self._flush_queue_to_file()
            self.message_queue.clear()
        
        # Add to message queue
        self.message_queue.append(log_entry)
        
        # Print to console
        print(f"[{current_time_str}][{level:<6}][{self.name}] {message}")
        
        if level == "ERROR" or level == "FATAL":
            signal_error(1)

    def info(self, message):
        """Shorthand for INFO messages."""
        self.log(message, "INFO")

    def error(self, message):
        """Shorthand for ERROR messages, turns on the LED."""
        signal_error(1)
        self.log(message, "ERROR")
        
    def fatal(self, message):
        """Shorthand for FATAL messages, ensures LED is ON."""
        self.log(message, "FATAL")
        self._write_queue_to_file()
        continuous_blink()
    
    def _write_queue_to_file(self):
        """Writes the entire message queue to a text file."""
        try:
            # Generate filename with timestamp
            try:
                (year, month, mday, hour, minute, second, weekday, yearday) = time.localtime()
                timestamp = f"{year:04d}{month:02d}{mday:02d}_{hour:02d}{minute:02d}{second:02d}"
            except:
                timestamp = "unknown"
            
            filename = f"fatal_log_{timestamp}.txt"
            
            with open(filename, "w") as file:
                file.write(f"FATAL ERROR LOG - {self.name}\n")
                file.write("=" * 50 + "\n\n")
                
                for entry in self.message_queue:
                    file.write(f"[{entry['timestamp']}][{entry['level']:<6}][{entry['name']}] {entry['message']}\n")
                
                file.write("\n" + "=" * 50 + "\n")
                file.write(f"Total log entries: {len(self.message_queue)}\n")
            
            print(f"Fatal error log written to: {filename}")
            
        except Exception as e:
            print(f"Failed to write fatal log to file: {e}")
    
    def _flush_queue_to_file(self):
        """Flushes the message queue to a regular log file when queue is full."""
        try:
            try:
                (year, month, mday, hour, minute, second, weekday, yearday) = time.localtime()
                timestamp = f"{year:04d}{month:02d}{mday:02d}_{hour:02d}{minute:02d}{second:02d}"
            except:
                timestamp = "unknown"
            
            filename = f"log_flush_{timestamp}.txt"
            
            with open(filename, "w") as file:
                file.write(f"LOG QUEUE FLUSH - {self.name}\n")
                file.write("=" * 50 + "\n\n")
                
                for entry in self.message_queue:
                    file.write(f"[{entry['timestamp']}][{entry['level']:<6}][{entry['name']}] {entry['message']}\n")
                
                file.write("\n" + "=" * 50 + "\n")
                file.write(f"Total log entries flushed: {len(self.message_queue)}\n")
            
            print(f"Log queue flushed to: {filename}")
            
        except Exception as e:
            print(f"Failed to flush log queue to file: {e}")
    
    def get_message_queue(self):
        """Returns a copy of the message queue."""
        return self.message_queue.copy()
    
    def clear_message_queue(self):
        """Clears the message queue."""
        self.message_queue.clear()
    
    def get_queue_size(self):
        """Returns the current size of the message queue."""
        return len(self.message_queue)
    
    def get_recent_messages(self, count=10):
        """Returns the most recent 'count' messages from the queue."""
        return self.message_queue[-count:] if count <= len(self.message_queue) else self.message_queue.copy()

# --- Singleton Object Creation ---
# Create the single, global instance that all other modules will import.
SYSTEM_LOGGER = Logger("PICO_MAIN")