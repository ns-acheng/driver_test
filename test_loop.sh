#!/bin/bash

SITES=(
    "https://www.ebay.com"
    "https://www.microsoft.com"
    "https://www.apple.com"
    "https://www.google.com"
    "https://www.yahoo.com"
    "https://www.bing.com"
    "https://www.wikipedia.org"
    "https://www.nytimes.com"
    "https://www.cnn.com"
)

SERVICE_PLIST="/Library/LaunchDaemons/com.netskope.client.auxsvc.plist"
PROCESS_1="Netskope-Client.nsauxsvc"
PROCESS_2="Netskope-Client.NetskopeClientMacAppProxy"
LOOP_COUNT=300 # Total number of loops to run


cleanup() {
    echo -e "\nScript interrupted. Attempting to start service before exiting..."
    if [ -f "$SERVICE_PLIST" ]; then
        echo "Ensuring service is started..."
        # We are already root, so no sudo needed here
        launchctl bootstrap system "$SERVICE_PLIST"
    fi
    echo "Exiting."
    exit 1
}

trap cleanup SIGINT

open_sites() {
    echo "Opening sites in default browser..."
    for site in "${SITES[@]}"; do
        # Running as root, 'open' might fail. Run as the logged-in user.
        sudo -u "$LOGGED_IN_USER" open "$site"
        sleep 0.5
    done
}

close_browser_tabs() {
    echo "Closing browser tabs..."
    sudo -u "$LOGGED_IN_USER" osascript -e 'if application "Safari" is running then tell application "Safari" to close every document' 2>/dev/null
    sudo -u "$LOGGED_IN_USER" osascript -e 'if application "Google Chrome" is running then tell application "Google Chrome" to close every tab of every window' 2>/dev/null
    sudo -u "$LOGGED_IN_USER" osascript -e 'if application "Microsoft Edge" is running then tell application "Microsoft Edge" to close every tab of every window' 2>/dev/null
}

# --- Main Script ---

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root (use sudo)." 
   echo "Please run: sudo ./test_loop.sh"
   exit 1
fi

# Get the name of the user who is actually logged in
LOGGED_IN_USER=$(stat -f%Su /dev/console)
if [ -z "$LOGGED_IN_USER" ] || [ "$LOGGED_IN_USER" = "root" ]; then
    echo "ERROR: Could not determine the logged-in user. Exiting."
    exit 1
fi
echo "Running as root, but performing browser actions for user: $LOGGED_IN_USER"

# Define the user-specific crash path
USER_CRASH_PATH="/Users/$LOGGED_IN_USER/Library/Logs/DiagnosticReports/*nsclient*.*"


echo "Starting test loop. Will run $LOOP_COUNT times."
echo "Press Ctrl+C to interrupt. The script will try to re-start the service if interrupted."

for (( i=1; i<=$LOOP_COUNT; i++ )); do
    echo "================================================="
    echo "--- Loop $i of $LOOP_COUNT ---"
    echo "================================================="

    # 1. Open browser and connect
    open_sites

    # 2. Wait 60 seconds
    echo "Waiting 60 seconds..."
    sleep 60

    # 3. Stop the app
    echo "Stopping Netskope service..."
    if ! launchctl bootout system "$SERVICE_PLIST"; then
        # This is not critical, the service might already be stopped.
        echo "WARNING: 'launchctl bootout' command failed. Service might have already been stopped."
    fi

    # --- NEW: Wait and verify processes are stopped ---
    echo "Waiting 30 seconds for services to stop..."
    sleep 30

    echo "Verifying processes are stopped..."
    
    # Check process 1
    if launchctl list | grep -q "$PROCESS_1"; then
        echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        echo "ERROR: Process '$PROCESS_1' is STILL running after bootout."
        echo "Stopping script."
        echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        exit 1
    else
        echo "Process '$PROCESS_1' is stopped."
    fi

    # --- End of new check ---

    # 4. Close all browser tabs
    close_browser_tabs
    
    # Give a moment for files to be written if there was a crash
    echo "Waiting 5 seconds for any crash files to be written..."
    sleep 5 

    # 5. Search for crash dump
    echo "Checking for crash dumps at: $USER_CRASH_PATH"
    
    # Check if any files match the pattern
    if ls $USER_CRASH_PATH 1> /dev/null 2>&1; then
        echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        echo "ERROR: Found nsclient crash dump file. Stopping script."
        ls -l $USER_CRASH_PATH
        echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        # No need to call cleanup, we want the service to *stay* stopped for analysis
        exit 1
    else
        echo "No crash dumps found."
    fi

    # 6. Start the app
    echo "Starting Netskope service..."
    if ! launchctl bootstrap system "$SERVICE_PLIST"; then
        echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        echo "ERROR: 'launchctl bootstrap' command failed. Cannot start service."
        echo "Stopping script."
        echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        exit 1
    fi

    # 7. Wait 30 seconds
    echo "Waiting 30 seconds for services to start..."
    sleep 30

    # 8. Check if processes are running
    echo "Checking for processes..."
    
    # Check process 1
    if ! launchctl list | grep -q "$PROCESS_1"; then
        echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        echo "ERROR: Process '$PROCESS_1' is NOT running."
        echo "Stopping script."
        echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        exit 1
    else
        echo "Process '$PROCESS_1' is running."
    fi

    # Check process 2
    if ! launchctl list | grep -q "$PROCESS_2"; then
        echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        echo "ERROR: Process '$PROCESS_2' is NOT running."
        echo "Stopping script."
        echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        exit 1
    else
        echo "Process '$PROCESS_2' is running."
    fi

    echo "--- Loop $i complete ---"
done

echo "================================================="
echo "Successfully completed $LOOP_COUNT loops."
echo "================================================="
exit 0
